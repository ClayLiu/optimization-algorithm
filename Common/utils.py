from inspect import isfunction
from Exceptions.Errors import *
from Common.EnumSet import Bounds
import numpy as np
import sys


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


def generate_individual(boundsList, constraintFunction):
    while True:
        singlePosition = []
        for index, dimensionBounds in enumerate(boundsList):
            if isinstance(dimensionBounds, int):
                singlePosition.append(dimensionBounds)
            else:
                singlePosition.append(np.random.rand()*(dimensionBounds[Bounds.upper.value] - dimensionBounds[Bounds.lower.value]) + dimensionBounds[Bounds.lower.value])
        try:
            inspectors(singlePosition, boundsList, constraintFunction)
        except IllegalVariableError as e:
            continue
        except ViolatedConstraintError as e:
            continue
        break
    return singlePosition


def generate_population(populationQuantity, boundsList, constraintFunction):
    positions = []
    for i in range(populationQuantity):
        try:
            positions.append(generate_individual(boundsList, constraintFunction))
        except MismatchError as e:
            print(e.info)
            sys.exit(1)
    populationPositions = np.array(positions)
    return populationPositions
