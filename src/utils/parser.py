import os
from argparse import ArgumentParser, Namespace
from ast import literal_eval
from configparser import ConfigParser, Error as ConfigParserError
from typing import Any


class ParserError(ConfigParserError):
    pass


class Parser:
    def __init__(self):
        self.parser = ConfigParser()

    @staticmethod
    def _validate_path(file_path: str) -> str:
        if os.path.exists(file_path):
            return file_path
        else:
            raise ValueError(f"Path does not exist! {file_path}: False")

    @staticmethod
    def get_args() -> Namespace:
        parser = ArgumentParser()
        parser.add_argument(
            "--config-file-name", type=str, help="configuration file ini"
        )
        return parser.parse_args()

    def read(self, file_path: str) -> Any:
        try:
            path = self._validate_path(file_path=file_path)
            self.parser.read(path)
            return {
                i: {i[0]: literal_eval(i[1]) for i in self.parser.items(i)}
                for i in self.parser.sections()
            }

        except (ParserError, ValueError) as parser_error:
            raise parser_error
