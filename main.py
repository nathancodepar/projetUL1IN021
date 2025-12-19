import subprocess
import os
import signal
import sqlite3
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database import init_db, DB_PATH

app = FastAPI()

init_db()

monitor_process = None 

app.mount("/static", StaticFiles(directory="static"), name="static")

class Prefs(BaseModel):
    min_temp: float
    max_temp: float
    min_light: float
    min_sound: float


@app.get("/api/current")
def get_current():
    """Récupère la dernière mesure en base de données"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 1").fetchone()
    conn.close()
    return dict(data) if data else {}

@app.get("/api/preferences")
def read_prefs():
    """Lit les préférences actuelles"""
    from database import get_preferences
    return get_preferences()

@app.post("/api/preferences")
def update_prefs(p: Prefs):
    """Met à jour les préférences dans la base"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE preferences SET min_temp=?, max_temp=?, min_light=?, min_sound=? WHERE id=1",
        (p.min_temp, p.max_temp, p.min_light, p.min_sound)
    )
    conn.commit()
    conn.close()
    return {"message": "Success"}


@app.post("/api/monitor/start")
def start_monitor():
    """Lance le script monitor.py en arrière-plan"""
    global monitor_process
    
    if monitor_process is None or monitor_process.poll() is not None:
        monitor_process = subprocess.Popen(
            ["python3", "monitor.py"], 
            preexec_fn=os.setsid
        )
        return {"status": "Moniteur démarré", "pid": monitor_process.pid}
    return {"status": "Le moniteur tourne déjà"}

@app.post("/api/monitor/stop")
def stop_monitor():
    """Arrête proprement le moniteur et éteint la LED"""
    global monitor_process
    
    if monitor_process and monitor_process.poll() is None:
        try:
            os.killpg(os.getpgid(monitor_process.pid), signal.SIGINT)
            monitor_process = None
            return {"status": "Moniteur arrêté (LED éteinte)"}
        except Exception as e:
            return {"status": f"Erreur lors de l'arrêt: {str(e)}"}
    return {"status": "Le moniteur n'est pas lancé"}

@app.get("/api/monitor/status")
def get_monitor_status():
    """Vérifie si le moniteur est en cours d'exécution"""
    is_running = monitor_process is not None and monitor_process.poll() is None
    return {"running": is_running}
