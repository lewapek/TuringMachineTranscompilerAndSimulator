# -*- coding: utf-8 -*-
import codecs
import datetime
import creator.machine_parser as p

__author__ = 'lewap'

indentation = '    '
headers_file = 'creator/static_parts/headers.py'

tape_left_extension = 2 * indentation + "tape.insert(0, '" + p.blank + "')\n" + \
                      2 * indentation + "actual_state_and_pos[1] += 1\n"
tape_right_extension = 2 * indentation + "tape.append('" + p.blank + "')\n"


def create_file(path, parsed_content):
    name = parsed_content[0]
    description = parsed_content[1]
    tape_alphabet = parsed_content[2]
    working_alphabet = parsed_content[3]
    initial_state = parsed_content[4]
    states_and_transitions = parsed_content[5]

    f = codecs.open(path + '/' + name + '.py', 'w', 'utf-8')
    content = u"# -*- coding: utf-8 -*-\n" \
              "# Auto generated file\n" \
              "# " + str(datetime.datetime.now()) + "\n"
    f.write(content)

    [f.write('# ' + d + '\n') for d in description.split('\n')]

    headers = codecs.open(headers_file, 'r', 'utf-8')
    f.write(headers.read())
    headers.close()

    content = u"tape_alphabet = " + str(tape_alphabet) + "\n" \
              "working_alphabet = " + str(working_alphabet) + "\n" \
              "\n"

    for st in states_and_transitions:
        content += "\n@information_wrapper(trace, quiet)\n" \
                   "def " + st[0] + "(tape, position):\n"

        transitions = st[1]
        i = 0
        for t in transitions:
            content += indentation + ("if" if i == 0 else "elif") + " tape[position] == working_alphabet[" + str(i) + "]:\n"
            if len(t) == 1:
                if t[0] in p.accept:
                    content += 2 * indentation + "return accept()\n"
                else:
                    content += 2 * indentation + "return reject()\n"
            else:
                content += 2 * indentation + "tape[position] = '" + t[0] + "'\n"
                content += 2 * indentation + "return " + t[1] + ", position " + ("+ 1" if t[2] in p.move_right else "- 1") + "\n"
            i += 1
        content += indentation + "else:\n"
        content += 2 * indentation + "raise NoSuchSymbolError\n"
        content += "\n"

    content += "\nx = u''\n" \
               "if not args.x:\n" + \
               indentation + "print('No input word delivered. Type it now.')\n" + \
               indentation + "x = input()\n" \
               "else:\n" + \
               indentation + "x = args.x\n" + \
               indentation + "if x == 'BLANK' or x == 'blank':\n" + \
               2 * indentation + "x = '" + p.blank + "'\n" \
               "\n"

    content += "actual_state_and_pos = (" + initial_state + ", 1)\n" \
               "tape = list('" + p.blank + "') + list(x) + list('" + p.blank + "')\n" \
               "for i in range(max_steps):\n" + \
               indentation + "if actual_state_and_pos == accept():\n" + \
               2 * indentation + "if not quiet:\n" + \
               3 * indentation + "print('Accepted in ' + str(i) + ' steps!')\n" + \
               2 * indentation + "exit(accept())\n" + \
               indentation + "elif actual_state_and_pos == reject():\n" + \
               2 * indentation + "if not quiet:\n" + \
               3 * indentation + "print('Rejected in ' + str(i) + ' steps!')\n" + \
               2 * indentation + "exit(reject())\n" + \
               "\n" + \
               indentation + "if actual_state_and_pos[1] < 0:\n" + tape_left_extension + \
               indentation + "elif actual_state_and_pos[1] >= len(tape):\n" + tape_right_extension + \
               "\n" + \
               indentation + "new_state_and_pos = actual_state_and_pos[0](tape, actual_state_and_pos[1])\n" + \
               "\n" + \
               indentation + "if actual_state_and_pos[1] <= 1 and tape[0] != '" + p.blank + "':\n" + tape_left_extension + \
               indentation + "elif actual_state_and_pos[1] >= len(tape) - 2 and tape[-1] != '" + p.blank + "':\n" + tape_right_extension + \
               "\n" + \
               indentation + "actual_state_and_pos = new_state_and_pos\n"

    content += "\n" \
               "if not quiet:\n" + \
               indentation + "print('Rejected due to max steps (' + str(max_steps) + ') overflow.')\n" \
               "exit(reject_max_steps_exceeded())\n"
    f.write(content)

    f.close()
