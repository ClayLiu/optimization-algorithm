from GAutils.utils import *


def binaryEncode(number, bounds, decimalDigits = 6):
    """
    :param boundLists: 区间列表-> [25,[10,20],[10,20]]
    :param decimalDigits: 小数位数，希望精确到的位数,输入数字如果超过该精度，后面的将会被忽略
    :param number:希望转换的数字
    :return:
    """
    return decimal_to_binary(number, bounds, decimalDigits)


# print(binaryEncode(67, [1, 99]))


