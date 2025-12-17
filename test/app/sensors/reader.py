import math
import time
from grove.adc import ADC

# Initialisation de l'ADC (Automatique pour le Hat 12 bits)
adc = ADC()

def read_temperature():
    """Capteur sur A4. Formule pour Grove Temperature v1.2 (12-bit)"""
    try:
        # Lecture brute sur le port A4 (Canal 4)
        raw_value = adc.read(4)
        
        # Conversion 12-bit (0-4095) vers équivalent 10-bit (0-1023) 
        # pour la formule mathématique standard
        value = raw_value / 4.0
        
        if value == 0: return 0.0
        
        B = 4275  # Valeur B du thermistor
        R0 = 100000 # Résistance nominale
        R = 1023.0 / value - 1.0
        R = R0 * R
        
        # Équation de Steinhart-Hart simplifiée
        temperature = 1.0 / (math.log(R / R0) / B + 1 / 298.15) - 273.15
        return round(temperature, 2)
    except Exception as e:
        print(f"Erreur Température: {e}")
        return 0.0

def read_luminosity():
    """Capteur sur A0. Retourne un pourcentage (0-100%)"""
    try:
        raw_value = adc.read(0)
        # On transforme le 0-4095 en 0-100
        percentage = (raw_value / 4095.0) * 100
        return round(percentage, 2)
    except Exception as e:
        print(f"Erreur Lumière: {e}")
        return 0.0

def read_sound_level():
    """Capteur sur A2. Retourne la valeur brute 12-bit"""
    try:
        return float(adc.read(2))
    except Exception as e:
        print(f"Erreur Son: {e}")
        return 0.0