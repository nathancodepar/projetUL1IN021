import smbus2 as smbus
import math
import time

BUS = 1
ADDRESS = 0x04
bus = smbus.SMBus(BUS)

def read_analog(pin):
    reg = 0x10 + pin
    try:
        data = bus.read_i2c_block_data(ADDRESS, reg, 2)
        # On garde la lecture standard MSB/LSB
        return (data[1] << 8) | data[0]
    except:
        return 0

def get_sensor_data():
    # --- 1. TEMPÉRATURE (A0) ---
    raw_temp = read_analog(0)
    
    # On utilise raw_temp DIRECTEMENT (sans le 4095 -) 
    # pour que la valeur monte quand il fait chaud
    val_calibree = raw_temp 
    
    if 100 < val_calibree < 4000:
        resistance = (4095.0 - val_calibree) * 100000.0 / val_calibree
        # Formule avec B=4250 pour la version v1.2
        inv_t = 1.0 / 298.15 + (1.0 / 4250.0) * math.log(resistance / 100000.0)
        temp_final = (1.0 / inv_t) - 273.15
    else:
        temp_final = 23.0

    # --- 2. LUMINOSITÉ (Port A2) ---
    raw_light = read_analog(2)
    
    # Si la valeur est très basse (comme tes 15), on booste la sensibilité.
    # On considère que 4095 (max) = environ 1000 lux (soleil direct)
    # Et on utilise un multiplicateur pour que la lumière artificielle 
    # de ton bureau arrive vers les 300-500 lx.
    
    # Formule boostée :
    light_lx = (raw_light / 4095.0) * 1200 
    
    # Si tu as toujours 15, essaie l'inversion (certains Hats Grove inversent le signal) :
    # light_lx = ((4095 - raw_temp) / 4095.0) * 1000

    light_percent = round(light_lx, 0)
    # --- 3. SON (A4) ---
    # Pour le son, on va lire plusieurs fois très vite pour attraper le "pic" de bruit
    # --- 3. SON (Port A4) ---
    # On prend 50 mesures très rapides pour détecter l'amplitude maximale
    # --- 3. SON (Port A4) ---
    samples = [read_analog(4) for _ in range(50)]
    amplitude = max(samples) - min(samples)
    
    # On utilise une échelle plus douce pour les petits bruits
    if amplitude < 10:
        sound_db = 30 # Silence total
    else:
        # Formule ajustée pour être moins "généreuse" sur les décibels
        sound_db = (20 * math.log10(amplitude)) + 15
        
    sound_db = max(30, min(100, sound_db))

    return round(temp_final, 1), light_percent, round(sound_db, 1)