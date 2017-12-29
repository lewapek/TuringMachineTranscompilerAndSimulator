# Turing machine transcompiler and simulator
*Machine description to python3 program transcompiler.*

This project enables you to provide Turing machine using DSL (example below) and converts it to python3 program. Having the generated program you can freely run it to check if it accepts input words. You can also write some tests and quickly check how many of them passed or failed (due to rejection or exceeding configurable max-steps parameter).

The project was created in 2014 as a tool supporting learning for colloquium at AGH University of Science and Technology (subject: 'Computation and Complexity Theory').

Machines contain single tape, infinite at both sides.  
Working alphabet is alphabet for input words.  
Tape alphabet is alphabet consisting of characters which can be written on tape (working alphabet + optional additional characters).


## Usage
1. Create deterministic Turing machine in the following form:


    machineName
    /*
    multiline comment
    */
    Tape alphabet split by space
    Initial state
    Machine description in the form of table, where 1st column consist of state names and 1st row consist of working alphabet.
    Columns are split by ;
    Each row consists of 3-element tuple with character, state name and transition which tells the machine to write the character on the tape, switch to the state and move 1 character left or rigth.

All elements should be placed on single line except from multiline comment and machine description.

## Example
In this next section you will see practical example how to write sample Turing machine, transcompile it to python3 program, run, trace and test.


Empty input word is represented by 'BLANK' string.



TESTING PROCESS

There is possibility to write tests for your machine. Test cases should be placed in text file.

Test file should contain n lines (each representing single test case).

Each test case is input_word and bool_value

bool_value is one of ('Y', 'y', 'A', 'a', '+') in case machine should accept given word or one of ('N', 'n', 'R', 'r', '-') in case machine should reject given word.

To run test:

    python3 machine_filename --test test_file

For example:

    python3 example_machine_0pow_n_1pow_n.py --test ../example.test
