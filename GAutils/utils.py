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


def decimal_to_binary(number, bounds, decimalDigits = 6):
    """将数字按精度要求转换到二进制数"""
    checkParameters(number, bounds)
    if isinstance(bounds, int):
        # 如果区间是数字，则该变量恒定为一个值，则直接转换为二进制数，不做处理
        return bin(number).replace("0b", "")
    else:
        # 否则先将区间分成N份，然后将该数字在该区间的为第几份，然后将其转换为二进制数
        digit = number_to_digit(number, bounds, decimalDigits)
        binary = bin(digit)  # 0b101
        interval_length = get_interval_length(bounds)
        binary = binary.replace("0b", "0" * (get_binary_length(interval_length, decimalDigits) - 2))
    return binary


def number_to_digit(number, bounds, decimalDigits):
    """将区间分成n份，获取该数字是其中的第几份"""
    intervalLength = get_interval_length(bounds)
    subintervalSum = intervalLength*10**decimalDigits
    precision = intervalLength / subintervalSum
    return int((number - bounds[Bounds.lower]) / precision)


def get_binary_length(intervalLength, decimalDigits):
    """获取转换的二进制数的位数"""
    digitSum = intervalLength*10**decimalDigits + 1
    n = 2
    binaryLength = 1
    while True:
        if digitSum < n:
            break
        else:
            n = n << 1
            binaryLength = binaryLength + 1
    return binaryLength


def get_interval_length(bounds):
    """获取区间长度"""
    return bounds[Bounds.upper] - bounds[Bounds.lower]
