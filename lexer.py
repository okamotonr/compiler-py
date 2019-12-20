from typing import List, Union

from type_collection.tokens import Token, TokenKind

class Lexer:
    def __init__(self, code: str):
        self._index = 0
        self._code = code
        self._end = len(code)

    def tokenize(self):
        token_stream = []
        while not self._is_finised():
            char = self._code[self._index]
            if char.isdigit():
                token = self._digit()
                token_stream.append(token)
            elif char in ["+", "-", "/", "*", "(", ")"]:
                token_kind = TokenKind(char)
                token = Token(token_kind, self._index)
                token_stream.append(token)
                self._index += 1
            else:
                self._index += 1

        return token_stream

    def _digit(self):
        value = ""
        index = self._index
        while True:
            char = self._code[self._index]
            if not char.isdigit():
                break
            value += char
            self._index += 1
        token_kind = TokenKind.NUM
        token = Token(token_kind, index, value=int(value))
        return token

    def _is_finised(self):
        return self._index == self._end


