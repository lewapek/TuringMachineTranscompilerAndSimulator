# -*- coding: utf-8 -*-
import argparse
import codecs
from creator import machine_parser, file_creator

__author__ = 'lewap'

default_input_file = 'example.description'

command_line_parser = argparse.ArgumentParser(description='Turing machine simulator creator')
command_line_parser.add_argument('-f', '--file', dest='input_file', default=None, required=False,
                                 help='File containing machine description.')
command_line_parser.add_argument('-o', '--output', dest='output_path', default='created_machines', required=False,
                                 help='Path to store output file inside.')
args = command_line_parser.parse_args()

content_to_parse = u''

if args.input_file:
    f = codecs.open(args.input_file, 'r', 'utf-8')
    content_to_parse = f.read()
    f.close()
else:
    print('You did\'t specified file to read machine description from. Type it now. Type END to finish.')
    line = input()
    while line != 'END':
        content_to_parse += line + '\n'
        line = input()

parsed_content = machine_parser.parse(content_to_parse)
file_creator.create_file(args.output_path, parsed_content)
