# -*- coding: utf-8 -*-
import codecs
import datetime
import os

from transcompiler import config
from transcompiler.utils import utils

indentation = "    "


def indent(times=1):
    return times * indentation


def choose_machine_name_from(cmd_name, parsed_name):
    filename = parsed_name if cmd_name is None else cmd_name
    return utils.ensure_python_extension_in(filename)


tape_left_extension = indent(2) + "tape.insert(0, '" + config.blank + "')\n" + \
                      indent(2) + "actual_state_and_pos[1] += 1\n"
tape_right_extension = indent(2) + "tape.append('" + config.blank + "')\n"


def create_file(directory, command_line_name, parsed_content, project_directory_path):
    beginning_file = os.path.join(
        os.path.relpath(project_directory_path, os.getcwd()),
        "transcompiler/core/static_parts/beginning.py"
    )
    parsed_name = parsed_content[0]
    description = parsed_content[1]
    tape_alphabet = parsed_content[2]
    working_alphabet = parsed_content[3]
    initial_state = parsed_content[4]
    states_and_transitions = parsed_content[5]

    filename = choose_machine_name_from(command_line_name, parsed_name)
    created_file_path = directory + "/" + filename

    f = codecs.open(created_file_path, "w", "utf-8")
    comments = "# -*- coding: utf-8 -*-\n" \
               "# Auto generated file\n" \
               "# " + str(datetime.datetime.now()) + "\n"
    f.write(comments)
    f.write("# warning: \n"
            "#          below import depends on project location and transcompiled code destination\n"
            "#          in case of project or machine movement this file may not work\n"
            "import sys\n"
            "sys.path.append('" + project_directory_path + "')\n")

    [f.write("# " + d + "\n") for d in description.split("\n")]

    beginning = codecs.open(beginning_file, "r", "utf-8")
    f.write(beginning.read())
    beginning.close()

    content = "tape_alphabet = " + str(tape_alphabet) + "\n" + \
              "working_alphabet = " + str(working_alphabet) + "\n" + \
              "\n"

    for (state, transition) in states_and_transitions:
        content += "\n@information_wrapper(trace, quiet)\n" \
                   "def " + state + "(tape, position):\n"

        transitions = transition
        i = 0
        for t in transitions:
            content += indent(1) + ("if" if i == 0 else "elif") + " tape[position] == working_alphabet[" + str(
                i) + "]:\n"
            if len(t) == 1:
                if t[0] in config.accept:
                    content += indent(2) + "return accept()\n"
                else:
                    content += indent(2) + "return reject()\n"
            else:
                content += indent(2) + "tape[position] = '" + t[0] + "'\n"
                content += indent(2) + "return " + t[1] + ", position " + (
                    "+ 1" if t[2] in config.move_right else "- 1") + "\n"
            i += 1
        content += indent(1) + "else:\n"
        content += indent(2) + "raise NoSuchSymbolError\n"
        content += "\n"

    content += "\nx = ''\n" \
               "if not args.x:\n" + \
               indent(1) + "print('No input word delivered. Type it now.')\n" + \
               indent(1) + "x = input()\n" \
                           "else:\n" + \
               indent(1) + "x = args.x\n" + \
               indent(1) + "if x == '':\n" + \
               indent(2) + "x = '" + config.blank + "'\n" \
                                                    "\n"

    content += "actual_state_and_pos = (" + initial_state + ", 1)\n" + \
               "tape = list('" + config.blank + "') + list(x) + list('" + config.blank + "')\n" + \
               "for i in range(max_steps):\n" + \
               indent(1) + "if actual_state_and_pos == accept():\n" + \
               indent(2) + "if not quiet:\n" + \
               indent(3) + "print('Accepted in ' + str(i) + ' steps!')\n" + \
               indent(2) + "exit(accept())\n" + \
               indent(1) + "elif actual_state_and_pos == reject():\n" + \
               indent(2) + "if not quiet:\n" + \
               indent(3) + "print('Rejected in ' + str(i) + ' steps!')\n" + \
               indent(2) + "exit(reject())\n" + \
               "\n" + \
               indent(1) + "if actual_state_and_pos[1] < 0:\n" + tape_left_extension + \
               indent(1) + "elif actual_state_and_pos[1] >= len(tape):\n" + tape_right_extension + \
               "\n" + \
               indent(1) + "new_state_and_pos = actual_state_and_pos[0](tape, actual_state_and_pos[1])\n" + \
               "\n" + \
               indent(
                   1) + "if actual_state_and_pos[1] <= 1 and tape[0] != '" + config.blank + "':\n" + tape_left_extension + \
               indent(
                   1) + "elif actual_state_and_pos[1] >= len(tape) - 2 and tape[-1] != '" + config.blank + "':\n" + \
               tape_right_extension + \
               "\n" + \
               indent(1) + "actual_state_and_pos = new_state_and_pos\n"

    content += "\n" \
               "if not quiet:\n" + \
               indent(1) + "print('Rejected due to max steps (' + str(max_steps) + ') exceeded.')\n" \
                           "exit(reject_max_steps_exceeded())\n"
    f.write(content)

    f.close()

    return created_file_path
