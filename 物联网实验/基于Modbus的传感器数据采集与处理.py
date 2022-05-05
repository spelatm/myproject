import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

from binascii import *
import crcmod


# 生成CRC16-MODBUS校验码
def crc16Add(read):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "")  # 消除空格
    readcrcout = hex(crc16(unhexlify(data))).upper()
    str_list = list(readcrcout)
    # print(str_list)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
    crc_data = "".join(str_list)  # 用""把数组的每一位结合起来  组成新的字符串
    # print(crc_data)
    read = read.strip() + ' ' + crc_data[4:] + ' ' + crc_data[2:4]  # 把源代码和crc校验码连接起来
    # print('CRC16校验:', crc_data[4:] + ' ' + crc_data[2:4])
    print(read)
    return read

#
# if __name__ == '__main__':
#     crc16Add("01 06 00 66 00 C8 AA 00")
#

# # 设定串口为从站
# master = modbus_rtu.RtuMaster(serial.Serial(port="COM1",
#                                             baudrate=9600, bytesize=8, parity='N', stopbits=1))
# master.set_timeout(5.0)

def what_to_do(x):
    '"02 03 00 00 00 03"其中02表示设备地址，即站号，03表示读寄存器命令，“00 00”表示寄存器起始地址，“00 03”表示寄存器数量。'
    '"02 06 00 03 00 FE"其中02表示设备地址，即站号，06表示设置单个寄存器命令，“00 03”表示寄存器起始地址，“00 FE”表示要设置的值'
    if int(x[2:4], 16) == 6:
        master.execute(int(x[0:2], 16), cst.WRITE_SINGLE_REGISTER, int(x[4:8], 16), output_value=int(x[8:], 16))#写入寄存器的操作，站号为1，对7号寄存器，写入值500
        crc16Add(x)

    if int(x[2:4], 16) == 3:
        out1 = master.execute(int(x[0:2], 16), cst.READ_HOLDING_REGISTERS, int(x[4:8], 16), int(x[8:], 16))  # 读寄存器的操作，站号为1，从2号寄存器开始，往后读5个
        print(out1)
        crc16Add(x)

# master.execute(1, cst.WRITE_SINGLE_REGISTER, 7, output_value=500)#写入寄存器的操作，站号为1，对7号寄存器，写入值500
#
# out1 = master.execute(1, cst.READ_COILS, 2, 5)#读寄存器的操作，站号为1，从2号寄存器开始，往后读5个

if __name__ == '__main__':
    # 设定串口为从站
    master = modbus_rtu.RtuMaster(serial.Serial(port="COM1",
                                                baudrate=9600, bytesize=8, parity='N', stopbits=1))
    master.set_timeout(5.0)
    while True:
        x = input()
        what_to_do(x)