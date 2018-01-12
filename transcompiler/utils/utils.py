import codecs
import logging
import os


def get_absolute_file_directory(file):
    return os.path.dirname(os.path.abspath(file))


def set_logging_level(level_as_string):
    upper_case_level = level_as_string.strip().upper()
    if upper_case_level == "DEBUG":
        level = logging.DEBUG
    elif upper_case_level == "WARM":
        level = logging.WARN
    elif upper_case_level == "ERROR":
        level = logging.ERROR
    else:
        level = logging.INFO
    logging.basicConfig(level=level)


def read_filename_from(path):
    return os.path.basename(path)


def read_utf8_content_from(input_file):
    descriptor = codecs.open(input_file, "r", "utf-8")
    content = descriptor.read()
    descriptor.close()
    return content


def create_output_filename_from(cmd_name, name_based_on_input_name):
    filename = name_based_on_input_name if cmd_name is None else cmd_name
    return ensure_python_extension_in(filename)


def ensure_python_extension_in(filename):
    return filename if filename.endswith(".py") else filename + ".py"
