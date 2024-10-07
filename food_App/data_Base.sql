import sqlite3
def setup_database():
    conn = sqlite3.connect('nutrition_data.db')
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS nutrition
                 (id INTEGER PRIMARY KEY, food_name TEXT, calories REAL, protein REAL)''')
    conn.commit()
    conn.close()
    setup_database()