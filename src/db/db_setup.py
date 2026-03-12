import sqlite3
import json
import threading
from src.utils import AppLogger as LOG

_db_lock = threading.Lock()
_conn = sqlite3.connect('questions.db', check_same_thread=False)

def _execute(query, params=(), commit=False, fetch=None):
    with _db_lock:
        try:
            c = _conn.cursor()
            c.execute(query, params)
            if commit:
                _conn.commit()
            if fetch == 'one':
                return c.fetchone()
            elif fetch == 'all':
                return c.fetchall()
            return c
        except sqlite3.Error as e:
            LOG.ERR(f"DB Error: {e.args[0]} on query: {query}")
            return None

def create_tables():
    _execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  subject TEXT, level INTEGER, question TEXT,
                  option_a TEXT, option_b TEXT, option_c TEXT, option_d TEXT, correct_option TEXT)''', commit=True)

    _execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT)''', commit=True)

    _execute('''CREATE TABLE IF NOT EXISTS scores
                 (user_id INTEGER, score INTEGER, total_questions INTEGER, FOREIGN KEY(user_id) REFERENCES users(user_id))''', commit=True)

    _execute('''CREATE TABLE IF NOT EXISTS groups
                 (group_id INTEGER PRIMARY KEY, group_name TEXT, group_type TEXT)''', commit=True)

def get_username_from_user_id(user_id):
    result = _execute("SELECT first_name FROM users WHERE user_id=?", (user_id,), fetch='one')
    return result[0] if result else None

def add_user(user_id, username, first_name, last_name):
    _execute("INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
             (user_id, username, first_name, last_name), commit=True)

def get_user(user_id):
    return _execute("SELECT * FROM users WHERE user_id = ?", (user_id,), fetch='one')

def add_group(group_id, group_name, group_type):
    _execute("INSERT OR IGNORE INTO groups (group_id, group_name, group_type) VALUES (?, ?, ?)",
             (group_id, group_name, group_type), commit=True)

def get_group(group_id):
    return _execute("SELECT * FROM groups WHERE group_id = ?", (group_id,), fetch='one')

def get_all_groups():
    return _execute("SELECT * FROM groups", fetch='all')

def add_question(sub, level, question, option_a, option_b, option_c, option_d, correct_option=""):
    _execute("INSERT INTO questions (subject, level, question, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
             (sub, level, question, option_a, option_b, option_c, option_d, correct_option), commit=True)
    LOG.INF("Question Added")

def get_random_question():
    question = _execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1", fetch='one')
    if question is None:
        return "NEED_ATTENTION"
    return question

def get_subjects():
    subjects = _execute("SELECT DISTINCT subject FROM questions", fetch='all')
    return [s[0] for s in subjects] if subjects else []

def get_random_question_by_subject(subject):
    question = _execute("SELECT * FROM questions WHERE subject = ? ORDER BY RANDOM() LIMIT 1", (subject,), fetch='one')
    return question if question else get_random_question()

def update_user_score(user_id, correct):
    row = _execute("SELECT * FROM scores WHERE user_id = ?", (user_id,), fetch='one')
    if row:
        score = row[1] + (1 if correct else 0)
        total_questions = row[2] + 1
        _execute("UPDATE scores SET score = ?, total_questions = ? WHERE user_id = ?",
                 (score, total_questions, user_id), commit=True)
    else:
        score = 1 if correct else 0
        total_questions = 1
        _execute("INSERT INTO scores (user_id, score, total_questions) VALUES (?, ?, ?)",
                 (user_id, score, total_questions), commit=True)

def get_user_score(user_id):
    return _execute("SELECT score, total_questions FROM scores WHERE user_id = ?", (user_id,), fetch='one')

def get_leaderboard():
    return _execute('''SELECT u.username, s.score, s.total_questions
                       FROM scores s JOIN users u ON s.user_id = u.user_id
                       ORDER BY s.score DESC LIMIT 10''', fetch='all')

def dump_db(db_name):
    try:
        tables = _execute("SELECT name FROM sqlite_master WHERE type='table';", fetch='all')
        if not tables: return
        
        db_data = {}
        with _db_lock:
            c = _conn.cursor()
            for table_name in tables:
                table_name = table_name[0]
                c.execute(f"SELECT * FROM {table_name};")
                rows = c.fetchall()
                c.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in c.fetchall()]
                db_data[table_name] = [dict(zip(columns, row)) for row in rows]
        
        with open('db_dump.json', 'w') as f:
            json.dump(db_data, f, indent=4)
    except sqlite3.Error as e:
        LOG.ERR(f"An error occurred: {e.args[0]}")

def dump_db_to_text(db_name, output_file):
    try:
        tables = _execute("SELECT name FROM sqlite_master WHERE type='table';", fetch='all')
        if not tables: return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            with _db_lock:
                c = _conn.cursor()
                for table_name in tables:
                    table_name = table_name[0]
                    f.write(f"Table: {table_name}\n")
                    c.execute(f"PRAGMA table_info({table_name});")
                    columns = [col[1] for col in c.fetchall()]
                    f.write("\t" + "\t".join(columns) + "\n")
                    f.write("\t" + "-" * (len("\t".join(columns))) + "\n")
                    c.execute(f"SELECT * FROM {table_name};")
                    for row in c.fetchall():
                        f.write("\t" + "\t".join(str(col) for col in row) + "\n")
                    f.write("\n")
        
        LOG.INF(f"Database dumped to {output_file}")
    except sqlite3.Error as e:
        LOG.ERR(f"An error occurred: {e.args[0]}")

def deleteQuestionsTable():
    _execute("DROP TABLE questions", commit=True)

def dump_db_t():
    dump_db_to_text('questions.db', 'db_dump.txt')
    dump_db('questions.db')

if __name__ == "__main__":
    create_tables()
    dump_db_to_text('questions.db', 'db_dump.txt')