from type_collection.ast import Expr, ExprKind
from type_collection.ir import Temp, IrNode, IrNodeKind

class IrGenerator:

    def __init__(self):
        self._next_temp = Temp(0)
        self._ir_seq = []

    def gen_ir(self, expr: Expr):
        temp = self._gen_expr(expr)
        self._add_node(IrNode(IrNodeKind.Return, arg1=temp))
        return self._ir_seq

    def _gen_expr(self, expr: Expr):
        if expr.is_binop():
            temp1 = self._gen_expr(expr.lhs)
            temp2 = self._gen_expr(expr.rhs)
            if expr.exp_kind == ExprKind.ADD:
                ir = IrNode(IrNodeKind.Add, temp1, temp2)
            elif expr.exp_kind == ExprKind.SUB:
                ir = IrNode(IrNodeKind.Sub, temp1, temp2)
            elif expr.exp_kind == ExprKind.MUL:
                ir = IrNode(IrNodeKind.Mul, temp1, temp2)
            elif expr.exp_kind == ExprKind.DIV:
                ir = IrNode(IrNodeKind.Div, temp1, temp2)
            self._add_node(ir)
            self._add_node(IrNode(IrNodeKind.Kill, arg1=temp2))
            return temp1
        else:
            temp = self._new_temp()
            ir = IrNode(IrNodeKind.Imm, temp, expr.value)
            self._add_node(ir)
            return temp

    def _add_node(self, ir_node: IrNode):
        self._ir_seq.append(ir_node)

    def _new_temp(self):
        temp = self._next_temp
        next_num = temp.num + 1
        self._next_temp = Temp(next_num)
        return temp