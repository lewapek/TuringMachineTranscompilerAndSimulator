from transcompiler.core.static_parts.functions import accept, reject
from transcompiler.utils.exceptions import IncorrectTestCaseError

from transcompiler import config


def expected_result_from(string):
    if string in config.true_signs:
        return accept()
    elif string in config.false_signs:
        return reject()
    else:
        raise IncorrectTestCaseError


def parse_test_cases(content):
    result = []
    content = content.split("\n")
    for line in content:
        split_line = line.split()
        if len(split_line) == 1:
            result.append([config.blank, expected_result_from(split_line[0])])
        elif len(split_line) == 2:
            result.append([split_line[0], expected_result_from(split_line[1])])
        else:
            raise IncorrectTestCaseError
    return result
