from sensor.pms5003s import get_results
import time
import serial

if __name__ == '__main__':
    # 查看可用串口  控制台：python -m serial.tools.list_ports
    # usb转串口的芯片有时会不太稳定，需要重新插拔。
    try:
        ser = serial.Serial("/dev/ttyUSB0", 9600)       # 如果程序正在运行，设备拔出再插上会变为ttyUSB1
    except Exception as e:
        ser = serial.Serial("/dev/ttyUSB1", 9600)
        # ser = serial.Serial("/dev/ttyAMA0", 9600)     # 树莓派3b的串口被蓝牙和console占用，设置了一会也没成功。

    try:
        while True:
            time.sleep(10)
            results = get_results(ser)
            if results != '-1':

                print(results.pm1dot0)
    except KeyboardInterrupt:
        if ser != None:
            ser.close()