import sqlite3
import json

def create_tables():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()

    # Create table for storing questions
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  subject TEXT,
                  level INTEGER,
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


def get_username_from_user_id(user_id):
    conn = sqlite3.connect('questions.db')  # Replace with your DB path
    c = conn.cursor()
    c.execute("SELECT first_name FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

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

def add_question(sub, level, question, option_a, option_b, option_c, option_d, correct_option = ""):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("INSERT INTO questions (subject, level, question, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (sub, level, question, option_a, option_b, option_c, option_d, correct_option))
    conn.commit()
    conn.close()

def get_random_question():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    #c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    question = c.fetchone()
    if question == None:
        conn.close()
        return "NEED_ATTENTION"
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

def dump_db(db_name):
    """
    Dumps the complete SQLite database into a JSON file.
    
    Parameters:
    db_name (str): The name of the SQLite database file.
    
    Returns:
    None
    """
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        # Get list of all tables in the database
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        
        db_data = {}
        
        # Iterate over each table and extract its data
        for table_name in tables:
            table_name = table_name[0]
            c.execute(f"SELECT * FROM {table_name};")
            rows = c.fetchall()
            
            # Get column names
            c.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in c.fetchall()]
            
            # Store table data in a list of dictionaries
            table_data = []
            for row in rows:
                row_data = dict(zip(columns, row))
                table_data.append(row_data)
            
            db_data[table_name] = table_data
        
        # Close the database connection
        conn.close()
        
        # Dump database data to a JSON file
        with open('db_dump.json', 'w') as f:
            json.dump(db_data, f, indent=4)
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")



def dump_db_to_text(db_name, output_file):
    """
    Dumps the complete SQLite database to a text file in a tabular format.
    
    Parameters:
    db_name (str): The name of the SQLite database file.
    output_file (str): The name of the output file.
    
    Returns:
    None
    """
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        # Get list of all tables in the database
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for table_name in tables:
                table_name = table_name[0]
                
                # Write table header
                f.write(f"Table: {table_name}\n")
                
                # Get column names
                c.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in c.fetchall()]
                
                # Write column names
                f.write("\t" + "\t".join(columns) + "\n")
                
                # Write separator
                f.write("\t" + "-" * (len("\t".join(columns))) + "\n")
                
                # Write table data
                c.execute(f"SELECT * FROM {table_name};")
                rows = c.fetchall()
                for row in rows:
                    f.write("\t" + "\t".join(str(col) for col in row) + "\n")
                
                f.write("\n")  # Separate tables with a blank line
        
        conn.close()
        
        print(f"Database dumped to {output_file}")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

def deleteQuestionsTable():
    conn = sqlite3.connect('questions.db')
    # Create a cursor object
    c = conn.cursor()
    # Delete the entire 'question' table
    c.execute("DROP TABLE questions")
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

if __name__ == "__main__":
    create_tables()
    # Sample data
    #add_question("Which is the largest continent by land area?","Africa","Asia","Europe","North America")
    # Call the function
    #dump_db('questions.db')
    # Call the function
    dump_db_to_text('questions.db', 'db_dump.txt')
    #deleteQuestionsTable()
    
    
    
    
