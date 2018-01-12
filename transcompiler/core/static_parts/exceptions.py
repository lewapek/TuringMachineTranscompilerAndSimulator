# -*- coding: utf-8 -*-


class NoSuchSymbolError(Exception):
    def __init__(self, character=None):
        self.character = character

    def __str__(self):
        msg = "Unexpected (out of tape alphabet) character on tape."
        if self.character:
            return msg + " Found: '" + self.character + "'."
        return msg
