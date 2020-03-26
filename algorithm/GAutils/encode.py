from Exceptions.Errors import *


class Encode:
    def __init__(self, boundsLists, decimalDigits):
        self.boundsLists = boundsLists
        self.decimalDigits = decimalDigits

    def get_interval_length(self, bounds):
        """获取区间长度"""
        return bounds[0] - bounds[1]

    def binaryEncode(self, number, bounds):
        """根据区间将数字转换到二进制字符串，int->String"""
        self.check_parameters(number, bounds)
        if isinstance(bounds, int):
            # 如果区间是数字，则该变量恒定为一个值，则直接转换为二进制数，不做处理
            return int(number, 2)
        else:
            # 否则先将区间分成N份，然后将该数字在该区间的为第几份，然后将其转换为二进制数
            digit = self.number_to_digit(number, bounds)
            pureBinary = self.num_to_binstr(digit)  # 101
            finalBinary = self.fill_zeros(pureBinary, self.get_interval_length(bounds))
        return finalBinary

    def grayEncode(self, number, bounds):
        """根据区间将数字转换到二进制字符串，int->String"""
        binaryString = self.binaryEncode(number, bounds)
        binary = self.binstr_to_num(binaryString)
        gray = binary ^ (binary >> 1)
        pureGray = self.num_to_binstr(gray)
        finalGray = self.fill_zeros(pureGray, self.get_interval_length(bounds))
        return finalGray

    def grayListEncode(self, numberList):
        grayEncodeList = []
        for i, number in enumerate(numberList):
            grayEncodeList.append(self.grayEncode(number, self.boundsLists[i]))
        return grayEncodeList

    def binaryListEncode(self, numberList):
        binaryEncodeList = []
        for i, number in enumerate(numberList):
            binaryEncodeList.append(self.binaryEncode(number, self.boundsLists[i]))
        return binaryEncodeList

    def number_to_digit(self, number, bounds):
        """将区间分成n份，获取该数字是其中的第几份"""
        intervalLength = self.get_interval_length(bounds)
        subintervalSum = intervalLength * 10 ** self.decimalDigits
        precision = intervalLength / subintervalSum
        digit = int((number - bounds[0]) / precision)

        return digit

    def check_parameters(self, number, bounds):
        """检查参数是否合法"""
        if not (isinstance(number, int) or isinstance(number, float)):
            raise TypeError("输入参数类型错误")
        if isinstance(bounds, int):
            if number != bounds:
                raise IllegalVariableError
        else:
            if number < bounds[0] or number > bounds[1]:
                raise IllegalVariableError

    def fill_zeros(self, binaryString, intervalLength):
        return "0" * (self.bin_max_length(intervalLength) - len(binaryString)) + binaryString

    def bin_max_length(self, intervalLength):
        """获取能表示该最大份数的二进制数的位数"""
        digitSum = int(intervalLength * 10 ** self.decimalDigits + 1)
        binaryLength = len(self.num_to_binstr(digitSum))
        return binaryLength

    def num_to_binstr(self, number):
        return bin(number).replace("0b", "")

    def binstr_to_num(self, binstr):
        """二进制字符串转换为整数"""
        return int(binstr, 2)
