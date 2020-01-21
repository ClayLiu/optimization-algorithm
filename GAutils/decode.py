from Common.EnumSet import *
from GAutils.utils import *


def binaryDecode(binaryNumber, bounds, decimalDigits = 6):
    """二进制编码到解码"""
    digit = int(binaryNumber, 2)
    intervalLength = interval_length(bounds)
    subintervalSum = intervalLength * 10 ** decimalDigits
    precision = intervalLength / subintervalSum
    number = bounds[Bounds.lower] + digit*precision
    return number

print(binaryDecode("110011000001011000011000000", [-10,99]))