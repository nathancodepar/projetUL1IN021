import time
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.grove_sound_sensor import GroveSoundSensor
from grove.grove_temperature_sensor_v1_2 import GroveTemperatureSensor

# Assurez-vous que les capteurs sont branchés sur ces ports A (Analogiques)
light_sensor = GroveLightSensor(0) # Port A0
sound_sensor = GroveSoundSensor(2) # Port A2
temp_sensor = GroveTemperatureSensor(4) # Port A4

def read_temperature():
    return round(temp_sensor.temperature, 2)

def read_luminosity():
    return float(light_sensor.light)

def read_sound_level():
    return float(sound_sensor.sound)