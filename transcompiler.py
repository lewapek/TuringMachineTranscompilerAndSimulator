# -*- coding: utf-8 -*-
import argparse

from transcompiler.core import file_creator, machine_parser
from transcompiler.utils import utils


def parse_command_line():
    command_line_parser = argparse.ArgumentParser(description="Turing machine simulator creator")
    command_line_parser.add_argument("-f", "--file", dest="input_file", required=True,
                                     help="file containing machine specification")
    command_line_parser.add_argument("-d", "--dir", dest="output_directory", default="created_machines",
                                     required=False, help="path to store output file inside")
    command_line_parser.add_argument("-n", "--name", dest="output_name", default=None, required=False,
                                     help="output filename, .py extension will be added automatically if needed")
    command_line_parser.add_argument("-l", "--log", dest="logging_level", default="INFO", required=False,
                                     help="logging level")
    return command_line_parser.parse_args()


args = parse_command_line()
utils.set_logging_level(args.logging_level)
content_to_parse = utils.read_content_from(args.input_file)

parsed_content = machine_parser.parse(content_to_parse)
file_creator.create_file(
    args.output_directory,
    args.output_name,
    parsed_content,
    utils.get_absolute_file_directory(__file__)
)
