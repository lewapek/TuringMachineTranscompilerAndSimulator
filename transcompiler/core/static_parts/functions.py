# -*- coding: utf-8 -*-


def information_wrapper(trace, quiet):
    def wrapper(state_function):
        def decorated_state_function(tape, position):
            if not quiet:
                before = ""
                for i in range(position):
                    before += " "
                print(before + "↓")
                text = ""
                for i in range(len(tape)):
                    text += tape[i]
                print(text + " " + state_function.__name__)

                if trace is not None:
                    input()
            return state_function(tape, position)
        return decorated_state_function
    return wrapper


def accept():
    return 0


def reject():
    return 1


def reject_max_steps_exceeded():
    return 2
