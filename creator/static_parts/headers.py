import sys
import os

sys.path.append('.')
sys.path.append('..')

from creator.static_parts.functions import *
from creator.static_parts.exceptions import *
import argparse
import codecs
import creator.test_parser as p
from subprocess import Popen, PIPE

max_steps = 10000

command_line_parser = argparse.ArgumentParser()
command_line_parser.add_argument('-t', '--trace', dest='trace', action='store_true', default=None, required=False,
                                 help="Enables trace mode")
command_line_parser.add_argument('-x', dest='x', default=None, required=False, help='Input word')
command_line_parser.add_argument('-q', '--quiet', dest='quiet_mode', action='store_true', default=None, required=False)
command_line_parser.add_argument('--test', dest='test', default=None, required=False,
                                 help='Test mode. Requires file with test cases.')
command_line_parser.add_argument('-s', '--steps', dest='max_steps', default=None, required=False,
                                 help='Max steps (' + str(max_steps) + ') by default')
args = command_line_parser.parse_args()

accept_string = 'yes'
reject_string = 'no'

if args.max_steps and int(args.max_steps) > 0:
    max_steps = int(args.max_steps)
trace = args.trace
quiet = args.quiet_mode
test = args.test

if test:
    f = codecs.open(test, 'r', 'utf-8')
    test_cases = f.read()
    f.close()

    test_cases = p.parse(test_cases)
    length = max(len(t[0]) for t in test_cases) + max(len(accept_string), len(reject_string)) + 5

    ok, failed, max_steps_exceeded = 0, 0, 0
    total = len(test_cases)

    for t in test_cases:
        if t[0] == '':
            t[0] = 'BLANK'
        cmd = 'python3 ' + os.path.realpath(__file__) + ' -q -x ' + t[0] + ' -s ' + str(max_steps)
        process = Popen(cmd.split(' '), stdout=PIPE)
        process.communicate()
        return_value = process.wait()
        test_case_string = '[' + t[0] + ', ' + (accept_string if t[1] == 0 else reject_string) + '] '
        print('\n' + ('{0: <' + str(length) + '}').format(test_case_string), end='')
        if t[1] == return_value:
            ok += 1
            print('OK')
        else:
            failed += 1
            print('FAILED', end='')
            if return_value == 2:
                max_steps_exceeded += 1
                print(' (max steps exceeded)')

    print()
    print('OK     : ' + str(ok) + '/' + str(total))
    print('FAILED : ' + str(failed) + '/' + str(total) + ' (max steps reached: ' + str(max_steps_exceeded) + '/' + str(failed) + ')')

    exit(0)
