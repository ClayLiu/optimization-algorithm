from Common.utils import *

import Common.EnumSet

import math

def decode(interval, chromosome):
    '''将一个染色体 chromosome 映射为区间 interval 之内的数值'''
    d = interval[1] - interval[0]
    n = float(2 ** 24 - 1)
    return (interval[0] + chromosome * d / n)

print(bin(7))

