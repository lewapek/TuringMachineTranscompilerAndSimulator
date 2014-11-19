# -*- coding: utf-8 -*-
import re
import creator.exceptions as e

__author__ = 'lewap'

accept = ['accept', 'a', 'yes', 'y']
reject = ['reject', 'r', 'no', 'n']
move_left = ['l', '<']
move_right = ['r', '>']
move = move_left + move_right
blank = u'▯'


def parse(content):
    description_regex = re.compile(r'/\*(.*)\*/', re.DOTALL)
    description = description_regex.findall(content)
    if description:
        description = description[0]
    else:
        description = ''
    content = re.sub(description_regex, '', content)

    content = re.sub(re.compile(r'blank'), blank, content)

    lines = content.splitlines()
    [lines.remove(i) for i in lines if i == '']
    name = lines[0].replace(' ', '_')
    tape_alphabet = lines[1].split()
    working_alphabet = lines[2].split()
    initial_state = lines[3].replace(' ', '')

    states_and_transitions = []
    for line in lines[4:]:
        splitted_line = line.split(';')
        state = splitted_line[0].replace(' ', '')
        transitions = []
        for transition in splitted_line[1:]:
            transitions += [transition.split()]
        states_and_transitions += [[state, transitions]]

    check_blank_in_alphabet(tape_alphabet)
    check_blank_in_alphabet(working_alphabet)

    working_alphabet += [blank]
    check_states(initial_state, states_and_transitions, working_alphabet)

    return name, description, tape_alphabet, working_alphabet, initial_state, states_and_transitions


def check_blank_in_alphabet(a):
    if blank in a:
        raise e.IncorrectInputAlphabetError


def check_if_tape_alphabet_in_working_alphabet(tape_alphabet, working_alphabet):
    if tape_alphabet not in working_alphabet:
        raise e.TapeAlphabetNotSubsetOfWorkingAlphabet


def check_states(initial_state, states_and_transitions, working_alphabet):
    states = []
    for st in states_and_transitions:
        states += [st[0]]

    if initial_state not in states:
        raise e.InitialStateNotInStates

    for st in states_and_transitions:
        for t in st[1]:
            if len(t) == 1:
                if t[0] not in accept and t[0] not in reject:
                    raise e.IncorrectTransitionError(t)
            elif len(t) == 3:
                if t[0] not in working_alphabet or t[1] not in states or t[2] not in move:
                    raise e.IncorrectTransitionError(t)
            else:
                raise e.IncorrectTransitionError(t)
