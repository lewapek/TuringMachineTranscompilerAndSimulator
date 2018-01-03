# -*- coding: utf-8 -*-

#
accept = ["accept", "a", "yes", "y"]
reject = ["reject", "r", "no", "n"]

move_left = ["l", "<"]
move_right = ["r", ">"]
move = move_left + move_right

blank = "▯"
blank_equivalents = ["BLANK", "blank"]


# test cases config - case insensitive values
# true signs - word should be accepted by machine, false signs - rejected
# see example/example.test for sample usage
true_signs = ("y", "yes", "a", "accept", "+")
false_signs = ("n", "no", "r", "reject", "-")
