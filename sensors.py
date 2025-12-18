import smbus2 as smbus
import math
import time

BUS = 1
ADDRESS = 0x04
bus = smbus.SMBus(BUS)

def read_analog(pin):
    """Lecture 12-bits avec correction de l'ordre des octets"""
    reg = 0x10 + pin
    try:
        data = bus.read_word_data(ADDRESS, reg)
        # Inversion des octets (le Hat envoie le MSB en premier)
        return ((data & 0xFF) << 8) | (data >> 8)
    except:
        return 0

def get_sensor_data():
    # 1. TEMPÉRATURE (A0) - Formule Thermistance v1.2
    raw_temp = read_analog(0)
    if 0 < raw_temp < 4095:
        # Calcul de la résistance pour un ADC 12-bits
        resistance = (4095.0 - raw_temp) * 100000.0 / raw_temp
        # Formule de Steinhart-Hart
        # $T = \frac{1}{\frac{\ln(R/R0)}{B} + \frac{1}{298.15}} - 273.15$
        temp = 1.0 / (math.log(resistance / 100000.0) / 4275 + 1 / 298.15) - 273.15
    else:
        temp = 0.0

    # 2. LUMINOSITÉ (A2)
    # On normalise sur une échelle de 0 à 1000 pour plus de clarté
    raw_light = read_analog(2)
    light_score = round((raw_light / 4095.0) * 1000, 1)

    # 3. SON (A4)
    # On prend le maximum sur 10 échantillons pour détecter les pics de bruit
    samples = [read_analog(4) for _ in range(10)]
    sound_level = max(samples)
    
    return round(temp, 1), light_score, sound_level