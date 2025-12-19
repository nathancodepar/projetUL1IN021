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
        return (data[1] << 8) | data[0]
    except:
        return 0

def get_sensor_data():
    raw_temp = read_analog(0)
    val_calibree = raw_temp 
    
    if 100 < val_calibree < 4000:
        resistance = (4095.0 - val_calibree) * 100000.0 / val_calibree
        inv_t = 1.0 / 298.15 + (1.0 / 4250.0) * math.log(resistance / 100000.0)
        temp_final = (1.0 / inv_t) - 273.15
    else:
        temp_final = 23.0

    raw_light = read_analog(2)
    
    light_lx = (raw_light / 4095.0) * 1200 

    light_percent = round(light_lx, 0)

    samples = [read_analog(4) for _ in range(50)]
    amplitude = max(samples) - min(samples)
    
    if amplitude < 10:
        sound_db = 30
    else:
        sound_db = (20 * math.log10(amplitude)) + 15
        
    sound_db = max(30, min(100, sound_db))

    return round(temp_final, 1), light_percent, round(sound_db, 1)
