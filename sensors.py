import smbus2 as smbus
import math

BUS = 1
ADDRESS = 0x04 # Adresse standard du Grove Base Hat

bus = smbus.SMBus(BUS)

def read_analog(pin):
    # Lecture du registre correspondant à la pine analogique (A0, A2, etc.)
    # Sur le Hat Grove, A0 est souvent au registre 0x10
    reg = 0x10 + pin
    data = bus.read_word_data(ADDRESS, reg)
    return data

def get_sensor_data():
    # Exemple pour Température v1.2 (Thermistance)
    raw_temp = read_analog(0) # Port A0
    B = 4275
    R0 = 100000
    if raw_temp > 0:
        R = 1023.0 / raw_temp - 1.0
        R = R0 * R
        temperature = 1.0 / (math.log(R / R0) / B + 1 / 298.15) - 273.15
    else: temperature = 0

    # Luminosité v1.2
    light = read_analog(2) # Port A2
    
    # Son v1.6
    sound = read_analog(4) # Port A4
    
    return round(temperature, 2), light, sound