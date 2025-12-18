import time
import RPi.GPIO as GPIO
from sensors import get_sensor_data
from database import save_measurement, get_preferences, init_db

# --- CONFIGURATION DE LA LED ---
LED_PIN = 18 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

def run_monitor():
    # Initialisation de la base de données
    init_db()
    print("Démarrage du monitoring (toutes les 30s) avec alerte LED...")

    try:
        while True:
            # 1. Récupérer les vraies valeurs des capteurs
            temp, light, sound = get_sensor_data()
            
            # 2. Récupérer les préférences de l'utilisateur
            pref = get_preferences()
            
            # 3. Vérifier les conditions et lister les problèmes
            errors = []
            if not (pref['min_temp'] <= temp <= pref['max_temp']):
                errors.append("Température")
            if light < pref['min_light']:
                errors.append("Luminosité")
            if sound > pref['min_sound']:
                errors.append("Bruit")

            # 4. Logique de l'alerte (LED + Statut)
            if not errors:
                # Tout est OK
                GPIO.output(LED_PIN, GPIO.LOW)
                status = "IDÉAL"
            else:
                # Il y a au moins un problème
                GPIO.output(LED_PIN, GPIO.HIGH)
                status = "ALERTE: " + ", ".join(errors)
            
            # 5. Enregistrer dans SQLite
            save_measurement(temp, light, sound, status)
            
            # Affichage console pour débugger
            print(f"[{status}] T:{temp}°C | L:{light}lx | S:{sound}dB")
            
            # 6. Attendre 30 secondes
            time.sleep(30)

    except KeyboardInterrupt:
        print("Arrêt du moniteur...")
    finally:
        # On éteint la LED et on libère les ressources GPIO proprement
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    run_monitor()