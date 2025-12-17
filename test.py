import time
from grove.gpio import GPIO

# Le port D16 correspond au GPIO 16
led = GPIO(16, GPIO.OUT)

print("Début du test : La LED doit clignoter 5 fois...")

try:
    for i in range(5):
        print("LED ON")
        led.write(1)
        time.sleep(1)
        print("LED OFF")
        led.write(0)
        time.sleep(1)
except KeyboardInterrupt:
    led.write(0)

print("Test terminé.")