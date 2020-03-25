from caller import *

boundsList = ((-2 * math.pi, 2 * math.pi), (-2 * math.pi, 2 * math.pi))
objectiveFunction = lambda x, y: x ** 2 + y ** 2 + 25 * (math.sin(x) ** 2 + math.sin(y) ** 2)
constraintFunction = lambda x, y: True
populationSum = 30
iterNum = 1000
extremum=False


c = calculation(objectiveFunction, boundsList, constraintFunction, populationSum, iterNum, extremum=extremum)
c.run()
