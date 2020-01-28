from Common.EnumSet import *
from Exceptions.Errors import *


# from GAutils.encode import grayEncodeForList


# def check_parameters(number, bounds):
#     """检查参数是否合法"""
#     if not (isinstance(number, int) or isinstance(number, float)):
#         raise TypeError("输入参数类型错误")
#     if isinstance(bounds, int):
#         if number != bounds:
#             raise IllegalVariableError
#     else:
#         if number < bounds[Bounds.lower] or number > bounds[Bounds.upper]:
#             raise IllegalVariableError
#
#
# def get_interval_length(bounds):
#     """获取区间长度"""
#     return bounds[Bounds.upper] - bounds[Bounds.lower]
#
#
# def fill_zeros(binaryString, intervalLength, decimalDigits):
#     return "0" * (binary_length(intervalLength, decimalDigits) - len(binaryString)) + binaryString


# def decimal_to_binary(number, bounds, decimalDigits = 6):
#     """将数字按精度要求转换到二进制字符串，int->string"""
#     checkParameters(number, bounds)
#     if isinstance(bounds, int):
#         # 如果区间是数字，则该变量恒定为一个值，则直接转换为二进制数，不做处理
#         return int(number, 2)
#     else:
#         # 否则先将区间分成N份，然后将该数字在该区间的为第几份，然后将其转换为二进制数
#         digit = number_to_digit(number, bounds, decimalDigits)
#         pureBinary = numberToBinaryString(digit)  # 0b101
#         intervalLength = interval_length(bounds)
#         pureBinary = "0" * (binary_length(intervalLength, decimalDigits) - len(pureBinary)) + pureBinary
#     return pureBinary


# def number_to_digit(number, bounds, decimalDigits):
#     """将区间分成n份，获取该数字是其中的第几份"""
#     intervalLength = get_interval_length(bounds)
#     subintervalSum = intervalLength * 10 ** decimalDigits
#     precision = intervalLength / subintervalSum
#     digit = int((number - bounds[Bounds.lower]) / precision)
#
#     return digit
#
#
# def binary_length(intervalLength, decimalDigits):
#     """获取能表示该最大份数的二进制数的位数"""
#     digitSum = int(intervalLength*10**decimalDigits + 1)
#     binaryLength = len(number_to_binarystring(digitSum))
#     return binaryLength
#
#
# def number_to_binarystring(binary):
#     """数字型转换为二进制字符串"""
#     return bin(binary).replace("0b", "")
#
#
# def binarystring_to_number(binaryString):
#     """二进制字符串转换为二进制"""
#     return int(binaryString, 2)


# def shear(chromosome, start, end):
#     """染色体剪切: [start,end), 染色体首位下标为1"""
#     chromosomeLength = len(bin(chromosome).replace("0b", ""))
#     m = 2 ** chromosomeLength - 1
#     leftZeros = start - 1
#     rightZeros = chromosomeLength - end
#     mask = (m >> (leftZeros + rightZeros + 1))
#     mask = mask << (leftZeros + 1)
#     return chromosome & mask
#
# def splicing(*chromosomes):
#     """染色体拼接"""
#     finalChromosome = 0
#     for chromosome in chromosomes:
#         finalChromosome = finalChromosome + chromosome
#     return finalChromosome

def shear(chromosome, start, end):
    """染色体剪切: [start,end), 染色体首位下标为1"""
    return chromosome[start:end]


def splicing(*chromosomes):
    """染色体拼接"""
    finalChromosome = ""
    for chromosome in chromosomes:
        finalChromosome += chromosome
    return finalChromosome
