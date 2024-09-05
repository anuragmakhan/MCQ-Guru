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
    deleteQuestionsTable()
    create_tables()
    # Sample data
    #add_question("Which is the largest continent by land area?","Africa","Asia","Europe","North America")
    # Call the function
    #dump_db('questions.db')
    # Call the function
    dump_db_to_text('questions.db', 'db_dump.txt')
    #deleteQuestionsTable()
    
    
    add_question("SCIENCE","0","What is the chemical symbol for water?","H2O","O2","CO2","H2","H2O")

    add_question("SCIENCE","0","Which planet is known as the Red Planet?","Earth","Mars","Venus","Jupiter","Mars")

    add_question("SCIENCE","0","What is the speed of light in a vacuum?","300,000 km/s","150,000 km/s","450,000 km/s","600,000 km/s","300,000 km/s")

    add_question("SCIENCE","0","Who is known as the father of modern physics?","Isaac Newton","Albert Einstein","Galileo Galilei","Niels Bohr","Albert Einstein")

    add_question("SCIENCE","0","What is the basic unit of life?","Atom","Molecule","Cell","Organ","Cell")

    add_question("SCIENCE","0","What is the atomic number of Carbon?","12","6","14","8","6")

    add_question("SCIENCE","0","Which gas is most abundant in the Earth's atmosphere?","Oxygen","Nitrogen","Carbon Dioxide","Argon","Nitrogen")

    add_question("SCIENCE","0","Which vitamin is produced when the skin is exposed to sunlight?","Vitamin A","Vitamin B","Vitamin C","Vitamin D","Vitamin D")

    add_question("SCIENCE","0","What is the powerhouse of the cell?","Nucleus","Mitochondria","Ribosome","Lysosome","Mitochondria")

    add_question("SCIENCE","0","Which planet is closest to the sun?","Earth","Venus","Mercury","Mars","Mercury")

    add_question("SCIENCE","0","What is the most abundant element in the universe?","Oxygen","Hydrogen","Helium","Carbon","Hydrogen")

    add_question("SCIENCE","0","What is the chemical formula for table salt?","NaCl","KCl","NaOH","HCl","NaCl")

    add_question("SCIENCE","0","What is the hardest natural substance on Earth?","Gold","Diamond","Iron","Quartz","Diamond")

    add_question("SCIENCE","0","Which blood cells help in clotting?","Red blood cells","White blood cells","Platelets","Plasma","Platelets")

    add_question("SCIENCE","0","Which planet has the largest rings in the solar system?","Jupiter","Uranus","Saturn","Neptune","Saturn")

    add_question("SCIENCE","0","What type of bond is formed between two atoms sharing electrons?","Ionic bond","Covalent bond","Hydrogen bond","Metallic bond","Covalent bond")

    add_question("SCIENCE","0","Which organ is primarily responsible for filtering blood in the human body?","Liver","Heart","Kidney","Lung","Kidney")

    add_question("SCIENCE","0","What is the primary gas found in the air we exhale?","Oxygen","Nitrogen","Carbon Dioxide","Helium","Carbon Dioxide")

    add_question("SCIENCE","0","Which scientist developed the theory of relativity?","Nikola Tesla","Thomas Edison","Albert Einstein","James Maxwell","Albert Einstein")

    add_question("SCIENCE","0","What is the boiling point of water at sea level?","0°C","50°C","100°C","150°C","100°C")

    add_question("SCIENCE","0","Which part of the plant is responsible for photosynthesis?","Root","Stem","Leaf","Flower","Leaf")

    add_question("SCIENCE","0","What is the SI unit of force?","Joule","Newton","Pascal","Watt","Newton")

    add_question("SCIENCE","0","Which planet is known as the Earth's twin?","Mars","Jupiter","Venus","Mercury","Venus")

    add_question("SCIENCE","0","What is the process by which plants make their food?","Respiration","Transpiration","Photosynthesis","Fermentation","Photosynthesis")

    add_question("SCIENCE","0","What is the smallest unit of matter?","Molecule","Atom","Proton","Neutron","Atom")

    add_question("SCIENCE","0","Which gas is used in the process of photosynthesis?","Oxygen","Carbon Dioxide","Nitrogen","Hydrogen","Carbon Dioxide")

    add_question("SCIENCE","0","What is the most common type of star in the universe?","Red dwarf","Yellow dwarf","Blue giant","White dwarf","Red dwarf")

    add_question("SCIENCE","0","Which organelle is known as the 'brain' of the cell?","Mitochondria","Nucleus","Ribosome","Golgi apparatus","Nucleus")

    add_question("SCIENCE","0","What is the pH level of pure water?","3","5","7","9","7")

    add_question("SCIENCE","0","Which type of cell division results in two identical daughter cells?","Mitosis","Meiosis","Binary fission","Budding","Mitosis")

    add_question("SCIENCE","0","Which element is essential for the formation of hemoglobin in the blood?","Calcium","Iron","Sodium","Potassium","Iron")

    add_question("SCIENCE","0","What is the primary component of natural gas?","Butane","Propane","Methane","Ethane","Methane")

    add_question("SCIENCE","0","What is the largest organ in the human body?","Heart","Liver","Skin","Brain","Skin")

    add_question("SCIENCE","0","Which planet is known as the Gas Giant?","Mercury","Mars","Jupiter","Venus","Jupiter")

    add_question("SCIENCE","0","What is the name of the process by which cells divide to form gametes?","Mitosis","Meiosis","Fusion","Fragmentation","Meiosis")

    add_question("SCIENCE","0","What is the chemical symbol for potassium?","K","P","Pt","Po","K")

    add_question("SCIENCE","0","Which organ is responsible for producing insulin?","Liver","Kidney","Pancreas","Gallbladder","Pancreas")

    add_question("SCIENCE","0","What type of energy is stored in a battery?","Kinetic energy","Potential energy","Chemical energy","Thermal energy","Chemical energy")

    add_question("SCIENCE","0","Which blood type is considered the universal donor?","A+","AB+","O-","B+","O-")

    add_question("SCIENCE","0","What is the main gas found in the Earth's ozone layer?","Oxygen","Ozone","Nitrogen","Carbon dioxide","Ozone")

    add_question("SCIENCE","0","What is the process of converting solid directly into gas called?","Condensation","Sublimation","Evaporation","Deposition","Sublimation")

    add_question("SCIENCE","0","Which organ of the human body is primarily responsible for detoxification?","Heart","Lung","Liver","Kidney","Liver")

    add_question("SCIENCE","0","What is the smallest bone in the human body? - A  ) Femur","Tibia","Stapes","Radius","Stapes")

    add_question("SCIENCE","0","Which type of electromagnetic radiation has the longest wavelength?","Gamma rays","X-rays","Ultraviolet","Radio waves","Radio waves")

    add_question("SCIENCE","0","What is the chemical formula for carbon dioxide?","CO","CO2","C2O","CO3","CO2")

    add_question("SCIENCE","0","What is the primary function of red blood cells?","Fight infections","Clot blood","Transport oxygen","Remove waste","Transport oxygen")

    add_question("SCIENCE","0","Which part of the eye controls the amount of light entering it?","Lens","Retina","Pupil","Cornea","Pupil")

    add_question("SCIENCE","0","What is the SI unit of temperature?","Celsius","Fahrenheit","Kelvin","Joule","Kelvin")

    add_question("SCIENCE","0","Which planet is known as the 'Evening Star'?","Mars","Venus","Jupiter","Saturn","Venus")

    add_question("SCIENCE","0","What is the most common type of rock on the Earth's surface?","Igneous","Sedimentary","Metamorphic","Basalt","Sedimentary")

    add_question("SCIENCE","0","Which vitamin is essential for blood clotting?","Vitamin A","Vitamin B","Vitamin C","Vitamin K","Vitamin K")

    add_question("SCIENCE","0","What is the most abundant mineral in the human body?","Potassium","Iron","Calcium","Sodium","Calcium")

    add_question("SCIENCE","0","Which gas is commonly known as laughing gas?","Nitrogen","Nitrous oxide","Carbon monoxide","Methane","Nitrous oxide")

    add_question("SCIENCE","0","What is the main organ involved in the circulatory system?","Liver","Lung","Heart","Kidney","Heart")

    add_question("SCIENCE","0","Which organelle is responsible for protein synthesis in the cell?","Lysosome","Mitochondria","Ribosome","Golgi apparatus","Ribosome")

    add_question("SCIENCE","0","What is the most common metal in the Earth's crust?","Iron","Aluminum","Copper","Zinc","Aluminum")

    add_question("SCIENCE","0","Which part of the brain is responsible for balance and coordination?","Cerebrum","Cerebellum","Medulla","Hypothalamus","Cerebellum")

    add_question("SCIENCE","0","What is the SI unit of electric current?","Volt","Ampere","Watt","Ohm","Ampere")

    add_question("SCIENCE","0","What is the main component of the sun?","Carbon","Oxygen","Hydrogen","Helium","Hydrogen")

    add_question("SCIENCE","0","Which acid is found in the stomach?","Hydrochloric acid","Sulfuric acid","Nitric acid","Acetic acid","Hydrochloric acid")

    add_question("SCIENCE","0","What is the chemical symbol for gold?","Gd","Ag","Au","Al","Au")

    add_question("SCIENCE","0","What is the term for animals that are active during the night?","Diurnal","Nocturnal","Crepuscular","Arboreal","Nocturnal")

    add_question("SCIENCE","0","Which planet has the most moons?","Mars","Earth","Jupiter","Saturn","Jupiter")

    add_question("SCIENCE","0","What is the most abundant gas in Earth's atmosphere?","Oxygen","Nitrogen","Argon","Carbon dioxide","Nitrogen")

    add_question("SCIENCE","0","Which substance is known as the universal solvent?","Alcohol","Ether","Water","Acetone","Water")

    add_question("SCIENCE","0","What is the smallest planet in our solar system?","Venus","Earth","Mars","Mercury","Mercury")

    add_question("SCIENCE","0","What is the powerhouse of the cell?","Ribosome","Nucleus","Mitochondria","Golgi apparatus","Mitochondria")

    add_question("SCIENCE","0","Which element is the primary component of diamonds?","Carbon","Silicon","Oxygen","Nitrogen","Carbon")

    add_question("SCIENCE","0","Which organ in the human body filters waste products from the blood?","Heart","Liver","Kidney","Lungs","Kidney")

    add_question("SCIENCE","0","What is the study of fungi called?","Zoology","Botany","Mycology","Ecology","Mycology")

    add_question("SCIENCE","0","Which vitamin is essential for the absorption of calcium?","Vitamin A","Vitamin C","Vitamin D","Vitamin E","Vitamin D")

    add_question("SCIENCE","0","What is the SI unit of pressure?","Joule","Pascal","Watt","Newton","Pascal")

    add_question("SCIENCE","0","What type of cell contains a nucleus?","Prokaryotic","Eukaryotic","Bacterial","Archaeal","Eukaryotic")

    add_question("SCIENCE","0","What is the name of the process by which plants lose water vapor?","Respiration","Transpiration","Photosynthesis","Fermentation","Transpiration")

    add_question("SCIENCE","0","Which gas is responsible for the greenhouse effect?","Nitrogen","Oxygen","Carbon Dioxide","Helium","Carbon Dioxide")

    add_question("SCIENCE","0","What is the most abundant element in the Earth's crust?","Oxygen","Silicon","Aluminum","Iron","Oxygen")

    add_question("SCIENCE","0","What is the atomic number of oxygen?","6","8","10","12","8")

    add_question("SCIENCE","0","Which metal is liquid at room temperature?","Iron","Mercury","Copper","Lead","Mercury")

    add_question("SCIENCE","0","Which part of the cell is responsible for controlling cell activities?","Nucleus","Cytoplasm","Ribosome","Mitochondria","Nucleus")

    add_question("SCIENCE","0","Which vitamin is known as the 'sunshine vitamin'?","Vitamin A","Vitamin B12","Vitamin C","Vitamin D","Vitamin D")

    add_question("SCIENCE","0","Which organelle is known as the 'suicide bag' of the cell?","Lysosome","Mitochondria","Nucleus","Golgi apparatus","Lysosome")

    add_question("SCIENCE","0","What is the process of cell division in which the chromosome number is halved?","Mitosis","Meiosis","Binary Fission","Budding","Meiosis")

    add_question("SCIENCE","0","What is the chemical formula for methane?","CH4","C2H6","C2H4","C3H8","CH4")

    add_question("SCIENCE","0","Which planet is known for its Great Red Spot?","Earth","Mars","Jupiter","Saturn","Jupiter")

    add_question("SCIENCE","0","Which hormone regulates blood sugar levels?","Adrenaline","Thyroxine","Insulin","Glucagon","Insulin")

    add_question("SCIENCE","0","What is the   SI unit of energy?","Watt","Volt","Joule","Ohm","Joule")

    add_question("SCIENCE","0","What type of rock is formed from cooling magma?","Sedimentary","Metamorphic","Igneous","Basalt","Igneous")

    add_question("SCIENCE","0","Which planet is the hottest in the solar system?","Mercury","Venus","Mars","Jupiter","Venus")

    add_question("SCIENCE","0","What is the most common isotope of hydrogen?","Deuterium","Tritium","Protium","Helium-3","Protium")

    add_question("SCIENCE","0","Which type of bond is formed between a metal and a non-metal?","Covalent bond","Ionic bond","Hydrogen bond","Van der Waals bond","Ionic bond")

    add_question("SCIENCE","0","Which part of the plant is responsible for absorbing water and nutrients?","Stem","Leaf","Root","Flower","Root")

    add_question("SCIENCE","0","What is the largest artery in the human body?","Carotid artery","Femoral artery","Pulmonary artery","Aorta","Aorta")

    add_question("SCIENCE","0","Which gas is released during photosynthesis?","Oxygen","Carbon Dioxide","Nitrogen","Hydrogen","Oxygen")

    add_question("SCIENCE","0","What is the boiling point of water in Fahrenheit?","32°F","100°F","180°F","212°F","212°F")

    add_question("SCIENCE","0","Which part of the human brain controls voluntary movements?","Medulla oblongata","Cerebellum","Cerebrum","Hypothalamus","Cerebrum")

    add_question("SCIENCE","0","What is the chemical formula for table salt?","NaCl","KCl","NaOH","HCl","NaCl")

    add_question("SCIENCE","0","Which planet has the most extensive ring system?","Jupiter","Uranus","Neptune","Saturn","Saturn")

    add_question("SCIENCE","0","What is the most reactive metal?","Sodium","Potassium","Calcium","Magnesium","Potassium")

    add_question("SCIENCE","0","What is the SI unit of time?","Minute","Second","Hour","Day","Second")

    add_question("SCIENCE","0","  0. What is the process by which plants convert sunlight into food?","Photosynthesis","Respiration","Fermentation","Transpiration","Photosynthesis") 
        

    add_question("POLITY","0","भारतीय संविधान में कितनी मूलभूत अधिकारों की व्यवस्था है?","4","6","8","10","6")

    add_question("POLITY","0","संविधान के किस अनुच्छेद में संसद के संशोधन का प्रावधान है?","अनुच्छेद 356","अनुच्छेद 368","अनुच्छेद 370","अनुच्छेद 352","अनुच्छेद 368")

    add_question("POLITY","0","भारतीय संविधान का कौन सा भाग 'मूलभूत अधिकारों' से संबंधित है?","भाग III","भाग IV","भाग V","भाग VI","भाग III")

    add_question("POLITY","0","राष्ट्रपति के द्वारा नियुक्त होने वाले उच्चतम न्यायालय के न्यायाधीशों की आयु सीमा क्या है?","60 वर्ष","62 वर्ष","65 वर्ष","70 वर्ष","65 वर्ष")

    add_question("POLITY","0","भारतीय संविधान की प्रस्तावना में निम्नलिखित में से कौन सा शब्द जोड़ा गया था?","पंथनिरपेक्ष","समाजवादी","धर्मनिरपेक्ष","सभी","सभी")

    add_question("POLITY","0","राज्य सभा के सदस्यों का कार्यकाल कितना होता है?","4 वर्ष","5 वर्ष","6 वर्ष","7 वर्ष","6 वर्ष")

    add_question("POLITY","0","संविधान की आठवीं अनुसूची में कितनी भाषाओं का उल्लेख है?","14","18","22","25","22")

    add_question("POLITY","0","भारत के राष्ट्रपति का निर्वाचन किसके द्वारा होता है?","जनता के द्वारा","संसद के द्वारा","निर्वाचन मंडल के द्वारा","विधानमंडल के द्वारा","निर्वाचन मंडल के द्वारा")

    add_question("POLITY","0","भारतीय संविधान में संघ सूची में कितने विषय हैं?","52","66","97","100","97")

    add_question("POLITY","0","भारतीय संविधान के अनुसार, राज्यपाल की नियुक्ति कौन करता है?","राष्ट्रपति","प्रधानमंत्री","सर्वोच्च न्यायालय","मुख्यमंत्री","राष्ट्रपति")

    add_question("POLITY","0","संविधान के किस अनुच्छेद के तहत आपातकाल की घोषणा की जा सकती है?","अनुच्छेद 352","अनुच्छेद 356","अनुच्छेद 360","अनुच्छेद 370","अनुच्छेद 352")

    add_question("POLITY","0","भारतीय संसद के कितने सदन हैं?","1","2","3","4","2")

    add_question("POLITY","0","संविधान का कौन सा अनुच्छेद मौलिक कर्तव्यों की व्याख्या करता है?","अनुच्छेद 14","अनुच्छेद 21","अनुच्छेद 51A","अनुच्छेद 32","अनुच्छेद 51A")

    add_question("POLITY","0","भारत के उपराष्ट्रपति का कार्यकाल कितने वर्षों का होता है?","4 वर्ष","5 वर्ष","6 वर्ष","7 वर्ष","5 वर्ष")

    add_question("POLITY","0","भारतीय संसद का संयुक्त सत्र किसके द्वारा बुलाया जाता है?","प्रधानमंत्री","राष्ट्रपति","लोकसभा अध्यक्ष","राज्यसभा अध्यक्ष","राष्ट्रपति")

    add_question("POLITY","0","संविधान के किस अनुच्छेद के तहत 'राज्य के नीति निर्देशक सिद्धांतों' का उल्लेख किया गया है?","अनुच्छेद 36-51","अनुच्छेद 19-22","अनुच्छेद 14-18","अनुच्छेद 32-35","अनुच्छेद 36-51")

    add_question("POLITY","0","भारत के किस संविधान संशोधन ने 'न्यायिक पुनर्विचार' की शक्ति को कमजोर किया?","24वां संशोधन","42वां संशोधन","44वां संशोधन","52वां संशोधन","42वां संशोधन")

    add_question("POLITY","0","भारतीय संविधान में नागरिकता के अधिकारों का उल्लेख किस अनुच्छेद में है?","अनुच्छेद 5-11","अनुच्छेद 12-35","अनुच्छेद 36-51","अनुच्छेद 52-151","अनुच्छेद 5-11")

    add_question("POLITY","0","भारतीय संविधान का कौन सा अनुच्छेद 'समानता का अधिकार' प्रदान करता है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 32","अनुच्छेद 14")

    add_question("POLITY","0","'राज्य का प्रधान' किसे कहा जाता है?","प्रधानमंत्री","मुख्यमंत्री","राज्यपाल","राष्ट्रपति","राष्ट्रपति")

    add_question("POLITY","0","'भारतीय संविधान के किस अनुच्छेद में राज्यपाल को अध्यादेश जारी करने का अधिकार दिया गया है?","अनुच्छेद 123","अनुच्छेद 213","अनुच्छेद 356","अनुच्छेद 370","अनुच्छेद 213")

    add_question("POLITY","0","संविधान के किस भाग में 'संघ एवं राज्य के बीच संबंध' का वर्णन है?","भाग VIII","भाग X","भाग XI","भाग XII","भाग XI")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद में 'स्वतंत्रता का अधिकार' दिया गया है?","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 23","अनुच्छेद 32","अनुच्छेद 19")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मुफ्त और अनिवार्य शिक्षा' का प्रावधान है?","अनुच्छेद 21A","अनुच्छेद 45","अनुच्छेद 51A","अनुच्छेद 14","अनुच्छेद 21A")

    add_question("POLITY","0","संविधान के किस भाग में 'राज्यों के लिए नीति निर्देशक सिद्धांत' का वर्णन है?","भाग III","भाग IV","भाग V","भाग VI","भाग IV")

    add_question("POLITY","0","भारतीय संविधान के अनुसार, संविधान सभा के अध्यक्ष कौन थे?","डॉ. भीमराव अंबेडकर","डॉ. राजेंद्र प्रसाद","जवाहरलाल नेहरू","सरदार पटेल","डॉ. राजेंद्र प्रसाद")

    add_question("POLITY","0","'महिला और बाल कल्याण' से संबंधित प्रावधान भारतीय संविधान के किस अनुच्छेद में है?","अनुच्छेद 15","अनुच्छेद 21","अनुच्छेद 39","अनुच्छेद 51A","अनुच्छेद 39")

    add_question("POLITY","0","किस संविधान संशोधन ने पंचायतों और नगरपालिकाओं को संवैधानिक दर्जा प्रदान किया?","42वां संशोधन","44वां संशोधन","73वां संशोधन","86वां संशोधन","73वां संशोधन")

    add_question("POLITY","0","भारत के संविधान में 'मूल संरचना सिद्धांत' किसने स्थापित किया?","गोलकनाथ बनाम पंजाब राज्य मामला","केशवानंद भारती बनाम केरल राज्य मामला","इंदिरा गांधी बनाम राज नारायण मामला","मिनर्वा मिल्स मामला","केशवानंद भारती बनाम केरल राज्य मामला")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद में 'जीवन और व्यक्तिगत स्वतंत्रता का अधिकार' दिया गया है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 32 - **सही उत्तर:   C) अनुच्छेद 21")

    add_question("POLITY","0","किस संविधान संशोधन के तहत 'लोकपाल और लोकायुक्त' की स्थापना की गई थी?","42वां संशोधन","44वां संशोधन","73वां संशोधन","97वां संशोधन","97वां संशोधन")

    add_question("POLITY","0","भारतीय संविधान का कौन सा भाग 'संविधान के संशोधन' से संबंधित है?","भाग IX","भाग XI","भाग XII","भाग XX","भाग XX")

    add_question("POLITY","0","किस अनुच्छेद के तहत 'राष्ट्रपति शासन' की घोषणा की जा सकती है?","अनुच्छेद 352","अनुच्छेद 356","अनुच्छेद 360","अनुच्छेद 368","अनुच्छेद 356")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संपत्ति का अधिकार' हटाया गया था?","अनुच्छेद 19","अनुच्छेद 31","अनुच्छेद 32","अनुच्छेद 44","अनुच्छेद 31")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद में 'उचित प्रक्रिया का अधिकार' दिया गया है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 32","अनुच्छेद 21")

    add_question("POLITY","0","भारतीय संविधान में 'पंचायती राज' से संबंधित प्रावधान किस भाग में दिए गए हैं?","भाग IX","भाग XI","भाग XII","भाग XIV","भाग IX")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद में 'संवैधानिक उपचारों का अधिकार' दिया गया है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 32","अनुच्छेद 32")

    add_question("POLITY","0","संविधान के किस अनुच्छेद के तहत संसद को 'विशेष राज्य' का दर्जा देने का अधिकार है?","अनुच्छेद 275","अनुच्छेद 371","अनुच्छेद 356","अनुच्छेद 368","अनुच्छेद 371")

    add_question("POLITY","0","भारतीय संविधान का कौन सा अनुच्छेद 'राष्ट्रपति के कर्तव्यों' का वर्णन करता है?","अनुच्छेद 53","अनुच्छेद 54","अनुच्छेद 61","अनुच्छेद 74","अनुच्छेद 53")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'राष्ट्रपति को क्षमादान का अधिकार' प्राप्त है?","अनुच्छेद 61","अनुच्छेद 72","अनुच्छेद 74","अनुच्छेद 76","अनुच्छेद 72")

    add_question("POLITY","0","किस अनुच्छेद के तहत 'पारदर्शिता और जवाबदेही' का प्रावधान किया गया है?","अनुच्छेद 19(1)(a)","अनुच्छेद 21","अनुच्छेद 25","अनुच्छेद 51A(h)","अनुच्छेद 51A(h)")

    add_question("POLITY","0","किस संविधान संशोधन ने 'आरक्षण' के प्रावधान को संवैधानिक दर्जा दिया?","42वां संशोधन","44वां संशोधन","93वां संशोधन","97वां संशोधन","93वां संशोधन")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'अल्पसंख्यक अधिकारों' की सुरक्षा की जाती है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 29-30","अनुच्छेद 29-30")

    add_question("POLITY","0","संविधान के किस अनुच्छेद के तहत 'समानता के अधिकार' का प्रावधान है?","अनुच्छेद 14","अनुच्छेद 16","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 14")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'समान अवसर' का प्रावधान है?","अनुच्छेद 14","अनुच्छेद 16","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 16")

    add_question("POLITY","0","संविधान के किस अनुच्छेद के तहत 'संवैधानिक उपचार' का अधिकार है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 32","अनुच्छेद 21","अनुच्छेद 32")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'आपातकाल की घोषणा' की जाती है?","अनुच्छेद 352","अनुच्छेद 356","अनुच्छेद 360","अनुच्छेद 368","अनुच्छेद 352")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'धर्म की स्वतंत्रता' का अधिकार दिया गया है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 25-28","अनुच्छेद 25-28")

    add_question("POLITY","0","किस संविधान संशोधन के तहत 'शिक्षा का अधिकार' अनिवार्य किया गया?","42वां संशोधन","44वां संशोधन","86वां संशोधन","93वां संशोधन","86वां संशोधन")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'भारतीय नागरिकता' का प्रावधान है?","अनुच्छेद 5-11","अनुच्छेद 12-35","अनुच्छेद 36-51","अनुच्छेद 52-151","अनुच्छेद 5-11")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संवैधानिक संशोधन' का अधिकार है?","अनुच्छेद 356","अनुच्छेद 368","अनुच्छेद 352","अनुच्छेद 370","अनुच्छेद 368")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संसदीय शासन व्यवस्था' का प्रावधान है?","अनुच्छेद 52-78","अनुच्छेद 79-122","अनुच्छेद 123-151","अनुच्छेद 152-237","अनुच्छेद 52-78")

    add_question("POLITY","0","संविधान के किस अनुच्छेद के तहत 'राष्ट्रपति के कर्तव्य और कार्य' का प्रावधान है?","अनुच्छेद 53","अनुच्छेद 54","अनुच्छेद 56","अनुच्छेद 61","अनुच्छेद 53")

    add_question("POLITY","0","किस अनुच्छेद के तहत 'उप-राष्ट्रपति का निर्वाचन' किया जाता है?","अनुच्छेद 54","अनुच्छेद 56","अनुच्छेद 63","अनुच्छेद 67","अनुच्छेद 63")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मौलिक कर्तव्यों' का वर्णन है?","अनुच्छेद 14","अनुच्छेद 21","अनुच्छेद 51A","अनुच्छेद 32","अनुच्छेद 51A")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मुफ्त कानूनी सहायता' का प्रावधान है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 39A","अनुच्छेद 39A")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संघ और राज्य के बीच संबंध' का वर्णन है?","अनुच्छेद 256-263","अनुच्छेद 264-293  ","अनुच्छेद 294-300","अनुच्छेद 301-307","अनुच्छेद 256-263")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'राष्ट्रपति शासन' का प्रावधान है?","अनुच्छेद 352","अनुच्छेद 356","अनुच्छेद 360","अनुच्छेद 368","अनुच्छेद 356")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'समानता का अधिकार' दिया गया है?","अनुच्छेद 14-18","अनुच्छेद 19-22","अनुच्छेद 23-24","अनुच्छेद 25-28","अनुच्छेद 14-18")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संसदीय लोकतंत्र' का प्रावधान है?","अनुच्छेद 52","अनुच्छेद 79","अनुच्छेद 124","अनुच्छेद 152","अनुच्छेद 79")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संसद की शक्तियों' का प्रावधान है?","अनुच्छेद 79-122","अनुच्छेद 123-151","अनुच्छेद 152-237","अनुच्छेद 238-242","अनुच्छेद 79-122")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संवैधानिक संशोधन' का प्रावधान है?","अनुच्छेद 352","अनुच्छेद 356","अनुच्छेद 368","अनुच्छेद 370","अनुच्छेद 368")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संविधान के मौलिक अधिकार' का वर्णन है?","अनुच्छेद 12-35","अनुच्छेद 36-51","अनुच्छेद 52-78","अनुच्छेद 79-122","अनुच्छेद 12-35")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'राज्य नीति निर्देशक सिद्धांत' का प्रावधान है?","अनुच्छेद 36-51","अनुच्छेद 52-78","अनुच्छेद 79-122","अनुच्छेद 123-151","अनुच्छेद 36-51")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मौलिक अधिकारों' का प्रावधान है?","अनुच्छेद 14-18","अनुच्छेद 19-22","अनुच्छेद 23-24","अनुच्छेद 25-28","अनुच्छेद 19-22")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'नागरिकता' का प्रावधान है?","अनुच्छेद 5-11","अनुच्छेद 12-35","अनुच्छेद 36-51","अनुच्छेद 52-151","अनुच्छेद 5-11")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मौलिक अधिकारों' का प्रावधान है?","अनुच्छेद 14-18","अनुच्छेद 19-22","अनुच्छेद 23-24","अनुच्छेद 25-28","अनुच्छेद 14-18")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मुफ्त कानूनी सहायता' का प्रावधान है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 39A","अनुच्छेद 39A")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संवैधानिक उपचार' का अधिकार है?","अनुच्छेद 32","अनुच्छेद 21","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 32")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'धर्म की स्वतंत्रता' का अधिकार दिया गया है?","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 25-28","अनुच्छेद 25-28")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संविधान संशोधन' का प्रावधान है?","अनुच्छेद 368","अनुच्छेद 352","अनुच्छेद 356","अनुच्छेद 370","अनुच्छेद 368")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मौलिक कर्तव्यों' का प्रावधान है?","अनुच्छेद 51A","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 32","अनुच्छेद 51A")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मुफ्त और अनिवार्य शिक्षा' का प्रावधान है?","अनुच्छेद 21A","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 32","अनुच्छेद 21A")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'धर्म की स्वतंत्रता' का अधिकार दिया गया है?","अनुच्छेद 25-28","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 25-28")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संविधान संशोधन' का प्रावधान है?","अनुच्छेद 368","अनुच्छेद 352","अनुच्छेद 356","अनुच्छेद 370","अनुच्छेद 368")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'राज्य के नीति निर्देशक सिद्धांत' का प्रावधान है?","अनुच्छेद 36-51","अनुच्छेद 52-78","अनुच्छेद 79-122","अनुच्छेद 123-151","अनुच्छेद 36-51")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संसदीय शासन व्यवस्था' का प्रावधान है?","अनुच्छेद 79-122","अनुच्छेद 123-151","अनुच्छेद 152-237","अनुच्छेद 238-242","अनुच्छेद 79-122")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मौलिक अधिकारों' का प्रावधान है?","अनुच्छेद 14-18","अनुच्छेद 19-22","अनुच्छेद 23-24","अनुच्छेद 25-28","अनुच्छेद 14-18")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मौलिक कर्तव्यों' का प्रावधान है?","अनुच्छेद 51A","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 32","अनुच्छेद 51A")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'मुफ्त कानूनी सहायता' का प्रावधान है?","अनुच्छेद 39A","अनुच्छेद 14","अनुच्छेद 19","अनुच्छेद 21","अनुच्छेद 39A")

    add_question("POLITY","0","भारतीय संविधान के किस अनुच्छेद के तहत 'संविधान संशोधन' का प्रावधान है?","अनुच्छेद 368","अनुच्छेद 352","अनुच्छेद 356","अनुच्छेद 370","अनुच्छेद 368")
    
    add_question("HISTORY","0","Who was the founder of the Maurya Dynasty?","Chandragupta Maurya","Ashoka","Bindusara","Harshavardhana","Chandragupta Maurya")

    add_question("HISTORY","0","The Battle of Plassey was fought in which year?","1757","1761","1776","1782","1757")

    add_question("HISTORY","0","Who was the first Sultan of Delhi?","Qutb-ud-din Aibak","Iltutmish","Alauddin Khilji","Balban","Qutb-ud-din Aibak")

    add_question("HISTORY","0","The Treaty of Versailles ended which war?","World War I","World War II","The Crimean War","The Franco-Prussian War","World War I")

    add_question("HISTORY","0","Who is known as the 'Napoleon of India'?","Chandragupta Maurya","Ashoka","Samudragupta","Harshavardhana","Samudragupta")

    add_question("HISTORY","0","Who was the last Mughal Emperor of India?","Bahadur Shah Zafar","Akbar II","Shah Alam II","Aurangzeb","Bahadur Shah Zafar")

    add_question("HISTORY","0","Who was the first woman to become the President of the Indian National Congress?","Annie Besant","Sarojini Naidu","Vijayalakshmi Pandit","Indira Gandhi","Annie Besant")

    add_question("HISTORY","0","The 'Sepoy Mutiny' of 1857 is also known as?","First War of Indian Independence","Revolt of 1857","Indian Mutiny","All of the above","All of the above")

    add_question("HISTORY","0","Who was the founder of the Gupta Empire?","Chandragupta I","Samudragupta","Skandagupta","Chandragupta II","Chandragupta I")

    add_question("HISTORY","0","The Ajanta Caves were built during the reign of which dynasty?","Maurya","Gupta","Satavahana","Chalukya","Satavahana")

    add_question("HISTORY","0","Who was the first Governor-General of India?","Warren Hastings","Lord Dalhousie","Lord Curzon","Lord Mountbatten","Warren Hastings")

    add_question("HISTORY","0","The Indus Valley Civilization is also known as?","Harappan Civilization","Vedic Civilization","Aryan Civilization","Dravidian Civilization","Harappan Civilization")

    add_question("HISTORY","0","Who built the famous Kailasa temple at Ellora?","Krishna I","Raja Raja Chola","Harshavardhana","Narasimhavarman I","Krishna I")

    add_question("HISTORY","0","Who among the following was the first British Governor-General of Bengal?","Robert Clive","Warren Hastings","Lord Cornwallis","Lord Wellesley","Warren Hastings")

    add_question("HISTORY","0","Who wrote the book 'Arthashastra'?","Kautilya","Megasthenes","Kalidasa","Vishnu Sharma","Kautilya")

    add_question("HISTORY","0","The Battle of Panipat was fought between which two armies?","Babur and Ibrahim Lodi","Akbar and Rana Sanga","Aurangzeb and Dara Shikoh","Shivaji and Afzal Khan","Babur and Ibrahim Lodi")

    add_question("HISTORY","0","Which Indian freedom fighter was known as the 'Frontier Gandhi'?","Khan Abdul Ghaffar Khan","Maulana Abul Kalam Azad","Lala Lajpat Rai","Bal Gangadhar Tilak","Khan Abdul Ghaffar Khan")

    add_question("HISTORY","0","The Mughal Empire was founded by which ruler?","Babur","Akbar","Humayun","Shah Jahan","Babur")

    add_question("HISTORY","0","The 'Dandi March' was led by which Indian leader?","Mahatma Gandhi","Jawaharlal Nehru","Subhas Chandra Bose","Sardar Vallabhbhai Patel","Mahatma Gandhi")

    add_question("HISTORY","0","Who was the founder of the Vijayanagara Empire?","Harihara and Bukka","Krishnadevaraya","Rajaraja Chola","Pulakesin II","Harihara and Bukka")

    add_question("HISTORY","0","Who was the first Emperor of the Mughal Empire to rule over most of the Indian subcontinent?","Akbar","Babur","Humayun","Shah Jahan","Akbar")

    add_question("HISTORY","0","The Ashokan Edicts are written in which script?","Brahmi","Devanagari","Kharosthi","Greek","Brahmi")

    add_question("HISTORY","0","Who was the author of 'Rajatarangini', a historical chronicle of Kashmir?","Kalhana","Banabhatta","Harsha","Kalidasa","Kalhana")

    add_question("HISTORY","0","Which Sultan of Delhi founded the city of Agra?","Sikandar Lodi","Ibrahim Lodi","Alauddin Khilji","Muhammad bin Tughlaq","Sikandar Lodi")

    add_question("HISTORY","0","Who was the first Indian ruler to accept the Subsidiary Alliance of the British?","Nizam of Hyderabad","Tipu Sultan","Marathas","Nawab of Bengal","Nizam of Hyderabad")

    add_question("HISTORY","0","The Simon Commission was boycotted by Indians because it:","Did not include any Indian member","Was headed by a British","Was meant to suppress Indian nationalism","Was related to the partition of Bengal","Did not include any Indian member")

    add_question("HISTORY","0","Who was the founder of the Indian National Army (INA)?","Subhas Chandra Bose","Mohan Singh","Rash Behari Bose","Bhagat Singh","Mohan Singh")

    add_question("HISTORY","0","Which Indian ruler defeated Seleucus Nicator?","Chandragupta Maurya","Bindusara","Ashoka","Kanishka","Chandragupta Maurya")

    add_question("HISTORY","0","The Second Battle of Tarain was fought between?","Prithviraj Chauhan and Muhammad Ghori","Akbar and Rana Pratap","Babur and Rana Sanga","Ahmad Shah Abdali and Marathas","Prithviraj Chauhan and Muhammad Ghori")

    add_question("HISTORY","0","Who was the first Indian woman to become the Governor of an Indian state?","Sarojini Naidu","Indira Gandhi","Vijayalakshmi Pandit","Sucheta Kripalani","Sarojini Naidu")

    add_question("HISTORY","0","Who was the first person to circumnavigate the Earth?","Ferdinand Magellan","Christopher Columbus","Vasco da Gama","Marco Polo","Ferdinand Magellan")

    add_question("HISTORY","0","Who was the first Indian to be elected to the British Parliament?","Dadabhai Naoroji","M.K. Gandhi","B.R. Ambedkar","Jawaharlal Nehru","Dadabhai Naoroji")

    add_question("HISTORY","0","The 'Quit India Movement' was launched in which year?","1942","1930","1920","1919","1942")

    add_question("HISTORY","0","Who among the following was the   founder of the Arya Samaj?","Swami Dayananda Saraswati","Swami Vivekananda","Raja Ram Mohan Roy","Ramakrishna Paramahamsa","Swami Dayananda Saraswati")

    add_question("HISTORY","0","Who was the Viceroy of India during the partition of Bengal in 1905?","Lord Curzon","Lord Minto","Lord Ripon","Lord Lytton","Lord Curzon")

    add_question("HISTORY","0","The Battle of Buxar was fought in which year?","1764","1757","1773","1784","1764")

    add_question("HISTORY","0","Who is known as the 'Father of Indian Renaissance'?","Raja Ram Mohan Roy","Swami Vivekananda","Bal Gangadhar Tilak","Rabindranath Tagore","Raja Ram Mohan Roy")

    add_question("HISTORY","0","Who was the last Viceroy of British India?","Lord Mountbatten","Lord Wavell","Lord Linlithgow","Lord Curzon","Lord Mountbatten")

    add_question("HISTORY","0","The 'Ryotwari System' was introduced by which British official?","Thomas Munro","Lord Cornwallis","Lord Curzon","Warren Hastings","Thomas Munro")

    add_question("HISTORY","0","Who was the founder of the Chola Empire?","Vijayalaya Chola","Rajaraja Chola I","Rajendra Chola","Kulottunga Chola I","Vijayalaya Chola")

    add_question("HISTORY","0","Who among the following led the Salt Satyagraha in Tamil Nadu?","C. Rajagopalachari","K. Kamaraj","V. O. Chidambaram Pillai","Periyar E. V. Ramasamy","C. Rajagopalachari")

    add_question("HISTORY","0","Which freedom fighter was known as the 'Lion of Punjab'?","Lala Lajpat Rai","Bhagat Singh","Udham Singh","Bal Gangadhar Tilak","Lala Lajpat Rai")

    add_question("HISTORY","0","The capital of the Pallava dynasty was?","Kanchipuram","Madurai","Thanjavur","Mysore","Kanchipuram")

    add_question("HISTORY","0","The First Anglo-Maratha War resulted in which treaty?","Treaty of Salbai","Treaty of Purandar","Treaty of Bassein","Treaty of Seringapatam","Treaty of Salbai")

    add_question("HISTORY","0","Who among the following was the architect of the Indian Constitution?","B.R. Ambedkar","Jawaharlal Nehru","Sardar Vallabhbhai Patel","Mahatma Gandhi","B.R. Ambedkar")

    add_question("HISTORY","0","The Non-Cooperation Movement was withdrawn after which incident?","Jallianwala Bagh Massacre","Chauri Chaura Incident","Simon Commission Arrival","Dandi March","Chauri Chaura Incident")

    add_question("HISTORY","0","Who was the first Indian to win a Nobel Prize?","Rabindranath Tagore","C.V. Raman","Amartya Sen","Mother Teresa","Rabindranath Tagore")

    add_question("HISTORY","0","Who was the leader of the 1857 Revolt in Lucknow?","Begum Hazrat Mahal","Rani Lakshmibai","Tantia Tope","Nana Sahib","Begum Hazrat Mahal")

    add_question("HISTORY","0","The All India Muslim League was founded in which year?","1906","1905","1911","1916","1906")

    add_question("HISTORY","0","The famous slogan 'Jai Hind' was given by which Indian leader?","Subhas Chandra Bose","Mahatma Gandhi","Bhagat Singh","Jawaharlal Nehru","Subhas Chandra Bose")    
    add_question("GEOGRAPHY","0","सबसे बड़ा महाद्वीप कौन सा है?","अफ्रीका","एशिया","यूरोप","उत्तरी अमेरिका","एशिया")

    add_question("GEOGRAPHY","0","भारत में सबसे लंबी नदी कौन सी है?","यमुना","गंगा","गोदावरी","ब्रह्मपुत्र","गंगा")

    add_question("GEOGRAPHY","0","सतह से सबसे ऊंचा पर्वत कौन सा है?","माउंट एवरेस्ट","कंचनजंगा","नंदा देवी","धौलागिरी","माउंट एवरेस्ट")

    add_question("GEOGRAPHY","0","भारत का सबसे बड़ा राज्य क्षेत्रफल के हिसाब से कौन सा है?","उत्तर प्रदेश","राजस्थान","महाराष्ट्र","मध्य प्रदेश","राजस्थान")

    add_question("GEOGRAPHY","0","निम्नलिखित में से कौन सा देश भूमध्य रेखा को नहीं छूता है?","ब्राज़ील","इंडोनेशिया","भारत","केन्या","भारत")

    add_question("GEOGRAPHY","0","हिमालय पर्वत किस प्रकार की पर्वत श्रेणी है?","ज्वालामुखीय","वलित","अवशिष्ट","चट्टानी","वलित")

    add_question("GEOGRAPHY","0","सवाना घास के मैदान किस महाद्वीप में पाए जाते हैं?","एशिया","अफ्रीका","दक्षिण अमेरिका","ऑस्ट्रेलिया","अफ्रीका")

    add_question("GEOGRAPHY","0","दुनिया का सबसे बड़ा रेगिस्तान कौन सा है?","सहारा","गोबी","कालाहारी","अंटार्कटिका","सहारा")

    add_question("GEOGRAPHY","0","‘ब्लू प्लैनेट’ किस ग्रह का उपनाम है?","मंगल","शनि","पृथ्वी","शुक्र","पृथ्वी")

    add_question("GEOGRAPHY","0","दुनिया की सबसे लंबी नदी कौन सी है?","अमेज़न","नील","यांग्त्ज़ी","मिसिसिपी","नील")

    add_question("GEOGRAPHY","0","निम्नलिखित में से कौन सा महासागर सबसे छोटा है?","हिंद महासागर","प्रशांत महासागर","अटलांटिक महासागर","आर्कटिक महासागर","आर्कटिक महासागर")

    add_question("GEOGRAPHY","0","‘ग्रीनलैंड’ किस देश का हिस्सा है?","नॉर्वे","डेनमार्क","कनाडा","आइसलैंड","डेनमार्क")

    add_question("GEOGRAPHY","0","भारत का सबसे दक्षिणी बिंदु कौन सा है?","कन्याकुमारी","इंदिरा पॉइंट","रामेश्वरम","लक्षद्वीप","इंदिरा पॉइंट")

    add_question("GEOGRAPHY","0","‘रूरलैंड’ किस देश का प्रमुख कृषि क्षेत्र है?","संयुक्त राज्य अमेरिका","ब्राजील","रूस","फ्रांस","संयुक्त राज्य अमेरिका")

    add_question("GEOGRAPHY","0","भारत के पश्चिमी तट पर स्थित द्वीप समूह कौन सा है?","अंडमान और निकोबार","लक्षद्वीप","मिनिकॉय","वेलिन","लक्षद्वीप")

    add_question("GEOGRAPHY","0","‘विज्ञान की जननी’ किस नदी को कहा जाता है?","गंगा","सिंधु","नील","तिबर","सिंधु")

    add_question("GEOGRAPHY","0","निम्नलिखित में से कौन सा राज्य भारत का ‘चावल का कटोरा’ कहा जाता है?","पंजाब","पश्चिम बंगाल","तमिलनाडु","छत्तीसगढ़","छत्तीसगढ़")

    add_question("GEOGRAPHY","0","'माउंट कोसियास्को' किस देश की सबसे ऊंची चोटी है?","ऑस्ट्रेलिया","न्यूजीलैंड","दक्षिण अफ्रीका","अर्जेंटीना","ऑस्ट्रेलिया")

    add_question("GEOGRAPHY","0","दुनिया का सबसे बड़ा महासागर कौन सा है?","अटलांटिक महासागर","हिंद महासागर","प्रशांत महासागर","दक्षिणी महासागर","प्रशांत महासागर")

    add_question("GEOGRAPHY","0","‘लाल सागर’ के पानी का रंग लाल क्यों दिखता है?","लाल शैवाल के कारण","मिट्टी के कारण","सूर्य की किरणों के कारण","लाल मछलियों के कारण","लाल शैवाल के कारण")

    add_question("GEOGRAPHY","0","पृथ्वी का कौन सा महाद्वीप सबसे छोटा है?","एशिया","यूरोप","ऑस्ट्रेलिया","अंटार्कटिका","ऑस्ट्रेलिया")

    add_question("GEOGRAPHY","0","किस राज्य में 'सरदार सरोवर बांध' स्थित है?","महाराष्ट्र","गुजरात","मध्य प्रदेश","राजस्थान","गुजरात")

    add_question("GEOGRAPHY","0","भारत के किस राज्य में सबसे ज्यादा चाय का उत्पादन होता है?","केरल","तमिलनाडु","असम","पश्चिम बंगाल","असम")

    add_question("GEOGRAPHY","0","दुनिया का सबसे बड़ा द्वीप कौन सा है?","ग्रीनलैंड","न्यू गिनी","बोरनियो","मेडागास्कर","ग्रीनलैंड")

    add_question("GEOGRAPHY","0","'ग्रेट बैरियर रीफ' किस देश के तट के पास स्थित है?","ऑस्ट्रेलिया","ब्राज़ील","भारत","दक्षिण अफ्रीका","ऑस्ट्रेलिया")

    add_question("GEOGRAPHY","0","विश्व का सबसे बड़ा सक्रिय ज्वालामुखी कौन सा है?","माउंट विसुवियस","माउंट सेंट हेलेंस","मौना लोआ","माउंट एटना","मौना लोआ")

    add_question("GEOGRAPHY","0","‘नर्मदा नदी’ कहाँ से निकलती है?","अमरकंटक","विंध्याचल","सतपुड़ा","अरावली","अमरकंटक")

    add_question("GEOGRAPHY","0","'साहरा मरुस्थल' किस महाद्वीप में स्थित है?","एशिया","अफ्रीका","ऑस्ट्रेलिया","दक्षिण अमेरिका","अफ्रीका")

    add_question("GEOGRAPHY","0","‘शून्य रेखा’ किसे कहा जाता है?","भूमध्य रेखा","ग्रीनविच मीन टाइम","कर्क रेखा","मकर रेखा","भूमध्य रेखा")

    add_question("GEOGRAPHY","0","दुनिया के सबसे ऊंचे झरने का नाम क्या है?","नियाग्रा फॉल्स","एंजल फॉल्स","विक्टोरिया फॉल्स","जोग फॉल्स","एंजल फॉल्स")

    add_question("GEOGRAPHY","0","भारत का कौन सा राज्य ‘झीलों का शहर’ के नाम से जाना जाता है?","राजस्थान","उत्तराखंड","जम्मू और कश्मीर","केरल","राजस्थान")

    add_question("GEOGRAPHY","0","किस ग्रह को ‘लाल ग्रह’ कहा जाता है?","बुध","मंगल","शनि","शुक्र","मंगल")

    add_question("GEOGRAPHY","0","‘हिमालय पर्वत श्रृंखला’ में सबसे ऊंची चोटी कौन सी है?","माउंट एवरेस्ट","नंगा पर्वत","माउंट कंचनजंगा - D  ) माउंट धौलागिरी","माउंट एवरेस्ट")

    add_question("GEOGRAPHY","0","भारतीय उपमहाद्वीप का सबसे बड़ा द्वीप कौन सा है?","श्रीलंका","मालदीव","अंडमान और निकोबार","लक्षद्वीप","श्रीलंका")

    add_question("GEOGRAPHY","0","‘तिब्बत का पठार’ किस महाद्वीप में स्थित है?","एशिया","यूरोप","अफ्रीका","उत्तरी अमेरिका","एशिया")

    add_question("GEOGRAPHY","0","किस पर्वत को ‘आल्प्स का सिरमौर’ कहा जाता है?","माउंट एलब्रुस","माउंट मेटरहॉर्न","माउंट ब्लैंक","माउंट किलिमंजारो","माउंट ब्लैंक")

    add_question("GEOGRAPHY","0","कौन सी नदी ‘भारत की जीवन रेखा’ मानी जाती है?","गंगा","यमुना","गोदावरी","नर्मदा","गंगा")

    add_question("GEOGRAPHY","0","किस राज्य में ‘काजीरंगा राष्ट्रीय उद्यान’ स्थित है?","पश्चिम बंगाल","असम","ओडिशा","मिजोरम","असम")

    add_question("GEOGRAPHY","0","दक्षिण अफ्रीका का कौन सा शहर ‘सोने का शहर’ कहलाता है?","जोहान्सबर्ग","केपटाउन","डरबन","प्रिटोरिया","जोहान्सबर्ग")

    add_question("GEOGRAPHY","0","कौन सा महासागर ‘हिंद महासागर’ से नहीं जुड़ा हुआ है?","अटलांटिक महासागर","प्रशांत महासागर","आर्कटिक महासागर","दक्षिणी महासागर","आर्कटिक महासागर")

    add_question("GEOGRAPHY","0","भारत की सबसे लंबी झील कौन सी है?","चिल्का झील","वुलर झील","डल झील","वेंबनाड झील","वेंबनाड झील")

    add_question("GEOGRAPHY","0","‘आर्कटिक सर्कल’ किस अक्षांश पर स्थित है?","23.5°N","66.5°N","23.5°S","66.5°S","66.5°N")

    add_question("GEOGRAPHY","0","भारत में 'नर्मदा नदी' का उद्गम स्थल कौन सा है?","विंध्याचल पर्वत","अरावली पर्वत","सतपुड़ा पर्वत","अमरकंटक","अमरकंटक")

    add_question("GEOGRAPHY","0","‘प्रशांत महासागर’ में सबसे बड़ा द्वीप कौन सा है?","न्यू गिनी","बोरनियो","हवाई","तस्मानिया","न्यू गिनी")

    add_question("GEOGRAPHY","0","‘काराकोरम पर्वत श्रृंखला’ किस देश में स्थित है?","भारत","पाकिस्तान","नेपाल","चीन","पाकिस्तान")

    add_question("GEOGRAPHY","0","किस महाद्वीप में ‘द ग्रेट विक्टोरिया डेजर्ट’ स्थित है?","अफ्रीका","एशिया","ऑस्ट्रेलिया","दक्षिण अमेरिका","ऑस्ट्रेलिया")

    add_question("GEOGRAPHY","0","भारत की सबसे बड़ी ताजे पानी की झील कौन सी है?","चिल्का झील","वुलर झील","डल झील","सांभर झील","वुलर झील")

    add_question("GEOGRAPHY","0","भारत के कौन से राज्य में सबसे ज्यादा वन क्षेत्र है?","असम","मध्य प्रदेश","महाराष्ट्र","ओडिशा","मध्य प्रदेश")

    add_question("GEOGRAPHY","0","दुनिया का सबसे बड़ा बंदरगाह कौन सा है?","सिंगापुर पोर्ट","रॉटरडैम पोर्ट","शंघाई पोर्ट","लॉस एंजेल्स पोर्ट","शंघाई पोर्ट")

    add_question("GEOGRAPHY","0","हिमालय पर्वत का सबसे ऊंचा स्थान कौन सा है?","माउंट एवरेस्ट","माउंट के2","माउंट कंचनजंगा","माउंट नंगा पर्वत","माउंट एवरेस्ट")  

    add_question("GEOGRAPHY","0","कौन सा राज्य 'पूर्वोत्तर का प्रवेशद्वार' कहा जाता है?","असम","मिजोरम","नागालैंड","मेघालय","असम")

    add_question("GEOGRAPHY","0","किस देश में ‘नील नदी’ बहती है?","इथियोपिया","सूडान","मिस्र","युगांडा","मिस्र")

    add_question("GEOGRAPHY","0","‘शेषाचलम पर्वत’ किस राज्य में स्थित है?","तमिलनाडु","कर्नाटक","आंध्र प्रदेश","केरल","आंध्र प्रदेश")

    add_question("GEOGRAPHY","0","भारत का सबसे बड़ा डेल्टा कौन सा है?","सुंदरबन","महानदी डेल्टा","गोदावरी डेल्टा","कृष्णा डेल्टा","सुंदरबन")

    add_question("GEOGRAPHY","0","'अरावली पर्वत' किस दिशा में स्थित है?","उत्तर-दक्षिण","पूर्व-पश्चिम","दक्षिण-पश्चिम","उत्तर-पश्चिम","उत्तर-दक्षिण")

    add_question("GEOGRAPHY","0","कौन सी नदी गंगा से नहीं मिलती?","यमुना","गोदावरी","गंडक","कोसी","गोदावरी")

    add_question("GEOGRAPHY","0","‘रूपकुंड झील’ किस राज्य में स्थित है?","उत्तराखंड","हिमाचल प्रदेश","जम्मू और कश्मीर","सिक्किम","उत्तराखंड")

    add_question("GEOGRAPHY","0","भारत का सबसे बड़ा तटीय राज्य कौन सा है?","तमिलनाडु","आंध्र प्रदेश","गुजरात","महाराष्ट्र","गुजरात")

    add_question("GEOGRAPHY","0","'क्योटो प्रोटोकॉल' किससे संबंधित है?","वैश्विक व्यापार","जलवायु परिवर्तन","अंतर्राष्ट्रीय शांति","परमाणु अप्रसार","जलवायु परिवर्तन")

    add_question("GEOGRAPHY","0","‘तस्मानिया’ किस देश का हिस्सा है?","न्यूजीलैंड","ऑस्ट्रेलिया","इंडोनेशिया","जापान","ऑस्ट्रेलिया")

    add_question("GEOGRAPHY","0","‘ग्रेट बैरियर रीफ’ किस महासागर में स्थित है?","अटलांटिक महासागर","प्रशांत महासागर","हिंद महासागर","दक्षिणी महासागर","प्रशांत महासागर")

    add_question("GEOGRAPHY","0","कौन सा देश 'लैटिन अमेरिका का प्रमुख' माना जाता है?","ब्राज़ील","अर्जेंटीना","मेक्सिको","चिली","ब्राज़ील")

    add_question("GEOGRAPHY","0","‘महाबलेश्वर’ किस नदी का उद्गम स्थल है?","यमुना","नर्मदा","कृष्णा","कावेरी","कृष्णा")

    add_question("GEOGRAPHY","0","भारत में ‘कालर केदार’ किस राज्य में स्थित है?","हिमाचल प्रदेश","उत्तराखंड","जम्मू और कश्मीर","सिक्किम","उत्तराखंड")

    add_question("GEOGRAPHY","0","भारत का कौन सा राज्य 'भारत का सबसे सुंदर राज्य' माना जाता है?","हिमाचल प्रदेश","केरल","राजस्थान","मेघालय","केरल")  

    add_question("GEOGRAPHY","0","'पामिर का पठार' किस महाद्वीप में स्थित है?","एशिया","यूरोप","अफ्रीका","दक्षिण अमेरिका","एशिया")

    add_question("GEOGRAPHY","0","किस राज्य में ‘अरावली पर्वत श्रेणी’ फैली हुई है?","राजस्थान","गुजरात","महाराष्ट्र","मध्य प्रदेश","राजस्थान")

    add_question("GEOGRAPHY","0","‘अल्मोड़ा’ किस राज्य में स्थित है?","उत्तराखंड","हिमाचल प्रदेश","जम्मू और कश्मीर","सिक्किम","उत्तराखंड")

    add_question("GEOGRAPHY","0","'रेशम का मार्ग' किस महाद्वीप से होकर गुजरता था?","यूरोप","एशिया","अफ्रीका","दक्षिण अमेरिका","एशिया")

    add_question("GEOGRAPHY","0","दुनिया का सबसे ठंडा स्थान कौन सा है?","ओइम्याकोन, रूस","नॉर्थ पॉल","अंटार्कटिका","ग्रीनलैंड","अंटार्कटिका")

    add_question("GEOGRAPHY","0","किस देश में सबसे ज्यादा ताजे पानी की झीलें हैं?","कनाडा","रूस","संयुक्त राज्य अमेरिका","ब्राजील","कनाडा")

    add_question("GEOGRAPHY","0","भारत का कौन सा राज्य 'भारत का मसालों का बगीचा' कहा जाता है?","केरल","तमिलनाडु","कर्नाटक","आंध्र प्रदेश","केरल")

    add_question("GEOGRAPHY","0","‘कुद्रेमुख राष्ट्रीय उद्यान’ किस राज्य में स्थित है?","तमिलनाडु","कर्नाटक","केरल","आंध्र प्रदेश","कर्नाटक")

    add_question("GEOGRAPHY","0","'ग्लेशियर' किस दिशा में ज्यादा पाई जाती है?","दक्षिणी","पूर्वी","पश्चिमी","उत्तरी","उत्तरी")

    add_question("GEOGRAPHY","0","भारत में कौन सी नदी ‘दक्षिण गंगा’ के नाम से जानी जाती है?","गोदावरी","कृष्णा","कावेरी","तापी","गोदावरी")

    add_question("GEOGRAPHY","0","भारत की सबसे बड़ी मछली पकड़ने की बंदरगाह कौन सी है?","मुंबई","कोच्चि","विशाखापत्तनम","चेन्नई","विशाखापत्तनम")

    add_question("GEOGRAPHY","0","किस राज्य में ‘भरतपुर पक्षी अभयारण्य’ स्थित है?","राजस्थान","उत्तर प्रदेश","गुजरात","मध्य प्रदेश","राजस्थान")

    add_question("GEOGRAPHY","0","'किलिमंजारो पर्वत' किस महाद्वीप में स्थित है?","एशिया","अफ्रीका","दक्षिण अमेरिका","ऑस्ट्रेलिया","अफ्रीका")

    add_question("GEOGRAPHY","0","भारत का सबसे ऊंचा जलप्रपात कौन सा है?","दूधसागर","जोग जलप्रपात","शिवसमुद्रम","नागार्जुनसागर","जोग जलप्रपात")

    add_question("GEOGRAPHY","0","'कच्छ का रण' किस राज्य में स्थित है?","राजस्थान","गुजरात","महाराष्ट्र","मध्य प्रदेश","गुजरात")

    add_question("GEOGRAPHY","0","‘मैटरहॉर्न पर्वत’ किस देश में स्थित है?","स्विट्जरलैंड","ऑस्ट्रिया","फ्रांस","इटली","स्विट्जरलैंड")

    add_question("GEOGRAPHY","0","'मध्य प्रदेश' का कौन सा शहर ‘हरित शहर’ के नाम से जाना जाता है?","भोपाल","इंदौर","ग्वालियर","जबलपुर","भोपाल")

    add_question("GEOGRAPHY","0","किस नदी को 'बिहार का शोक' कहा जाता है?","कोसी","गंडक","बागमती","सोन","कोसी")

    add_question("GEOGRAPHY","0","'सालार डी उयुनी' किस देश में स्थित है?","पेरू","बोलीविया","चिली","अर्जेंटीना","बोलीविया")

    add_question("GEOGRAPHY","0","‘कोरोमंडल तट’ किस दिशा में स्थित है?","पश्चिमी तट","पूर्वी तट","दक्षिणी तट","उत्तर तट","पूर्वी तट")

    add_question("GEOGRAPHY","0","'नंदा देवी पर्वत' किस राज्य में स्थित है?","हिमाचल प्रदेश","उत्तराखंड","सिक्किम","जम्मू और कश्मीर","उत्तराखंड")

    add_question("GEOGRAPHY","0","किस देश में 'महानदी' स्थित है?","भारत","बांग्लादेश","पाकिस्तान","नेपाल","भारत")

    add_question("GEOGRAPHY","0","किस महाद्वीप में ‘ग्रेट विक्टोरिया डेजर्ट’ स्थित है?","एशिया","अफ्रीका","ऑस्ट्रेलिया","दक्षिण अमेरिका","ऑस्ट्रेलिया")

    add_question("GEOGRAPHY","0","‘सह्याद्री पर्वत’ किस राज्य में स्थित है?","महाराष्ट्र","कर्नाटक","तमिलनाडु","केरल","महाराष्ट्र")

    add_question("GEOGRAPHY","0","‘भारत का प्रवेश द्वार’ किस शहर को कहा जाता है?","मुंबई","कोलकाता","दिल्ली","चेन्नई","मुंबई")

    add_question("GEOGRAPHY","0","कौन सी नदी 'ओडिशा का शोक' कहलाती है?","महानदी","गोदावरी","कृष्णा","तापी","महानदी")

    add_question("GEOGRAPHY","0","किस राज्य में ‘कोणार्क सूर्य मंदिर’ स्थित है?","पश्चिम बंगाल","ओडिशा","आंध्र प्रदेश","तमिलनाडु","ओडिशा")

    add_question("GEOGRAPHY","0","किस देश का ‘सेरेनगेटी राष्ट्रीय उद्यान’ प्रसिद्ध है?","केन्या","तंजानिया","दक्षिण अफ्रीका","जिम्बाब्वे","तंजानिया")

    add_question("GEOGRAPHY","0","'चिली' किस महाद्वीप में स्थित है?","दक्षिण अमेरिका","अफ्रीका","यूरोप","एशिया","दक्षिण अमेरिका")

    add_question("GEOGRAPHY","0","किस राज्य में ‘हिमकुंड साहिब’ स्थित है?","उत्तराखंड","हिमाचल प्रदेश","जम्मू और कश्मीर","पंजाब","उत्तराखंड")

    add_question("GEOGRAPHY","0","'सचिन' किस देश का मशहूर पर्वतारोही है?","भारत","नेपाल","जापान","पाकिस्तान","भारत")

    add_question("GEOGRAPHY","0","किस राज्य में ‘दुधवा राष्ट्रीय उद्यान’ स्थित है?","उत्तर प्रदेश","बिहार","पश्चिम बंगाल","ओडिशा","उत्तर प्रदेश")

    add_question("GEOGRAPHY","0","‘तिब्बत का पठार’ को किस नाम से जाना जाता है?","दुनिया की छत","एशिया का जलप्रपात","हिमालय का प्रवेशद्वार","महाद्वीपीय दर्रा","दुनिया की छत")

    add_question("GEOGRAPHY","0","भारत में कौन सा राज्य 'कॉफी राज्य' के नाम से प्रसिद्ध है?","कर्नाटक","केरल","तमिलनाडु","आंध्र प्रदेश","कर्नाटक")

    add_question("GEOGRAPHY","0","'गोवा' किस नदी के किन  ारे स्थित है?","गंगा","गोदावरी","कावेरी","मांडवी","मांडवी")
    
    
    
    
    
