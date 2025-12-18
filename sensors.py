import smbus2 as smbus
import math
import time

BUS = 1
ADDRESS = 0x04
bus = smbus.SMBus(BUS)

def read_analog(pin):
    """Lit les deux octets bruts et les réassemble dans le bon sens"""
    reg = 0x10 + pin
    try:
        # On lit 2 octets à partir du registre
        data = bus.read_i2c_block_data(ADDRESS, reg, 2)
        # data[0] est l'octet de poids faible (LSB)
        # data[1] est l'octet de poids fort (MSB)
        # Sur le Grove Base Hat, le montage est souvent : (MSB << 8) | LSB
        val = (data[1] << 8) | data[0]
        
        # Si la valeur est toujours délirante (ex: > 4095), tente l'inverse :
        # val = (data[0] << 8) | data[1]
        
        return val
    except Exception as e:
        print(f"Erreur de lecture I2C: {e}")
        return 0

def get_sensor_data():
    # 1. TEMPÉRATURE (A0)
    raw_temp = read_analog(0)
    temp = 0.0
    if 0 < raw_temp < 4095:
        # Formule spécifique Grove Temp v1.2 (Thermistance)
        # Résolution 12-bits = 4095
        resistance = (4095.0 - raw_temp) * 100000.0 / raw_temp
        temp = 1.0 / (math.log(resistance / 100000.0) / 4275 + 1 / 298.15) - 273.15
    
    # 2. LUMINOSITÉ (A2)
    raw_light = read_analog(2)
    # On ramène la valeur sur une échelle de 0 à 100
    light_percent = round((raw_light / 4095.0) * 100, 1)

    # 3. SON (A4)
    raw_sound = read_analog(4)
    # Le son est très instable, on normalise la valeur brute
    sound_val = raw_sound 

    return round(temp, 1), light_percent, sound_val