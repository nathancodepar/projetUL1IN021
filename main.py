import subprocess
import os
import signal
import sqlite3
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database import init_db, DB_PATH

app = FastAPI()
init_db()

# --- NOUVEAU : Gestion du processus moniteur ---
monitor_process = None 

app.mount("/static", StaticFiles(directory="static"), name="static")

class Prefs(BaseModel):
    min_temp: float
    max_temp: float
    min_light: float
    min_sound: float

# --- ROUTES EXISTANTES (Mises à jour) ---

@app.get("/api/current")
def get_current():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 1").fetchone()
    conn.close()
    return dict(data) if data else {}

@app.get("/api/preferences")
def read_prefs():
    from database import get_preferences
    return get_preferences()

@app.post("/api/preferences")
def update_prefs(p: Prefs):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE preferences SET min_temp=?, max_temp=?, min_light=?, min_sound=? WHERE id=1",
                 (p.min_temp, p.max_temp, p.min_light, p.min_sound))
    conn.commit()
    conn.close()
    return {"message": "Success"}

# --- NOUVELLES ROUTES : Contrôle du moniteur ---

@app.post("/api/monitor/start")
def start_monitor():
    global monitor_process
    # Vérifie si le processus tourne déjà
    if monitor_process is None or monitor_process.poll() is not None:
        # Lance monitor.py. "python3" est recommandé sur Raspberry Pi
        monitor_process = subprocess.Popen(["python3", "monitor.py"])
        return {"status": "Moniteur démarré", "pid": monitor_process.pid}
    return {"status": "Le moniteur tourne déjà"}

@app.post("/api/monitor/stop")
def stop_monitor():
    global monitor_process
    if monitor_process and monitor_process.poll() is None:
        monitor_process.terminate() # Arrête proprement le script
        monitor_process = None
        return {"status": "Moniteur arrêté"}
    return {"status": "Le moniteur n'est pas lancé"}

@app.get("/api/monitor/status")
def get_monitor_status():
    # Renvoie l'état au site web pour griser ou non les boutons
    is_running = monitor_process is not None and monitor_process.poll() is None
    return {"running": is_running}