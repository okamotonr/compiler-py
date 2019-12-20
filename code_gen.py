from typing import List

from reg_alloc import RegAllocator
from type_collection.ir import IrNodeKind, IrNode

class CodeGenerator:
    def __init__(self):
        self._allocator = RegAllocator()
        self._asm = ""

    def gen_code(self, ir_nodes: List[IrNode]):
        self._allocator.allocate(ir_nodes)
        for node in ir_nodes:
            self.gen_expr(node)
        
        self._zero_arity("ret")

        return self._asm

    def gen_expr(self, node: IrNode):
        if node.nodekind == IrNodeKind.Imm:
            self._two_arity("mov", self._reg_name(node.arg1), node.arg2)
        elif node.nodekind == IrNodeKind.Mov:
            self._two_arity("mov", self._reg_name(node.arg1), self._reg_name(node.arg2))
        elif node.nodekind == IrNodeKind.Add:
            self._two_arity("add", self._reg_name(node.arg1), self._reg_name(node.arg2))
        elif node.nodekind == IrNodeKind.Sub:
            self._two_arity("sub", self._reg_name(node.arg1), self._reg_name(node.arg2))
        elif node.nodekind == IrNodeKind.Mul:
            self._two_arity("mov", "rax", self._reg_name(node.arg2))
            self._one_arity("imul", self._reg_name(node.arg1))
            self._two_arity("mov", self._reg_name(node.arg1), "rax")
        elif node.nodekind == IrNodeKind.Div:
            self._two_arity("mov", "rax", self._reg_name(node.arg1))
            self._zero_arity("cqo")
            self._one_arity("idiv", self._reg_name(node.arg2))
            self._two_arity("mov", self._reg_name(node.arg1), "rax")
        elif node.nodekind == IrNodeKind.Return:
            self._two_arity("mov", "rax", self._reg_name(node.arg1))
        else:
            return


    def _zero_arity(self, code):
        self._asm += "  {}\n".format(code)

    def _one_arity(self, code, lhs):
        self._asm += "  {} {}\n".format(code, lhs)

    def _two_arity(self, code, lhs, rhs):
        self._asm += "  {} {}, {}\n".format(code, lhs, rhs)

    def _reg_name(self, temp):
        return self._allocator.reg_name(temp)

