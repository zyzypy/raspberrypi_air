import RPi.GPIO as GPIO
import sys
import time

LED = 21

def main():
    # GPIO.setwarnings(False)   # 如果有多个脚本控制电路会警告
    GPIO.setmode(GPIO.BCM)
    # GPIO.input(LED)     # 读输入引脚的值 #This will return either 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True
    # mode = GPIO.getmode()     # 判断board还是BCM模式
    GPIO.setup(LED, GPIO.OUT)   # 设置引脚为输入
    # GPIO.output(channel, state)   #State can be 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
    while(True):
        GPIO.output(LED,True)
        time.sleep(0.5)
        GPIO.output(LED,False)
        time.sleep(0.5)

main()





