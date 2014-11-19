__author__ = 'lewap'


true_signs = ('Y', 'y', 'A', 'a', '+')


def parse(content):
    result = []
    content = content.split('\n')
    for c in content:
        splitted = c.split(' ')
        result.append([splitted[0], 0 if splitted[1] in true_signs else 1])
    return result
