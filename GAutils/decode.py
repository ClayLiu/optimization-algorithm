from Common.EnumSet import *
from GAutils.utils import *


def binaryDecode(binary, bounds, decimalDigits = 6):
    """二进制编码的解码"""
    intervalLength = interval_length(bounds)
    subintervalSum = intervalLength * 10 ** decimalDigits
    number = bounds[Bounds.lower] + binary*intervalLength/subintervalSum
    return number


def grayDecode(gray, bounds, decimalDigits = 6):
    """格雷码解码"""
    grayString = bin(gray).replace("0b", "")
    binaryString = grayString[0]
    for i, number in enumerate(grayString):
        if i != 0:
            if number == binaryString[i-1]:
                binaryString = binaryString + "0"
            else:
                binaryString = binaryString + "1"
    binary = int("0b" + binaryString, 2)
    return binaryDecode(binary, bounds, decimalDigits)


def grayDecodeFromList(grayList,boundsList,decimalDigits = 6):
    """grayList中的gray为二进制数但是在数组中以整数型显示->[6260971, 7476972]，可以直接进行二进制数的取反等操作"""
    decodeList = []
    for i, gray in enumerate(grayList):
        decodeList.append(grayDecode(gray, boundsList[i], decimalDigits))

    return decodeList

