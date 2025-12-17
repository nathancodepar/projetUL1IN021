import smbus
import math
import time

# Initialisation du bus I2C (1 sur Raspberry Pi 4)
bus = smbus.SMBus(1)
ADDRESS = 0x04

def read_adc(channel):
    """Lit la valeur brute 12 bits (0-4095) sur le canal donné"""
    try:
        # Registre de lecture pour le Hat 12 bits : 0x10 + numéro de canal
        # On lit 2 octets (12 bits tiennent sur 2 octets)
        data = bus.read_i2c_block_data(ADDRESS, 0x10 + channel, 2)
        # Calcul de la valeur : octet_bas + (octet_haut * 256)
        value = data[0] + (data[1] << 8)
        return value
    except Exception as e:
        print(f"Erreur lecture I2C canal {channel}: {e}")
        return 0

def read_temperature():
    """Capteur sur A4 (Canal 4)"""
    raw_value = read_adc(4)
    if raw_value == 0: return 0.0
    
    # Conversion 12-bit vers 10-bit pour la formule standard
    value = raw_value / 4.0
    
    B = 4275
    R0 = 100000
    try:
        R = 1023.0 / value - 1.0
        R = R0 * R
        temperature = 1.0 / (math.log(R / R0) / B + 1 / 298.15) - 273.15
        return round(temperature, 2)
    except:
        return 0.0

def read_luminosity():
    """Capteur sur A0 (Canal 0)"""
    raw_value = read_adc(0)
    # Conversion en pourcentage
    percentage = (raw_value / 4095.0) * 100
    return round(percentage, 2)

def read_sound_level():
    """Capteur sur A2 (Canal 2)"""
    return float(read_adc(2))