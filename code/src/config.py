from typing import NamedTuple

from json_configparser import ConfigArgs


class Arguments(NamedTuple):
    stockfish_binary_path: str
    time: float
    log_level: str
    recognize_slower_mate: bool


def create_args_object(config_path):
    args_object = ConfigArgs(Arguments)
    dict_args = args_object.parse_json(config_path)
    return Arguments(**dict_args)
