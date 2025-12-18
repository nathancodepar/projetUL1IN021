import time
from sensors import get_sensor_data
from database import save_measurement, get_preferences, init_db

def run_monitor():
    # On s'assure que la table existe au démarrage
    init_db()
    print("Démarrage du monitoring (toutes les 30s)...")

    while True:
        # 1. Récupérer les vraies valeurs des capteurs
        temp, light, sound = get_sensor_data()
        
        # 2. Récupérer les préférences de l'utilisateur dans la DB
        pref = get_preferences()
        
        # 3. Vérifier si les conditions sont bonnes
        # On compare avec les seuils enregistrés en base
        is_ok = (pref['min_temp'] <= temp <= pref['max_temp']) and \
                (light >= pref['min_light']) and \
                (sound <= pref['min_sound'])
        
        status = "IDÉAL" if is_ok else "MAUVAIS"
        
        # 4. Enregistrer tout ça dans SQLite
        save_measurement(temp, light, sound, status)
        
        print(f"[{status}] T:{temp}°C | L:{light} | S:{sound}")
        
        # 5. Attendre 30 secondes
        time.sleep(30)

if __name__ == "__main__":
    run_monitor()