from sensor.pms5003s import get_results
import time
import serial

if __name__ == '__main__':
    # 查看可用串口  控制台：python -m serial.tools.list_ports
    try:
        # ser = serial.Serial("/dev/ttyUSB0", 9600)       # 如果程序正在运行，设备拔出再插上会变为ttyUSB1
        ser = serial.Serial("com9", 9600)       # 传感器通过转usb的转换板子连windows10平台 设备管理器-安装过期驱动-串口和LPT，成功的话会看到COM3之类的
    except Exception as e:
        ser = serial.Serial("/dev/ttyUSB1", 9600)
        # ser = serial.Serial("/dev/ttyAMA0", 9600)     # 树莓派3b的串口被蓝牙和console占用，设置了一会也没成功。

    try:
        while True:
            results = get_results(ser)
            print('pm2.5: %d ug/m3' % results['pm2dot5'], 'formaldehyde: %s mg/m3' % format(results['formaldehyde'], '.3f'))
            time.sleep(10)

    except KeyboardInterrupt:
        if ser != None:
            ser.close()