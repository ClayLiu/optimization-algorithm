from Common.EnumSet import *
from GAutils.utils import *


def binaryDecode(binaryString, bounds, decimalDigits = 6):
    """二进制编码的解码"""
    digit = int(binaryString, 2)
    intervalLength = interval_length(bounds)
    subintervalSum = intervalLength * 10 ** decimalDigits
    number = bounds[Bounds.lower] + digit*intervalLength/subintervalSum
    return number


def grayDecode(grayString, bounds, decimalDigits = 6):
    """格雷码解码"""
    binaryString = grayString[0]
    for i, number in enumerate(grayString):
        if i != 0:
            if number == binaryString[i-1]:
                binaryString = binaryString + "0"
            else:
                binaryString = binaryString + "1"
    return binaryDecode(binaryString, bounds, decimalDigits)

print(grayDecode("1110001100010010100100",[0,99]))