from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
from database import init_db, DB_PATH

app = FastAPI()
init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")

class Prefs(BaseModel):
    min_temp: float
    max_temp: float
    min_light: float

@app.get("/api/current")
def get_current():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 1").fetchone()
    return dict(data) if data else {}

@app.post("/api/preferences")
def update_prefs(p: Prefs):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE preferences SET min_temp=?, max_temp=?, min_light=? WHERE id=1",
                 (p.min_temp, p.max_temp, p.min_light))
    conn.commit()
    return {"message": "Préférences mises à jour"}