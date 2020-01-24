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
    binary = binaryEncode(number, bounds, decimalDigits)
    gray = binary ^ (binary >> 1)
    return gray


def grayEncodeForList(numberList, boundsList, decimalDigits = 6):
    grayEncodeList = []
    if isinstance(numberList, list) or isinstance(numberList, tuple):
        for i, number in enumerate(numberList):
            grayEncodeList.append(grayEncode(number, boundsList[i], decimalDigits))
    else:
        raise TypeError("参数类型错误！")

    return grayEncodeList
