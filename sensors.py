import smbus2 as smbus
import math
import time

# Configuration du bus I2C pour le Raspberry Pi
BUS = 1
ADDRESS = 0x04
bus = smbus.SMBus(BUS)

def read_analog(pin):
    """
    Lit les deux octets bruts sur le port analogique spécifié (A0, A2, A4)
    et les réassemble en une valeur 12-bits (0-4095).
    """
    reg = 0x10 + pin
    try:
        # Lecture de 2 octets (block data)
        data = bus.read_i2c_block_data(ADDRESS, reg, 2)
        # On réassemble : data[0] est le LSB (poids faible), data[1] est le MSB (poids fort)
        val = (data[1] << 8) | data[0]
        return val
    except Exception as e:
        print(f"Erreur de lecture I2C sur port A{pin}: {e}")
        return 0

def get_sensor_data():
    """
    Récupère et convertit les données de tous les capteurs.
    """
    
    # --- 1. TEMPÉRATURE (Port A0) ---
    raw_temp = read_analog(0)
    temp_final = 0.0
    
    # Inversion du signal pour le Hat Grove sur RPi 4
    val_calibree = 4095 - raw_temp 
    
    # On s'assure que val_calibree n'est pas trop proche de 0 ou 4095
    if 100 < val_calibree < 4000:
        try:
            # Calcul de la résistance avec un facteur de correction 
            # (Si 60°C est trop haut, on augmente le dénominateur)
            resistance = (4095.0 - val_calibree) * 100000.0 / val_calibree
            
            # Formule Steinhart-Hart
            # On passe B à 3975 (souvent plus précis pour les versions récentes du capteur v1.2)
            inv_t = 1.0 / 298.15 + (1.0 / 3975.0) * math.log(resistance / 100000.0)
            temp_final = (1.0 / inv_t) - 273.15
            
        except Exception:
            temp_final = 0.0
    else:
        # Si on est hors limites, on renvoie une valeur de sécurité
        temp_final = 20.0
    
    # --- 2. LUMINOSITÉ (Port A2) ---
    # Conversion en pourcentage simple (0 = Noir, 100 = Très lumineux)
    raw_light = read_analog(2)
    light_percent = round((raw_light / 4095.0) * 100, 1)

    # --- 3. SON (Port A4) ---
    # Approximation en décibels (dB)
    raw_sound = read_analog(4)
    
    # On utilise une valeur minimale de 1 pour éviter l'erreur mathématique log(0)
    val_for_log = max(raw_sound, 1)
    
    # Formule logarithmique : 20 * log10(valeur) + offset
    # L'offset (+15 ici) est à ajuster selon le calme de votre pièce
    sound_db = (20 * math.log10(val_for_log)) + 15
    
    # Limitation des valeurs pour rester dans une échelle humaine réaliste (30 à 100 dB)
    sound_db = max(30, min(100, sound_db))

    return round(temp_final, 1), light_percent, round(sound_db, 1)

# Petit test rapide si on lance le fichier directement
if __name__ == "__main__":
    try:
        while True:
            t, l, s = get_sensor_data()
            print(f"Temp: {t}°C | Lum: {l}% | Son: {s} dB")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Arrêt du test.")