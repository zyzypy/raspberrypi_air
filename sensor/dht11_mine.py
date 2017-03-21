# # 【废弃】百度普遍是下面这种写法
# # 优点简单统计。缺点高电平个数统计算法不稳定，二进制转十进制没用现成方法
# from RPi import GPIO
# import time
# """
# 原理详见奥松DHT11说明书
# """
# channel = 18    # BCM4 pin7
# data = []
# j = 0
#
# GPIO.setmode(GPIO.BCM)
#
#
# time.sleep(1)   # 步骤一、传感器上电1s等待电平稳定，传感器检测温湿度并记录数据
#
# GPIO.setup(channel, GPIO.OUT)   # 步骤二 设置IO输出同时低电平，保持18ms以上，传感器检测到低电平后准备发送数据
# time.sleep(0.05)
# GPIO.output(channel, GPIO.LOW)
# time.sleep(0.02)
# GPIO.output(channel, GPIO.HIGH)     # 步骤三 GPIO设置为高电平输入来接收数据
# # 等待回复
# GPIO.setup(channel, GPIO.IN)    # 即板子读这个pin脚的数据
#
# while GPIO.input(channel) == GPIO.LOW:
#     continue
# while GPIO.input(channel) == GPIO.HIGH:
#     continue
#
# # 取数据 ，数据是40bit的
# while j < 40:
#
#     k = 0
#     while GPIO.input(channel) == GPIO.LOW:
#         continue
#     # 根据1的个数（即高电平的时间来判断0 low还是1 high）
#     while GPIO.input(channel) == GPIO.HIGH:
#         k = k + 1
#         if k > 100:
#             break
#     print(j, k)
#     if k < 16:
#         data.append(0)
#     else:
#         data.append(1)
#     j += 1
#
# print(data)
#
# humidity_integer_bit = data[0:8]    # 湿度整数
# humidity_decimal_bit = data[8:16]   # 湿度小数 传感器默认0
# temperature_integer_bit = data[16:24]  # 温度
# temperature_decimal_bit = data[24:32]
# check_bit = data[32:40]     # 校验位
#
# humidity_integer = 0
# humidity_decimal = 0
# temperature_integer = 0
# temperature_decimal = 0
# check = 0
#
# for i in range(8):
#     humidity_integer+=humidity_integer_bit[i]*2**(7-i)
#     humidity_decimal+=humidity_decimal_bit[i]*2**(7-i)
#     temperature_integer+=temperature_integer_bit[i]*2**(7-i)
#     temperature_decimal+=temperature_decimal_bit[i]*2**(7-i)
#     check+=check_bit[i]*2**(7-i)
#
# tmp = humidity_integer+humidity_decimal+temperature_integer+temperature_decimal
# if check == tmp:
#     print('温度:%d  ;湿度：%d' % (humidity_integer, temperature_integer))
# else:
#     print('错误')
# print(humidity_integer,temperature_integer)
#
# GPIO.cleanup()
#
#
#
