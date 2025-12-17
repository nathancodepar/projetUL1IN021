from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import threading
import time
from app.sensors.reader import read_temperature, read_luminosity, read_sound_level
# Importez ici votre logique de base de données si nécessaire

app = FastAPI()

# Stockage temporaire de la dernière mesure
current_data = {"temp": 0, "light": 0, "sound": 0}

def background_measurements():
    """Boucle infinie de lecture des capteurs"""
    while True:
        current_data["temp"] = read_temperature()
        current_data["light"] = read_luminosity()
        current_data["sound"] = read_sound_level()
        
        print(f"MAJ Capteurs: {current_data}")
        # Optionnel: Sauvegarder ici dans la base de données
        time.sleep(30)

# Lancement du thread au démarrage
thread = threading.Thread(target=background_measurements, daemon=True)
thread.start()

@app.get("/api/status")
async def get_status():
    """Endpoint pour que le frontend récupère les données"""
    return current_data

@app.get("/")
async def read_index():
    return {"message": "Serveur opérationnel. Accédez à /api/status pour les données."}