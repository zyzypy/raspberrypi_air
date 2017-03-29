# coding=utf-8
from sensor.pms5003s import get_results
import time
import serial

if __name__ == '__main__':
    """ 设备连接方式：pms5003s传感器连 排针转ttl的转换板 再连ttl转串口usb的转换板 最后插到linux或win平台的usb口中。
        树莓派直接识别。win平台自动安装驱动，如果没有自动安装的话试试 设备管理器-安装过期驱动-串口和LPT"""
    """ 查看可用串口  终端：python -m serial.tools.list_ports
        树莓派显示/dev/ttyUSB0 。win平台 COM3 。根据显示修改下面的代码"""
    try:
        # ser = serial.Serial("/dev/ttyUSB0", 9600)
        # ser = serial.Serial("/dev/ttyAMA0", 9600)     # 树莓派3b的串口被蓝牙占用，网上有教程解除占用，ttl直接连串口。就不用 ttl转串口usb的板子了。
        ser = serial.Serial("com3", 9600)               # win平台
    except Exception as e:
        print('设备连接失败：', e)

    try:
        while True:
            results = get_results(ser)
            print('pm2.5: %d ug/m3' % results['pm2dot5'], 'formaldehyde: %s mg/m3' % format(results['formaldehyde'], '.3f'))
            time.sleep(10)

    except KeyboardInterrupt:
        if ser != None:
            ser.close()