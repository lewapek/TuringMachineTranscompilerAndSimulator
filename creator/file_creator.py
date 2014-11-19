# -*- coding: utf-8 -*-
import codecs
import datetime
import creator.machine_parser as p

__author__ = 'lewap'

indentation = '    '
headers_file = 'creator/static_parts/headers.py'


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
        content += indentation + "if position < 0:\n" + \
                   2 * indentation + "tape.insert(0, '" + p.blank + "')\n" + \
                   2 * indentation + "position = 0\n" + \
                   indentation + "elif position >= len(tape):\n" + \
                   2 * indentation + "tape.append('" + p.blank + "')\n" \
                   "\n"

        transitions = st[1]
        i = 0
        for t in transitions:
            content += indentation + ("if" if i == 0 else "elif") + " tape[position] == working_alphabet[" + str(i) + "]:\n"
            if len(t) == 1:
                if t[0] in p.accept:
                    content += 2 * indentation + "if not quiet:\n" + \
                               3 * indentation + "print('Accepted!')\n" + \
                               2 * indentation + "accept()\n"
                else:
                    content += 2 * indentation + "if not quiet:\n" + \
                               3 * indentation + "print('Rejected!')\n" + \
                               2 * indentation + "reject()\n"
            else:
                content += 2 * indentation + "tape[position] = '" + t[0] + "'\n"
                content += 2 * indentation + t[1] + "(tape, position " + ("+ 1" if t[2] in p.move_right else "-1") + ")\n"
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
               indentation + "if x == 'BLANK':\n" + \
               2 * indentation + "x = '" + p.blank + "'\n" \
               "\n"

    content += initial_state + "(list('" + p.blank + "') + list(x) + list('" + p.blank + "'), 1)"
    f.write(content)

    f.close()
