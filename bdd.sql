CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    mdp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY,
    temperature REAL,
    luminosite REAL,
    temps_max REAL,
    son REAL,
    FOREIGN KEY (id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS donnes (
    lancement INTEGER,
    temps REAL,
    temperature REAL,
    luminosite REAL,
    son INTEGER,
    PRIMARY KEY (lancement, temps)
);