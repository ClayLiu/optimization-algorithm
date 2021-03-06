from inspect import isfunction
from Exceptions.Errors import *
from Common.EnumSet import Bounds
import numpy as np
import sys
import configparser


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
            if variablesList[index] < dimensionBounds[Bounds.lower] or variablesList[index] > dimensionBounds[Bounds.upper]:
                raise IllegalVariableError


def generate_individual(boundsList, constraintFunction):
    while True:
        singlePosition = []
        for index, dimensionBounds in enumerate(boundsList):
            if isinstance(dimensionBounds, int):
                singlePosition.append(dimensionBounds)
            else:
                singlePosition.append(np.random.rand()*(dimensionBounds[Bounds.upper] - dimensionBounds[Bounds.lower]) + dimensionBounds[Bounds.lower])
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
    # populationPositions = np.array(positions)
    populationPositions = positions
    return populationPositions


def convert_position_to_legal(position, boundsLists):
    for index, var in enumerate(position):
        if isinstance(boundsLists[index], int):
            if var != boundsLists[index]:
                position[index] = boundsLists[index]
        else:
            if var < boundsLists[index][Bounds.lower]:
                position[index] = boundsLists[index][Bounds.lower]
            elif var > boundsLists[index][Bounds.upper]:
                position[index] = boundsLists[index][Bounds.upper]

    return position


def read_config(node,point):
    config = configparser.ConfigParser()
    config.read("/workplace/personalProjects/algorithm modules/optimization-algorithm/resources/config.ini")
    return config[node][point]
