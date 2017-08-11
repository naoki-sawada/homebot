import time
import RPi.GPIO as GPIO

class Plugin:
    def __init__(self):
        self.hs = HumanSensor()

    def read(self):
        self.hs.read()


class HumanSensor:
    def __init__(self, pin=29):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)

    def read(self):
        ret = GPIO.input(self.pin)
        print(ret)
        return ret


# while True:
#     pl = Plugin()
#     pl.read()
#     time.sleep(1)
