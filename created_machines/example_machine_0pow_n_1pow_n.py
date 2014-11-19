# -*- coding: utf-8 -*-
# Auto generated file
# 2014-11-19 18:05:16.998403
# Accepts language L={0^n1^n, n-natural (possible 0)}
# q_0 - looking for '0', when found, writes blank ang looking for '1'), accepts empty tape, when found '#', checking by q_c
# q_1 - looking for '1' (skipping rest), when not found, reject
# q_c - checking, whether there is possibility to go along all tape finding only '#', if yes, then accept
# q_b - going back
# 
import sys
import os

sys.path.append('..')

from creator.static_parts.functions import *
from creator.static_parts.exceptions import *
import argparse
import codecs
import creator.test_parser as p
from subprocess import Popen, PIPE

command_line_parser = argparse.ArgumentParser()
command_line_parser.add_argument('-t', '--trace', dest='trace', action='store_true', default=None, required=False,
                                 help="Enables trace mode")
command_line_parser.add_argument('-x', dest='x', default=None, required=False, help='Input word')
command_line_parser.add_argument('-q', '--quiet', dest='quiet_mode', action='store_true', default=None, required=False)
command_line_parser.add_argument('--test', dest='test', default=None, required=False,
                                 help='Test mode. Requires file with test cases.')
args = command_line_parser.parse_args()

trace = args.trace
quiet = args.quiet_mode
test = args.test
if test:
    f = codecs.open(test, 'r', 'utf-8')
    test_cases = f.read()
    f.close()

    test_cases = p.parse(test_cases)
    p.check(test_cases)
    for t in test_cases:
        if t[0] == '':
            t[0] = 'BLANK'
        length = t.max(axis=0) + 1
        cmd = 'python3 ' + os.path.realpath(__file__) + ' -q -x ' + t[0]
        process = Popen(cmd.split(' '), stdout=PIPE)
        process.communicate()
        return_value = process.wait()
        print('\n' + t[0] + ' ', end='')
        if t[1] == return_value:
            print('ok')
        else:
            print('FAILED')

    exit(0)

tape_alphabet = ['0', '1']
working_alphabet = ['0', '1', '#', '▯']


@information_wrapper(trace, quiet)
def q_0(tape, position):
    if position < 0:
        tape.insert(0, '▯')
        position = 0
    elif position >= len(tape):
        tape.append('▯')

    if tape[position] == working_alphabet[0]:
        tape[position] = '▯'
        q_1(tape, position + 1)
    elif tape[position] == working_alphabet[1]:
        if not quiet:
            print('Rejected!')
        reject()
    elif tape[position] == working_alphabet[2]:
        tape[position] = '#'
        q_c(tape, position + 1)
    elif tape[position] == working_alphabet[3]:
        if not quiet:
            print('Accepted!')
        accept()
    else:
        raise NoSuchSymbolError


@information_wrapper(trace, quiet)
def q_1(tape, position):
    if position < 0:
        tape.insert(0, '▯')
        position = 0
    elif position >= len(tape):
        tape.append('▯')

    if tape[position] == working_alphabet[0]:
        tape[position] = '0'
        q_1(tape, position + 1)
    elif tape[position] == working_alphabet[1]:
        tape[position] = '#'
        q_b(tape, position -1)
    elif tape[position] == working_alphabet[2]:
        tape[position] = '#'
        q_1(tape, position + 1)
    elif tape[position] == working_alphabet[3]:
        if not quiet:
            print('Rejected!')
        reject()
    else:
        raise NoSuchSymbolError


@information_wrapper(trace, quiet)
def q_c(tape, position):
    if position < 0:
        tape.insert(0, '▯')
        position = 0
    elif position >= len(tape):
        tape.append('▯')

    if tape[position] == working_alphabet[0]:
        if not quiet:
            print('Rejected!')
        reject()
    elif tape[position] == working_alphabet[1]:
        if not quiet:
            print('Rejected!')
        reject()
    elif tape[position] == working_alphabet[2]:
        tape[position] = '#'
        q_c(tape, position + 1)
    elif tape[position] == working_alphabet[3]:
        if not quiet:
            print('Accepted!')
        accept()
    else:
        raise NoSuchSymbolError


@information_wrapper(trace, quiet)
def q_b(tape, position):
    if position < 0:
        tape.insert(0, '▯')
        position = 0
    elif position >= len(tape):
        tape.append('▯')

    if tape[position] == working_alphabet[0]:
        tape[position] = '0'
        q_b(tape, position -1)
    elif tape[position] == working_alphabet[1]:
        if not quiet:
            print('Rejected!')
        reject()
    elif tape[position] == working_alphabet[2]:
        tape[position] = '#'
        q_b(tape, position -1)
    elif tape[position] == working_alphabet[3]:
        tape[position] = '▯'
        q_0(tape, position + 1)
    else:
        raise NoSuchSymbolError


x = u''
if not args.x:
    print('No input word delivered. Type it now.')
    x = input()
else:
    x = args.x
    if x == 'BLANK':
        x = '▯'

q_0(list('▯') + list(x) + list('▯'), 1)