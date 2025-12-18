import sqlite3

DB_PATH = "data/workspace.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Table pour les mesures
    cursor.execute('''CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temp REAL, light REAL, sound REAL, status TEXT)''')
    
    # Table pour les préférences (une seule ligne)
    cursor.execute('''CREATE TABLE IF NOT EXISTS preferences (
        id INTEGER PRIMARY KEY,
        min_temp REAL, max_temp REAL,
        min_light REAL, min_sound REAL)''')
    
    # Valeurs par défaut si vide
    cursor.execute("INSERT OR IGNORE INTO preferences (id, min_temp, max_temp, min_light, min_sound) VALUES (1, 19, 25, 300, 500)")
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