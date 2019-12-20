from enum import Enum

class ExprKind(Enum):
    ADD = "Add"
    SUB = "Sub"
    MUL = "Mul"
    DIV = "Div"
    NUM = "Number"

class Expr:
    def __init__(self, exp_kind: ExprKind, lhs=None, rhs=None, value=None):
        self._exp_kind = exp_kind
        self._lhs = lhs
        self._rhs = rhs
        self._value = value

    def __repr__(self):
        if self._exp_kind == ExprKind.NUM:
            return "<value-{}>".format(self._value)
        else:
            return "<kind-{}-(left-{})-(right-{})>".format(self._exp_kind, self._lhs, self._rhs)
    
    @property
    def exp_kind(self):
        return self._exp_kind

    @property
    def lhs(self):
        return self._lhs

    @property
    def rhs(self):
        return self._rhs

    @property
    def value(self):
        return self._value

    def is_binop(self):
        return self._exp_kind in [ExprKind.ADD, ExprKind.SUB, ExprKind.MUL, ExprKind.DIV]