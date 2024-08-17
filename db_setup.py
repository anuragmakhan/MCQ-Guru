import sqlite3

def create_tables():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()

    # Create table for storing questions
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question TEXT,
                  option_a TEXT,
                  option_b TEXT,
                  option_c TEXT,
                  option_d TEXT,
                  correct_option TEXT)''')

    # Create table for storing user data
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  first_name TEXT,
                  last_name TEXT)''')

    # Create table for storing user scores
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (user_id INTEGER,
                  score INTEGER,
                  total_questions INTEGER,
                  FOREIGN KEY(user_id) REFERENCES users(user_id))''')

    # Create table for storing group data
    c.execute('''CREATE TABLE IF NOT EXISTS groups
                 (group_id INTEGER PRIMARY KEY,
                  group_name TEXT,
                  group_type TEXT)''')
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
              (user_id, username, first_name, last_name))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def add_group(group_id, group_name, group_type):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO groups (group_id, group_name, group_type) VALUES (?, ?, ?)",
              (group_id, group_name, group_type))
    conn.commit()
    conn.close()

def get_group(group_id):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM groups WHERE group_id = ?", (group_id,))
    group = c.fetchone()
    conn.close()
    return group

def get_all_groups():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM groups")
    groups = c.fetchall()
    conn.close()
    return groups

def add_question(question, option_a, option_b, option_c, option_d, correct_option = ""):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?)",
              (question, option_a, option_b, option_c, option_d, correct_option))
    conn.commit()
    conn.close()

def get_random_question():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    #c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    c.execute("SELECT * FROM questions WHERE correct_option IS NULL OR correct_option = '' ORDER BY RANDOM() LIMIT 1")
    question = c.fetchone()
    if question == None:
        print("FATAL: DB EMPTY       !!!!!!!!!!")
        conn.close()
        return "NEED_ATTENTION"
    else:
        c.execute("UPDATE questions SET correct_option = 'visited' WHERE id = ?", (question[0],))
        conn.commit()
    conn.close()
    return question

def update_user_score(user_id, correct):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM scores WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if row:
        score = row[1] + (1 if correct else 0)
        total_questions = row[2] + 1
        c.execute("UPDATE scores SET score = ?, total_questions = ? WHERE user_id = ?",
                  (score, total_questions, user_id))
    else:
        score = 1 if correct else 0
        total_questions = 1
        c.execute("INSERT INTO scores (user_id, score, total_questions) VALUES (?, ?, ?)",
                  (user_id, score, total_questions))

    conn.commit()
    conn.close()

def get_user_score(user_id):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("SELECT score, total_questions FROM scores WHERE user_id = ?", (user_id,))
    score = c.fetchone()
    conn.close()
    return score

def get_leaderboard():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute('''SELECT u.username, s.score, s.total_questions
                 FROM scores s
                 JOIN users u ON s.user_id = u.user_id
                 ORDER BY s.score DESC LIMIT 10''')
    leaderboard = c.fetchall()
    conn.close()
    return leaderboard

if __name__ == "__main__":
    create_tables()
    # Sample data
    add_question("Which is the largest continent by land area?","Africa","Asia","Europe","North America")
