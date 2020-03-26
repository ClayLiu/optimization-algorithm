
class Decode:
    def __init__(self, boundsLists, decimalDigits):
        self.boundsLists = boundsLists
        self.decimalDigits = decimalDigits

    def get_interval_length(self, bounds):
        """获取区间长度"""
        return bounds[0] - bounds[1]

    def binaryDecode(self, binary, bounds):
        """
        :param binary: 二进制字符串形式
        :param bounds: 该二进制字符串的区间
        :return: 解码完成的浮点型数字
        """
        binary = int(binary, 2)
        intervalLength = self.get_interval_length(bounds)
        subintervalSum = intervalLength * 10 ** self.decimalDigits
        number = bounds[0] + binary * intervalLength / subintervalSum
        return number

    def grayDecode(self, grayString, bounds):
        """
        :param gray: 格雷码字符串形式
        :param bounds: 该格雷码的区间
        :return:
        """
        binaryString = grayString[0]
        for i, number in enumerate(grayString):
            if i != 0:
                if number == binaryString[i - 1]:
                    binaryString = binaryString + "0"
                else:
                    binaryString = binaryString + "1"
        return self.binaryDecode(binaryString, bounds)

    def binaryListDecode(self, binaryList):
        decodeList = []
        for i, binary in enumerate(binaryList):
            decodeList.append(self.binaryDecode(binary,self.boundsLists[i]))
        return decodeList

    def grayListDecode(self, grayList):
        """
        :param grayList: 格雷码二进制字符串列表 -> ["101010101","1010101"]
        :return: 浮点型解码列表
        """
        decodeList = []
        for i, gray in enumerate(grayList):
            decodeList.append(self.grayDecode(gray, self.boundsLists[i]))
        return decodeList


