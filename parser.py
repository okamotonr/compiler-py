from typing import List, Union
from enum import Enum

from type_collection.tokens import Token, TokenKind
from type_collection.ast import Expr, ExprKind


class Parser:
    def __init__(self, token_stream: List[Token]):
        self._index = 0
        self._token_stream = token_stream
        self._end = len(self._token_stream)

    def parser(self):
        return self.exper()

    def exper(self):
        expr = self.term()
        return expr

    def term(self):
        lhs = self.factor()
        while not self._is_finished():
            if self._token_stream[self._index].token_kind == TokenKind.PLUS:
                self._index += 1
                rhs = self.factor()
                lhs = Expr(ExprKind.ADD, lhs, rhs)
            elif self._token_stream[self._index].token_kind == TokenKind.MINOS:
                self._index += 1
                rhs = self.factor()
                lhs = Expr(ExprKind.SUB, lhs, rhs)
            else:
                break

        return lhs

    def factor(self):
        lhs = self.prime()
        while not self._is_finished():
            if self._token_stream[self._index].token_kind == TokenKind.STAR:
                self._index += 1
                rhs = self.prime()
                lhs = Expr(ExprKind.MUL, lhs, rhs)
            elif self._token_stream[self._index].token_kind == TokenKind.SLASH:
                self._index += 1
                rhs = self.prime()
                lhs = Expr(ExprKind.DIV, lhs, rhs)
            else:
                break

        return lhs

    def prime(self):

        token = self._token_stream[self._index]

        if token.token_kind == TokenKind.NUM:
            expr = Expr(ExprKind.NUM, value=token.value)
            self._index += 1
        elif token.token_kind == TokenKind.LPAREN:
            self._index += 1
            r_parlen_index = self.find_parlen()
            if r_parlen_index is None:
                raise ValueError

            parser = self.copy(self._index, r_parlen_index)
            expr = parser.exper()
            self._index = r_parlen_index + 1

        return expr

    def find_parlen(self):
        count = 0
        index = self._index
        ret = None
        while not (index == self._end):
            token = self._token_stream[index]
            if token.token_kind == TokenKind.LPAREN:
                count += 1
            elif token.token_kind == TokenKind.RPAREN:
                if count == 0:
                    ret = index
                    break
                else:
                    count -= 1
            index += 1

        return ret

    def copy(self, start: int, end: int):
        in_parlen = self._token_stream[start:end]
        return Parser(in_parlen)

    def _is_finished(self):
        return self._index == self._end
