# -*- coding: utf-8 -*-

__author__ = 'lewap'


def information_wrapper(trace, quiet):
    def wrapper(state_function):
        def decorated_state_function(tape, position):
            if not quiet:
                before = ''
                for i in range(position):
                    before += ' '
                print(before + u'↓')
                text = ''
                for i in range(len(tape)):
                    text += tape[i]
                print(text + ' ' + state_function.__name__)

                if trace is not None:
                    input()
            state_function(tape, position)

        return decorated_state_function
    return wrapper


def accept():
    exit(0)


def reject():
    exit(1)
