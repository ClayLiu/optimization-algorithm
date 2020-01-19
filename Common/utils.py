from inspect import isfunction
from Exceptions.Errors import *
from Common.EnumSet import Bounds


def inspectors(variablesList, boundsList, constraintFunction):

    # 检查变量间是否符合约束
    if isfunction(constraintFunction):
        if not constraintFunction(*variablesList):
            raise ViolatedConstraintError
    else:
        for constraintfunction in constraintFunction:
            if not constraintfunction(*variablesList):
                raise ViolatedConstraintError

    # 检查单个变量是否符合约束
    if len(variablesList) != len(boundsList):
        raise MismatchError
    for index, dimensionBounds in enumerate(boundsList):
        if isinstance(dimensionBounds, int):
            if variablesList[index] != dimensionBounds:
                raise IllegalVariableError
        else:
            if variablesList[index] < dimensionBounds[Bounds.lower.value] or variablesList[index] > dimensionBounds[Bounds.upper.value]:
                raise IllegalVariableError
