from Common.utils import *

import Common.EnumSet

import math
from bitarray import *

def decode(interval, chromosome):
    '''将一个染色体 chromosome 映射为区间 interval 之内的数值'''
    d = interval[1] - interval[0]
    n = float(2 ** 24 - 1)
    return (interval[0] + chromosome * d / n)

# print(bin(7))
# print(bin(int("0b111",2)+int("0b111", 2)))

# a=bitarray("101")
# b=bitarray("101")
print(np.array([int("0b101",2)]))
# print(b)