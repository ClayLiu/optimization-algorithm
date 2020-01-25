from GAutils.utils import *


def binaryEncode(number, bounds, decimalDigits = 6):
    """根据区间将数字转换到二进制字符串，int->String"""
    check_parameters(number, bounds)
    if isinstance(bounds, int):
        # 如果区间是数字，则该变量恒定为一个值，则直接转换为二进制数，不做处理
        return int(number, 2)
    else:
        # 否则先将区间分成N份，然后将该数字在该区间的为第几份，然后将其转换为二进制数
        digit = number_to_digit(number, bounds, decimalDigits)
        pureBinary = number_to_binarystring(digit)  # 101
        finalBinary = fill_zeros(pureBinary, get_interval_length(bounds), decimalDigits)
    return finalBinary


def grayEncode(number, bounds, decimalDigits = 6):
    """根据区间将数字转换到二进制字符串，int->String"""
    binaryString = binaryEncode(number, bounds, decimalDigits)
    binary = binarystring_to_number(binaryString)
    gray = binary ^ (binary >> 1)
    pureGray = number_to_binarystring(gray)
    finalGray = fill_zeros(pureGray, get_interval_length(bounds), decimalDigits)
    return finalGray


# def grayEncodeForList(numberList, boundsList, decimalDigits = 6):
#     grayEncodeList = []
#     if isinstance(numberList, list) or isinstance(numberList, tuple):
#         for i, number in enumerate(numberList):
#             grayEncodeList.append(grayEncode(number, boundsList[i], decimalDigits))
#     else:
#         raise TypeError("参数类型错误！")
#
#     return grayEncodeList

def grayEncodeForList(numberList, boundsList, decimalDigits = 6):
    grayEncodeList = []
    if isinstance(numberList, list) or isinstance(numberList, tuple):
        for i, number in enumerate(numberList):
            grayEncodeList.append(grayEncode(number, boundsList[i], decimalDigits))
    else:
        raise TypeError("参数类型错误！")

    return grayEncodeList
