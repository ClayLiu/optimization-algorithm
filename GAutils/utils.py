from Common.EnumSet import *
from Exceptions.Errors import *


def checkParameters(number, bounds):
    """检查参数是否合法"""
    if not (isinstance(number, int) or isinstance(number, float)):
        raise TypeError("输入参数类型错误")
    if isinstance(bounds, int):
        if number != bounds:
            raise IllegalVariableError
    else:
        if number < bounds[Bounds.lower] or number > bounds[Bounds.upper]:
            raise IllegalVariableError


def interval_length(bounds):
    """获取区间长度"""
    return bounds[Bounds.upper] - bounds[Bounds.lower]


def decimal_to_binary(number, bounds, decimalDigits = 6):
    """将数字按精度要求转换到二进制数"""
    checkParameters(number, bounds)
    if isinstance(bounds, int):
        # 如果区间是数字，则该变量恒定为一个值，则直接转换为二进制数，不做处理
        return bin(number).replace("0b", "")
    else:
        # 否则先将区间分成N份，然后将该数字在该区间的为第几份，然后将其转换为二进制数
        digit = number_to_digit(number, bounds, decimalDigits)
        pureBinary = bin(digit).replace("0b", "")  # 0b101
        intervalLength = interval_length(bounds)
        pureBinary = "0" * (binary_length(intervalLength, decimalDigits) - len(pureBinary)) + pureBinary
    return pureBinary


def number_to_digit(number, bounds, decimalDigits):
    """将区间分成n份，获取该数字是其中的第几份"""
    intervalLength = interval_length(bounds)
    subintervalSum = intervalLength * 10 ** decimalDigits
    precision = intervalLength / subintervalSum
    digiit = int((number - bounds[Bounds.lower]) / precision)

    return digiit


def binary_length(intervalLength, decimalDigits):
    """获取能表示该最大份数的二进制数的位数"""
    digitSum = intervalLength*10**decimalDigits + 1
    binaryLength = len(bin(digitSum).replace("0b", ""))
    return binaryLength



