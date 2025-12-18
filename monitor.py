import time
import RPi.GPIO as GPIO
import signal
import sys
from sensors import get_sensor_data
from database import save_measurement, get_preferences, init_db

# --- CONFIGURATION DE LA LED ---
LED_PIN = 18 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

def run_monitor():
    init_db()
    print("Démarrage du monitoring (toutes les 30s) avec alerte LED...")

    try:
        while True:
            temp, light, sound = get_sensor_data()
            pref = get_preferences()
            
            errors = []
            if not (pref['min_temp'] <= temp <= pref['max_temp']):
                errors.append("Température")
            if light < pref['min_light']:
                errors.append("Luminosité")
            if sound > pref['min_sound']:
                errors.append("Bruit")

            if not errors:
                GPIO.output(LED_PIN, GPIO.LOW)
                status = "IDÉAL"
            else:
                GPIO.output(LED_PIN, GPIO.HIGH)
                status = "ALERTE: " + ", ".join(errors)
            
            save_measurement(temp, light, sound, status)
            print(f"[{status}] T:{temp}°C | L:{light}lx | S:{sound}dB")
            
            time.sleep(10)

    except (KeyboardInterrupt, SystemExit):
        # Capturé lors du clic sur "Arrêter" (Signal SIGINT)
        print("Signal d'arrêt reçu...")
    finally:
        # Sécurité ultime : On éteint la LED avant de quitter
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()
        print("LED éteinte et GPIO libéré.")

if __name__ == "__main__":
    run_monitor()