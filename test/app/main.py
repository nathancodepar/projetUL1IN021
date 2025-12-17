from fastapi import FastAPI
import threading
import time
from app.sensors.reader import read_temperature, read_luminosity, read_sound_level

app = FastAPI()

# Stockage en mémoire
current_data = {"temp": 0, "light": 0, "sound": 0}

def background_measurements():
    while True:
        # Mise à jour des données
        current_data["temp"] = read_temperature()
        current_data["light"] = read_luminosity()
        current_data["sound"] = read_sound_level()
        
        print(f"Capteurs (SMBus) -> Temp: {current_data['temp']}°C, Light: {current_data['light']}%")
        time.sleep(30)

# Démarrage du thread de lecture
thread = threading.Thread(target=background_measurements, daemon=True)
thread.start()

@app.get("/api/status")
async def get_status():
    return current_data

@app.get("/")
async def index():
    return {"status": "Serveur SMBus actif", "data_url": "/api/status"}