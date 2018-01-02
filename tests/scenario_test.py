import os
import shutil
import unittest
from os.path import isfile, join

from transcompiler.core import machine_parser, file_creator
from transcompiler.utils import utils


class TestDslParsingProcess(unittest.TestCase):
    example_machine_path = "example/example.dsl"
    created_machines_directory = "machines/"

    @staticmethod
    def parse_single_machine_dsl(path):
        content_to_parse = utils.read_content_from(path)
        return machine_parser.parse(content_to_parse)

    @staticmethod
    def list_all_machines(directory):
        paths = map(
            lambda file: join(directory, file),
            os.listdir(directory)
        )
        non_test_files = filter(
            lambda path: isfile(path) and not path.endswith(".test"),
            paths
        )
        return non_test_files

    def test_parse_example_machine_without_exception(self):
        self.parse_single_machine_dsl("../" + self.example_machine_path)

    def test_parse_all_created_machines_without_exception(self):
        for path in self.list_all_machines("../" + self.created_machines_directory):
            with self.subTest(machine=path):
                self.parse_single_machine_dsl(path)

    def test_create_example_machine_python3_file(self):
        parsed = self.parse_single_machine_dsl("../" + self.example_machine_path)
        tmp_dir = "tmp/example_tm"
        shutil.rmtree(tmp_dir, ignore_errors=True)
        os.makedirs(tmp_dir)
        file_creator.create_file(tmp_dir, "example_machine", parsed, "../")
        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    unittest.main()
