from typing import List

from type_collection.ir import IrNode, IrNodeKind, Temp

REG64 = ["r10", "r11", "rbx", "r12", "r13", "r14", "r15"]


class RegAllocator:
    def __init__(self):
        self._reg_map = {}
        self._in_use = [False] * len(REG64)

    def allocate(self, ir_nodes: List[IrNode]):
        for node in ir_nodes:
            if node.nodekind in [
                    IrNodeKind.Add, IrNodeKind.Div, IrNodeKind.Sub,
                    IrNodeKind.Mul
            ]:
                self._alloc_new(node.arg1)
                self._alloc_new(node.arg2)
            elif node.nodekind in [IrNodeKind.Return, IrNodeKind.Imm]:
                self._alloc_new(node.arg1)
            elif node.nodekind == IrNodeKind.Kill:
                reg_id = self._reg_map[node.arg1]
                self._in_use[reg_id] = False
            elif node.nodekind == IrNodeKind.Nop:
                continue

    def reg_name(self, temp: Temp):
        return REG64[self._reg_map[temp]]

    def _alloc_new(self, temp: Temp):
        for reg in self._reg_map:
            if reg == temp:
                return

        for i, in_use in enumerate(self._in_use):
            if in_use is False:
                self._reg_map[temp] = i
                self._in_use[i] = True
                return
