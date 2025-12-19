import sqlite3
import os

DB_PATH = "data/workspace.db"

def init_db():
    if not os.path.exists('data'):
        os.makedirs('data')
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temp REAL, light REAL, sound REAL, status TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS preferences (
        id INTEGER PRIMARY KEY,
        min_temp REAL, max_temp REAL, min_light REAL, min_sound REAL)''')
    
    cursor.execute("INSERT OR IGNORE INTO preferences VALUES (1, 19.0, 25.0, 300.0, 600.0)")
    
    conn.commit()
    conn.close()

def get_preferences():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    res = conn.execute("SELECT * FROM preferences WHERE id=1").fetchone()
    conn.close()
    return dict(res)

def save_measurement(temp, light, sound, status):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO measurements (temp, light, sound, status) VALUES (?, ?, ?, ?)",
                 (temp, light, sound, status))
    conn.commit()
    conn.close()
