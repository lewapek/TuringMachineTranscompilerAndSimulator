# -*- coding: utf-8 -*-
import logging
import re

import transcompiler.utils.exceptions as e
from transcompiler import config


def parse(content):
    logging.debug("Parsing content:\n" + content)
    description_regex = re.compile(r"/\*(.*)\*/", re.DOTALL)
    description = description_regex.findall(content)
    if description:
        description = description[0]
    else:
        description = ""
    content = re.sub(description_regex, "", content)

    content = re.sub(re.compile(r"blank"), config.blank, content)
    content = re.sub(re.compile(r"BLANK"), config.blank, content)

    logging.debug("Preprocessed content:\n" + content)

    lines = content.splitlines()
    [lines.remove(i) for i in lines if i == ""]
    name = lines[0].replace(" ", "_")
    tape_alphabet = lines[1].split()
    initial_state = lines[2].replace(" ", "")
    working_alphabet = list(map(lambda character: character.strip(), lines[3].split(";")))[1:-1]

    logging.debug("Name: " + str(name))
    logging.debug("Tape alphabet: " + str(tape_alphabet))
    logging.debug("Initial state: " + str(initial_state))
    logging.debug("Working alphabet: " + str(working_alphabet))

    states_and_transitions = []
    for line in lines[4:]:
        split_line = line.split(";")
        state = split_line[0].replace(" ", "")
        transitions = []
        for transition in split_line[1:]:
            transitions += [transition.split()]
        states_and_transitions += [[state, transitions]]

    check_blank_in_alphabet(tape_alphabet)
    check_blank_in_alphabet(working_alphabet)

    working_alphabet += [config.blank]
    check_states(initial_state, states_and_transitions, working_alphabet)

    return name, description, tape_alphabet, working_alphabet, initial_state, states_and_transitions


def check_blank_in_alphabet(alphabet):
    if config.blank in alphabet:
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
                if t[0] not in config.accept and t[0] not in config.reject:
                    raise e.IncorrectTransitionError(t)
            elif len(t) == 3:
                if t[0] not in working_alphabet or t[1] not in states or t[2] not in config.move:
                    raise e.IncorrectTransitionError(t)
            else:
                raise e.IncorrectTransitionError(t)
