class IllegalVariableError(Exception):

    def __init__(self):
        self.info = "变量不符合约束条件"


class ViolatedConstraintError(Exception):

    def __init__(self):
        self.info = "变量间关系不符合约束条件"


class MismatchError(Exception):

    def __init__(self):
        self.info = "变量和区间不匹配"


