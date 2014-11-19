TuringMachineSimulatorCreator by lewap



Given a Turing machine description creates python3 file which simulates machine.

Only machines containing single tape (infinite at both sides) are allowed.



MACHINE CREATION PROCESS

To create Turing machine simulator run:

    python3 main.py [-h] [-f INPUT_FILE] [-o OUTPUT_PATH]

        -h, --help            show this help message and exit

        -f INPUT_FILE, --file INPUT_FILE

                              File containing machine description.

        -o OUTPUT_PATH, --output OUTPUT_PATH

                              Path to store output file inside.





Machine description can be placed in text file or you can specify it after running main.py.

Description should have following format:

Machine name

/\* comment - optional \*/

input alphabet separated by ' '

working alphabet separated by ' ' (except blank)

initial state name

state_name; transition1; transition2; transition3; ...

another_state_name; transition4; transition5; transition6;



where transitions appear in order of your working alphabet (last transition for blank)

transition format is one of:

new_sing_from_working_alphabet new_state move

    move = move_left | move_right

    move_left = 'l' | '<'

    move_right = 'r' | '>'

accept | a | y | yes | reject, r, no, n



Example description is placed in file 'example.description'.



MACHINE RUNNING PROCESS

After successful main.py execution file similar to your machine name appeared in 'OUTPUT_PATH' (created_machines by default).

To run your machine type go to 'OUTPUT_PATH' and type:

    python3 machine_filename [-h] [-t] [-x X] [-q] [--test TEST]

        -h, --help   show this help message and exit

        -t, --trace  Enables trace mode

        -x X         Input word

        -q, --quiet

        --test TEST  Test mode. Requires file with test cases.



To run example machine:

    python3 example_machine_0pow_n_1pow_n.py



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





Good luck on TOiZO :)

lewap