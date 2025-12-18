import time
from sensors import get_sensor_data
from database import save_measurement, get_preferences

def run_monitor():
    while True:
        temp, light, sound = get_sensor_data()
        pref = get_preferences()
        
        # Vérification des seuils
        is_ok = (pref['min_temp'] <= temp <= pref['max_temp']) and \
                (light >= pref['min_light'])
        
        status = "OK" if is_ok else "ALERTE"
        
        save_measurement(temp, light, sound, status)
        print(f"Mesure effectuée : {temp}°C, {light} lux. Status: {status}")
        
        time.sleep(30)

if __name__ == "__main__":
    run_monitor()