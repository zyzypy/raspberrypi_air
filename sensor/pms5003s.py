# coding=utf-8
"""
# 攀藤PMS5003s pm2.5甲醛二合一传感器 驱动
# 说明书http://wenku.baidu.com/link?url=72hZ2hqKo9uSpKRGjQxRYEJE3lPApwmtrrBpL0ZFNSOnOFAvTta3DL2yMb_iEEiN9AnXspcWBHwXMA5NfvxxnwIY0YakrHfuo9gN2KTFmyi
@author yangzheng
"""
import serial
import time


def get_results(ser):

    """ 从串口缓冲区读取设备发过来的数据
    """
    count = 0
    while count < 64:
        # 必要的软件延迟。否则刚打开串口设备数据还没进来，ser.inWaiting()为空。设备每0.2-0.8s传一次32字节结果数据，
        # 可以在ser = serial.Serial("/dev/ttyUSB0", 9600)后给time.sleep(2)然后再ser.read()，也可以while True循环read()部分，
        # sleep(1)能接受到1-2次数据集，再根据flag字节截取一次的32字节结果
        time.sleep(0.2)
        # 缓冲区已收到的数据字节个数
        count = ser.inWaiting()
        # print(count)

    # 读取数据
    try:
        recv_bytes = ser.read(count)
    except serial.SerialException:
        return '-1'
    recv_bytes_arr = bytearray(recv_bytes)      # 字节转字节数组才能操作
    # print('bytes length：', len(recv_bytes_arr), 'data：', recv_bytes_arr)

    BYTE_LENGTH = ''
    byte_flag_1 = False
    byte_flag_2 = False

    recv_decimal = []

    for i, byte in enumerate(recv_bytes_arr):
        """ 遍历字节组 转成16进制放入recv_hex
            根据起始字节截取一条32字节结果数据
            2字节起始符+2字节帧长度+13组*2字节数据+2字节校验=32
        """
        if byte_flag_1 is False:
            # debug时字节显示是10进制数字，print（byte）时控制台输出显示是按照ascii和16进制编出来的字符（这里略歧义）。字节本质是二进制数字，所以先处理成16进制为了后面处理。
            # hex()返回类型字符串。二进制>16进制>编码字符。数字到字符为编码，字符到数字为解码，说白了是数字到信息的映射关系。
            if hex(byte) == '0x42':    # 起始字节1  BYTE_FLAG_1为true时 continue到下一次循环，下一次的hex（byte）预计等于BYTE_FLAG_2
                byte_flag_1 = True
                recv_decimal.append(int(byte))
                continue
            else:
                continue

        if byte_flag_2 is False:        # 起始字节2
            if hex(byte) == '0x4d':
                byte_flag_2 = True
                recv_decimal.append(int(byte))
                continue
            else:
                byte_flag_1 = False     # 如果不等于BYTE_FLAG_2，说明前一次的BYTE_FLAG_1是数据位恰好相等 并不是起始符1
                continue

        if byte_flag_2 is True:         # 起始2字节 帧长度2字节值应该为28 固定所以写死，有校验不怕出问题。所以除了起始2字节，向后取30字节
            recv_decimal.append(int(byte))
            if i == 31:
                break

    # print('recv_decimal', recv_decimal, len(recv_decimal))

    # 校验。校验码=起始符1+起始符2+……..+数据13低八位 前面30个字节的和
    check_code = recv_decimal[-2]*256 + recv_decimal[-1]   # <<8相当于*256 移位运算符优先级低注意括号 校验位高低各8位两字节
    bytes_sum = sum(recv for recv in recv_decimal[0:-2])     # 除校验位其它30字节累加

    if check_code == bytes_sum:
        pass
    else:
        return '-1' # 校验错误


    # 取大气环境模式 数据，工厂模式的颗粒按金属算值会偏大
    # 每个数据两字节，数据前起始符和帧数量占4字节

    results = dict()
    results['pm1dot0'] = recv_decimal[10]*256 + recv_decimal[11]        # PM1.0 对应传感器文档数据4 即4+2*4 第11、12字节 对应数组下标10、11 单位ug/m3
    results['pm2dot5'] = recv_decimal[12]*256 + recv_decimal[13]        # 数据5
    results['pm10dot0'] = recv_decimal[14]*256 + recv_decimal[15]       # 数据6

    results['particulate0dot3'] = recv_decimal[16]*256 + recv_decimal[17]   # 0.3um以上颗粒  数据7 单位个
    results['particulate0dot5'] = recv_decimal[18]*256 + recv_decimal[19]   # 数据8
    results['particulate1dot0'] = recv_decimal[20]*256 + recv_decimal[21]   # 数据9
    results['particulate2dot5'] = recv_decimal[22]*256 + recv_decimal[23]   # 数据10
    results['particulate5dot0'] = recv_decimal[24]*256 + recv_decimal[25]   # 数据11
    results['particulate10dot0'] = recv_decimal[26]*256 + recv_decimal[27]   # 数据12

    results['formaldehyde'] = (recv_decimal[28]*256 + recv_decimal[29])/1000       # 甲醛 数据13 得数除1000 单位mg/m3

    # print('pm2.5: %d ug/m3' % results['pm2dot5'], 'formaldehyde: %s mg/m3' % format(results['formaldehyde'], '.3f'))

    # 清空接收缓冲区
    ser.flushInput()

    return results




