# -*- coding: utf-8 -*-
# Auto generated file
# 2018-01-03 23:57:04.530496
# warning: 
#          below import depends on project location and transcompiled code destination
#          in case of project or machine movement this file may not work
import sys
sys.path.append('yourLocalProjectAbsPathShouldBeHere/TuringMachineTranscompilerSimulator')
sys.path.append('..')
# Accepts language L={0^n1^n, n-natural (possible 0)}
# q_0 - looking for '0', when found, writes blank ang looking for '1'), accepts empty tape, when found '#', checking by q_c
# q_1 - looking for '1' (skipping rest), when not found, reject
# q_c - checking, whether there is possibility to go along all tape finding only '#', if yes, then accept
# q_b - going back
# 
import os
import argparse
import codecs
from subprocess import Popen, PIPE

# noinspection PyUnresolvedReferences
from transcompiler.core.static_parts.exceptions import *
# noinspection PyUnresolvedReferences
from transcompiler.core.static_parts.functions import *
from transcompiler.core.static_parts.tests_parser import parse_test_cases

from transcompiler.utils import utils

max_steps = 10000

command_line_parser = argparse.ArgumentParser()
command_line_parser.add_argument("-t", "--trace", dest="trace", action="store_true", default=None, required=False,
                                 help="enables trace mode")
command_line_parser.add_argument("-x", dest="x", default=None, required=False, help="input word")
command_line_parser.add_argument("-q", "--quiet", dest="quiet_mode", action="store_true", default=None, required=False,
                                 help="enables quiet mode")
command_line_parser.add_argument("--test", dest="test_cases_file", default=None, required=False,
                                 help="test mode, requires file with test cases")
command_line_parser.add_argument("-s", "--steps", dest="max_steps", default=None, required=False,
                                 help="Max steps (" + str(max_steps) + ") by default")
args = command_line_parser.parse_args()

accept_string = "yes"
reject_string = "no"

if args.max_steps and int(args.max_steps) > 0:
    max_steps = int(args.max_steps)
trace = args.trace
quiet = args.quiet_mode
test_cases_file = args.test_cases_file


def process_testing():
    test_cases_string = utils.read_utf8_content_from(test_cases_file)

    test_cases = parse_test_cases(test_cases_string)
    length = max(len(t[0]) for t in test_cases) + max(len(accept_string), len(reject_string)) + 5

    ok, failed, max_steps_exceeded = 0, 0, 0
    total = len(test_cases)

    for single_test_case in test_cases:
        cmd = "python3 " + os.path.realpath(__file__) + " -q -x " + single_test_case[0] + " -s " + str(max_steps)
        process = Popen(cmd.split(), stdout=PIPE)
        process.communicate()
        return_value = process.wait()
        test_case_string = "[" + single_test_case[0] + ", " + (
            accept_string if single_test_case[1] == 0 else reject_string) + "] "
        print("\n" + ("{0: <" + str(length) + "}").format(test_case_string), end="")
        if single_test_case[1] == return_value:
            ok += 1
            print("OK")
        else:
            failed += 1
            print("FAILED", end="")
            if return_value == 2:
                max_steps_exceeded += 1
                print(" (max steps exceeded)")
            else:
                print()

    print()
    print("OK     : " + str(ok) + "/" + str(total))
    print("FAILED : " + str(failed) + "/" + str(total) + " (max steps reached: " + str(max_steps_exceeded) + "/" + str(
        failed) + ")")

    exit(0)


if test_cases_file:
    process_testing()
tape_alphabet = ['0', '1']
working_alphabet = ['0', '1', '#', '▯']


@information_wrapper(trace, quiet)
def q_0(tape, position):
    if tape[position] == working_alphabet[0]:
        tape[position] = '▯'
        return q_1, position + 1
    elif tape[position] == working_alphabet[1]:
        return reject()
    elif tape[position] == working_alphabet[2]:
        tape[position] = '#'
        return q_c, position + 1
    elif tape[position] == working_alphabet[3]:
        return accept()
    else:
        raise NoSuchSymbolError


@information_wrapper(trace, quiet)
def q_1(tape, position):
    if tape[position] == working_alphabet[0]:
        tape[position] = '0'
        return q_1, position + 1
    elif tape[position] == working_alphabet[1]:
        tape[position] = '#'
        return q_b, position - 1
    elif tape[position] == working_alphabet[2]:
        tape[position] = '#'
        return q_1, position + 1
    elif tape[position] == working_alphabet[3]:
        return reject()
    else:
        raise NoSuchSymbolError


@information_wrapper(trace, quiet)
def q_c(tape, position):
    if tape[position] == working_alphabet[0]:
        return reject()
    elif tape[position] == working_alphabet[1]:
        return reject()
    elif tape[position] == working_alphabet[2]:
        tape[position] = '#'
        return q_c, position + 1
    elif tape[position] == working_alphabet[3]:
        return accept()
    else:
        raise NoSuchSymbolError


@information_wrapper(trace, quiet)
def q_b(tape, position):
    if tape[position] == working_alphabet[0]:
        tape[position] = '0'
        return q_b, position - 1
    elif tape[position] == working_alphabet[1]:
        return reject()
    elif tape[position] == working_alphabet[2]:
        tape[position] = '#'
        return q_b, position - 1
    elif tape[position] == working_alphabet[3]:
        tape[position] = '▯'
        return q_0, position + 1
    else:
        raise NoSuchSymbolError


x = ''
if not args.x:
    print('No input word delivered. Type it now.')
    x = input()
else:
    x = args.x
    if x == '':
        x = '▯'

actual_state_and_pos = (q_0, 1)
tape = list('▯') + list(x) + list('▯')
for i in range(max_steps):
    if actual_state_and_pos == accept():
        if not quiet:
            print('Accepted in ' + str(i) + ' steps!')
        exit(accept())
    elif actual_state_and_pos == reject():
        if not quiet:
            print('Rejected in ' + str(i) + ' steps!')
        exit(reject())

    if actual_state_and_pos[1] < 0:
        tape.insert(0, '▯')
        actual_state_and_pos[1] += 1
    elif actual_state_and_pos[1] >= len(tape):
        tape.append('▯')

    new_state_and_pos = actual_state_and_pos[0](tape, actual_state_and_pos[1])

    if actual_state_and_pos[1] <= 1 and tape[0] != '▯':
        tape.insert(0, '▯')
        actual_state_and_pos[1] += 1
    elif actual_state_and_pos[1] >= len(tape) - 2 and tape[-1] != '▯':
        tape.append('▯')

    actual_state_and_pos = new_state_and_pos

if not quiet:
    print('Rejected due to max steps (' + str(max_steps) + ') exceeded.')
exit(reject_max_steps_exceeded())
