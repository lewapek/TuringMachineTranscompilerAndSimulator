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

command_line_parser = argparse.ArgumentParser()
command_line_parser.add_argument('-t', '--trace', dest='trace', action='store_true', default=None, required=False,
                                 help="Enables trace mode")
command_line_parser.add_argument('-x', dest='x', default=None, required=False, help='Input word')
command_line_parser.add_argument('-q', '--quiet', dest='quiet_mode', action='store_true', default=None, required=False)
command_line_parser.add_argument('--test', dest='test', default=None, required=False,
                                 help='Test mode. Requires file with test cases.')
args = command_line_parser.parse_args()

accept_string = 'yes'
reject_string = 'no'
trace = args.trace
quiet = args.quiet_mode
test = args.test
if test:
    f = codecs.open(test, 'r', 'utf-8')
    test_cases = f.read()
    f.close()

    test_cases = p.parse(test_cases)
    length = max(len(t[0]) for t in test_cases) + max(len(accept_string), len(reject_string)) + 5

    ok, failed = 0, 0
    total = len(test_cases)

    for t in test_cases:
        if t[0] == '':
            t[0] = 'BLANK'
        cmd = 'python3 ' + os.path.realpath(__file__) + ' -q -x ' + t[0]
        process = Popen(cmd.split(' '), stdout=PIPE)
        process.communicate()
        return_value = process.wait()
        test_case_string = '[' + t[0] + ', ' + (accept_string if t[1] == 0 else reject_string) + '] '
        print('\n' + ('{0: <' + str(length) + '}').format(test_case_string), end='')
        if t[1] == return_value:
            ok += 1
            print('ok')
        else:
            failed += 1
            print('FAILED')

    print('\nOK: ' + str(ok) + '/' + str(total) + ', FAILED: ' + str(failed) + '/' + str(total))

    exit(0)

