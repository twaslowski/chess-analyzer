import chess.pgn
import chess.engine
from typing import *
import math
import io
import config
import progress_bar
from Blunder import Blunder
from board_util import generate_turn_string
import plotter


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


def _calculate_absolute_score(relative_score):
    if relative_score.white().is_mate():
        return -100
    else:
        return int(str(relative_score.white())) / 100


def analyze_game(game: chess.pgn) -> Tuple[List[Blunder], Any]:
    conf = config.create_args_object('config.json')
    engine = chess.engine.SimpleEngine.popen_uci(conf.stockfish_binary_path)

    blunders = []

    moves = game.mainline_moves()
    board = game.board()
    total_moves = math.ceil(len(list(moves)) / 2)

    scores = []
    prev_score = 0
    move_counter = 1
    prev_analysis = {}

    for move in moves:
        # formal stuff
        move_algebraic = board.san(move)
        board.push(move)

        # do analysis for current board state
        analysis = engine.analyse(board, chess.engine.Limit(conf.analysis.depth))

        # do the score graph
        score_relative = analysis.get('score')
        score_absolute = _calculate_absolute_score(score_relative)
        scores.append(score_absolute)

        # blunders, mistakes, inaccuracies logic
        _evaluate_move(board, move, blunders, move_counter, prev_score, score_absolute, prev_analysis)
        prev_score = score_absolute

        turn_string = generate_turn_string(move_counter, move_algebraic, True)
        progress_bar.print_progress_bar(iteration=move_counter, total=total_moves, suffix=turn_string)

        move_counter += 0.5
        prev_analysis = analysis

    engine.close()
    plot = plotter.plot(scores)
    return blunders, plot


def _evaluate_move(board, move, blunders, move_counter, prev_score, score, prev_analysis):
    if move_counter > 1:
        if _is_blunder(prev_score, score):
            blunders.append(Blunder(board.copy(), (prev_score, score), move_counter, move, prev_analysis.get('pv')[:6]))


# strictly numerical approach to blunders
def _is_blunder(prev_score, score):
    if _have_same_sign(prev_score, score):
        prev_score = math.fabs(prev_score)
        score = math.fabs(score)
        if prev_score > 50 or score > 50:
            return math.fabs(prev_score - score) > 20
        elif prev_score > 20 or score > 20:
            return math.fabs(prev_score - score) > 10
        elif prev_score > 10 or score > 10:
            return math.fabs(prev_score - score) > 5
        elif prev_score > 5 or score > 5:
            return math.fabs(prev_score - score) > 3
        else:
            return math.fabs(prev_score - score) > 2
    else:
        return math.fabs(math.fabs(prev_score) + math.fabs(score)) > 2


# returns if two numbers are both negative or positive
def _have_same_sign(i: int, j: int):
    return i < 0 and j < 0 or i > 0 and j > 0


def example():
    blunders = analyze_game(_read_pgn_from_file('../example_pgn_2.txt'))
    blunders_list = list(map(Blunder.stringify, blunders))
    for blunder in blunders_list:
        print(blunder)
