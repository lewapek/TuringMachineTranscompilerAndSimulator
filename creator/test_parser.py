from creator.exceptions import IncorrectTestCaseError

__author__ = 'lewap'


true_signs = ('Y', 'y', 'A', 'a', '+')
false_signs = ('N', 'n', 'R', 'r', '-')


def parse(content):
    result = []
    content = content.split('\n')
    for c in content:
        splitted = c.split(' ')
        result.append([splitted[0], 0 if splitted[1] in true_signs else 1])
    return result


def check(test_cases):
    for t in test_cases:
        if t[1] not in true_signs + false_signs:
            raise IncorrectTestCaseError
