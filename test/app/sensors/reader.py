import smbus
import math
import time

bus = smbus.SMBus(1)
ADDRESS = 0x04

def read_adc(channel):
    """Lecture standard pour le Hat Pi 2/3 (10 bits)"""
    try:
        # Sur ce modèle, on lit souvent un seul octet ou un mot de 10 bits
        data = bus.read_i2c_block_data(ADDRESS, 0x10 + channel, 2)
        # On ajuste pour le format 10 bits
        value = data[0] + (data[1] << 8)
        return value
    except Exception as e:
        return 0

def read_temperature():
    """Adapté pour 3.3V et 10 bits"""
    raw_value = read_adc(4)
    if raw_value <= 0: return 0.0
    
    # Plus besoin de diviser par 4 car on est déjà en 10 bits (0-1023)
    B = 4275
    R0 = 100000
    try:
        # Formule adaptée au 3.3V
        R = 1023.0 / raw_value - 1.0
        R = R0 * R
        temperature = 1.0 / (math.log(R / R0) / B + 1 / 298.15) - 273.15
        return round(temperature, 2)
    except:
        return 0.0

def read_luminosity():
    """Luminosité en % (base 1023)"""
    raw_value = read_adc(0)
    # 0-1023 -> 0-100%
    percentage = (raw_value / 1023.0) * 100
    return round(max(0, min(percentage, 100)), 2)

def read_sound_level():
    """Décibels adaptés pour Hat Pi 2/3 et 3.3V"""
    try:
        raw_value = read_adc(2)
        if raw_value < 2: return 30.0
        
        # On recalibre car le signal est plus faible en 3.3V
        # On augmente un peu le gain (+25) pour compenser
        dB = 20 * math.log10(raw_value) + 25
        
        # On définit une plage réaliste
        if dB < 35: dB = 35.0
        return round(min(dB, 110.0), 1)
    except:
        return 30.0