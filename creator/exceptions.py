# -*- coding: utf-8 -*-
__author__ = 'lewap'


class IncorrectInputAlphabetError(Exception):
    pass


class InitialStateNotInStates(Exception):
    pass


class IncorrectTransitionError(Exception):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return 'Mistake in transition ' + str(self.val) + '.'


class TapeAlphabetNotSubsetOfWorkingAlphabet(Exception):
    pass


class IncorrectTestCaseError(Exception):
    pass