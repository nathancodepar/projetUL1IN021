import math
import time
from grove.adc import ADC

# Initialisation du convertisseur Analogique-Numérique
adc = ADC()

def read_temperature():
    """Lecture du capteur de température Grove v1.2 sur le port A4."""
    try:
        # Lecture de la valeur brute sur le canal 4 (Port A4)
        value = adc.read(4)
        if value == 0:
            return 0.0
        
        # Formule spécifique au capteur Grove Temperature v1.2
        # (Basée sur une thermistance avec une valeur B de 4275)
        B = 4275
        R0 = 100000
        R = 1023.0 / value - 1.0
        R = R0 * R
        
        temperature = 1.0 / (math.log(R / R0) / B + 1 / 298.15) - 273.15
        return round(temperature, 2)
    except Exception as e:
        print(f"Erreur Température: {e}")
        return 0.0

def read_luminosity():
    """Lecture du capteur de lumière sur le port A0."""
    try:
        # Retourne la valeur brute entre 0 et 1023
        return float(adc.read(0))
    except Exception as e:
        print(f"Erreur Luminosité: {e}")
        return 0.0

def read_sound_level():
    """Lecture du capteur sonore sur le port A2."""
    try:
        # Retourne l'intensité sonore brute
        return float(adc.read(2))
    except Exception as e:
        print(f"Erreur Son: {e}")
        return 0.0