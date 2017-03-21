import time

import RPi.GPIO as GPIO

from sensor import dht22

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# 配置数据线的针
instance = dht22.DHT22(pin=4)

if __name__ == '__main__':
    while True:
        result = instance.read()
        print('\n', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        if result.is_valid():
            print("Temperature: %0.1f C" % result.temperature)
            print("Humidity: %0.1f %%" % result.humidity)
        else:
            print("Error: %d" % result.error_code)

        time.sleep(10)
