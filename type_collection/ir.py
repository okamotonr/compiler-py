from enum import Enum, auto

class Temp():
    def __init__(self, num):
        self._num = num

    @property
    def num(self):
        return self._num

class IrNodeKind(Enum):
    Imm = auto()
    Mov = auto()
    Add = auto()
    Sub = auto()
    Mul = auto()
    Div = auto()
    Kill = auto()
    Return = auto()
    Nop = auto()

class IrNode:
    def __init__(self, nodekind: IrNodeKind, arg1=None, arg2=None):
        self._nodekind = nodekind
        self._arg1 = arg1
        self._arg2 = arg2

    @property
    def nodekind(self):
        return self._nodekind

    @property
    def arg1(self):
        return self._arg1

    @property
    def arg2(self):
        return self._arg2