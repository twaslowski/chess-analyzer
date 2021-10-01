import io

import chess.engine
import chess.pgn


def read_pgn_from_string(text: str):
    pgn = chess.pgn.read_game(io.StringIO(text))
    if _is_valid_pgn(pgn):
        return pgn
    else:
        return None


def _is_valid_pgn(pgn):
    header_error_count = 0
    for key in pgn.headers.keys():
        if pgn.headers.get(key) == '?' or pgn.headers.get(key) == '*':
            header_error_count += 1
    return header_error_count < 3


def _read_pgn_from_file(filepath: str):
    with open(filepath) as file:
        return chess.pgn.read_game(file)
