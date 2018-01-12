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
