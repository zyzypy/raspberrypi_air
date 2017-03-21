# # run示例
# import RPi.GPIO as GPIO
# import dht11
#
# # initialize GPIO
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()
#
# # 配置数据线的针
# instance = dht11.DHT11(pin=4)
# result = instance.read()
#
# if result.is_valid():
#     print("Temperature: %d C" % result.temperature)
#     # DHT11的湿度较dht22偏低 湿度反应较慢 采样率较少
#     print("Humidity: %d %%" % result.humidity)
# else:
#     print("Error: %d" % result.error_code)
