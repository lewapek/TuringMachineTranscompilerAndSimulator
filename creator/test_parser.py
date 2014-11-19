from creator.exceptions import IncorrectTestCaseError

__author__ = 'lewap'


true_signs = ('Y', 'y', 'A', 'a', '+')
false_signs = ('N', 'n', 'R', 'r', '-')


def parse(content):
    result = []
    content = content.split('\n')
    for c in content:
        splitted = c.split(' ')

        if splitted[1] in true_signs:
            ret_val = 0
        elif splitted[1] in false_signs:
            ret_val = 1
        else:
            raise IncorrectTestCaseError

        result.append([splitted[0], ret_val])
    return result

