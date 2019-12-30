from enum import Enum


class TokenKind(Enum):
    PLUS = "+"
    MINOS = "-"
    STAR = "*"
    SLASH = "/"
    LPAREN = "("
    RPAREN = ")"
    NUM = "number"


class Token:
    def __init__(self, token_kind: TokenKind, index: int, value=None):
        self._token_kind = token_kind
        self._value = value
        self._index = index

    @property
    def token_kind(self):
        return self._token_kind

    @property
    def index(self):
        return self._index

    @property
    def value(self):
        if self._value is None:
            raise ValueError
        return self._value
