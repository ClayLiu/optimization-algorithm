from GAutils.utils import *


def binaryEncode(number, bounds, decimalDigits = 6):
    """
    :param boundLists: 区间列表-> 25 or [10, 14]
    :param decimalDigits: 小数位数，希望精确到的位数,输入数字如果超过该精度，后面的将会被忽略
    :param number:希望转换的数字
    :return:
    """
    return decimal_to_binary(number, bounds, decimalDigits)


def grayEncode(number, bounds, decimalDigits = 6):
    binary = int("0b" + binaryEncode(number, bounds, decimalDigits), 2)
    print("binary:"+bin(binary))
    gray = binary ^ (binary >> 1)
    grayString = bin(gray).replace("0b", "")
    return grayString


print("gray:"+grayEncode(3.111111, [0, 99]))

