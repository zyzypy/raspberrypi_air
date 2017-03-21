from sensor import dht22
from sensor.pms5003s import get_results
import serial
from flask import Flask, render_template, redirect, session
import random
import json
import time
import RPi.GPIO as GPIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'AKJSDHFKJHA'


def dht22_data_to_session():
    """
    实时温度 湿度，
    为了避免多个方法同时操作传感器，所以数据存入session对象
    """
    # 函数之间完全隔离，global，g对象都不行跨函数访问，仔细理解session跟全局变量的区别，和函数的返回值。

    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    # 配置数据线的针
    instance = dht22.DHT22(pin=4)   # BCM

    result = instance.read()
    # print('\n', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    if result.is_valid():
        session['temperature'] = str(result.temperature)
        session['humidity'] = str(result.humidity)
        # print("Temperature: %0.1f C" % result.temperature)
        # print("Humidity: %0.1f %%" % result.humidity)
    else:
        pass        # 传感器数据收集失败时session中的数据保持上一组
        # session['temperature'] = '-1'
        # session['humidity'] = '-1'
        # print("Error: %d" % result.error_code)
    GPIO.cleanup()    # 因为两个方法同时操作针脚会冲突，所以先将数据存入session。

def pms5003s_data_to_session():
    # 查看可用串口  控制台：python -m serial.tools.list_ports
    # usb转串口的芯片有时会不太稳定，需要重新插拔。
    try:
        ser = serial.Serial("/dev/ttyUSB0", 9600)       # 如果程序正在运行，设备拔出再插上会变为ttyUSB1
    except Exception as e:
        print(e)
        ser = serial.Serial("/dev/ttyUSB1", 9600)
        # ser = serial.Serial("/dev/ttyAMA0", 9600)     # 树莓派3b的串口被蓝牙和console占用，设置了一会也没成功。


    try:
        results = get_results(ser)
        if results != '-1':
            session['pm1dot0'] = results['pm1dot0']
            session['pm2dot5'] = results['pm2dot5']
            session['pm10dot0'] = results['pm10dot0']

            session['particulate0dot3'] = results['particulate0dot3']
            session['particulate0dot5'] = results['particulate0dot5']
            session['particulate1dot0'] = results['particulate1dot0']
            session['particulate2dot5'] = results['particulate2dot5']
            session['particulate5dot0'] = results['particulate5dot0']
            session['particulate10dot0'] = results['particulate10dot0']

            session['formaldehyde'] = results['formaldehyde']
        else:
            pass    # 校验错误
    except KeyboardInterrupt:
        if ser != None:
            ser.close()


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/temperature_now')
def temperature_now():
    if session:
        """
        保持传感器数据更新.因为无法做到传感器while取数据跟 web框架监听同时进行，所以还是要触发下传感器
        """
        dht22_data_to_session()
        # print(session['temperature'])
        return session['temperature']
    else:
        # print('session无数据')
        dht22_data_to_session()
        return '-1'


@app.route('/humidity_now')
def humidity_now():
    if session:
        """同一个传感器只在一个数据里触发，另一个数据从session取
        """
        # print(session['humidity'])
        return session['humidity']
    else:
        # print('session无数据')
        dht22_data_to_session()
        return '-1'


@app.route('/pms5003s/<name>')
def pms5003s(name):
    if session.items():     # dict_keys(['temperature', 'humidity'])
        if name == 'pm1dot0':
            """触发传感器新读取
            """
            # print(session['pm1dot0'])
            pms5003s_data_to_session()
            return str(session['pm1dot0'])
        elif name == 'pm2dot5':
            return str(session['pm2dot5'])
        elif name == 'pm10dot0':
            return str(session['pm10dot0'])

        elif name == 'particulate':
            data = list()
            data.append(session['particulate0dot3'])
            data.append(session['particulate0dot5'])
            data.append(session['particulate1dot0'])
            data.append(session['particulate2dot5'])
            data.append(session['particulate5dot0'])
            data.append(session['particulate10dot0'])

            return data.__str__()

        elif name == 'formaldehyde':
            return str(session['formaldehyde'])
        else:
            pass
    else:   # 程序刚启动session为空, 或报键错误
        pms5003s_data_to_session()




# 传感器工作，数据每几秒更新到内存变量中，供其它方法调取，避免请求太频繁导致gpio错误

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80, threaded=True)

