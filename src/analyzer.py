import chess.pgn
import chess.engine
import math

from chess import Move, Board

from src import config
from src import progress_bar

pgn_filename = '../example_pgn_2.txt'

blunders = []
missed_wins = []


def calculate_absolute_score(relative_score):
    if relative_score.white().is_mate():
        return -100
    else:
        return int(str(relative_score.white())) / 100


def generate_move_string(move_algebraic, move_counter):
    if move_counter % 1 == 0:
        return f"{int(move_counter)}. {move_algebraic}"
    else:
        return f"{int(move_counter - 0.5)}. .. {move_algebraic}"


def analyze_game():
    scores = []
    prev_score = 0
    move_counter = 1
    turn_string = ''
    prev_analysis = {}

    for move in moves:
        # formal stuff
        move_algebraic = board.san(move)
        board.push(move)

        # do analysis for current board state
        analysis = engine.analyse(board, chess.engine.Limit(time=0.1))

        # do the score graph
        score_relative = analysis.get('score')
        score_absolute = calculate_absolute_score(score_relative)
        scores.append(score_absolute)

        # blunders, mistakes, inaccuracies logic
        evaluate_move(move_algebraic, move_counter, prev_score, score_absolute, prev_analysis)
        prev_score = score_absolute

        turn_string = generate_turn_string(move_counter, move_algebraic, True)
        progress_bar.print_progress_bar(iteration=move_counter, total=total_moves, suffix=turn_string)

        move_counter += 0.5
        prev_analysis = analysis


def generate_turn_string(move_counter: float, move_algebraic: str, use_context: bool) -> str:
    if move_counter % 1 != 0:
        prefix = f"{math.floor(move_counter)}. .." if use_context else ' '
        return f"{prefix}{move_algebraic} "
    else:
        return f'{int(move_counter)}. {move_algebraic}'


def generate_alternative_line_algebraic(alternative_moves, move_counter):
    # store the move that was actually played
    prev_move = board.pop()

    # create string for alternative line
    alternative_line_algebraic_string = ''
    for move in alternative_moves:
        move_algebraic = board.san(move)
        turn_string = generate_turn_string(move_counter, move_algebraic, False)
        alternative_line_algebraic_string += f"{turn_string}"
        board.push(move)
        move_counter += 0.5

    # clean up
    for i in range(len(alternative_moves)):
        board.pop()
    board.push(prev_move)

    return alternative_line_algebraic_string


def evaluate_move(move_algebraic, move_counter, prev_score, score, prev_analysis):
    if move_counter % 1 != 0:
        move_algebraic = ".." + move_algebraic
        move_counter -= 0.5
    if move_counter > 1:
        if is_missed_win(prev_score, score):
            missed_wins.append(f"{int(move_counter)}. {move_algebraic}")
        elif is_blunder(prev_score, score):
            blunders.append({
                "turn": int(move_counter),
                "move": move_algebraic,
                "prev_score": prev_score,
                "new_score": score,
                "best continuation": generate_alternative_line_algebraic(prev_analysis.get('pv')[:6], move_counter)
            })


def is_missed_win(prev_score, score):
    return math.fabs(prev_score) == 100 and math.fabs(score) != 100


# strictly numerical approach to blunders
def is_blunder(prev_score, score):
    if have_same_sign(prev_score, score):
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
        return math.fabs(math.fabs(prev_score) - math.fabs(score)) > 1.5


# returns if two numbers are both negative or positive
def have_same_sign(i: int, j: int):
    return i < 0 and j < 0 or i > 0 and j > 0


def print_blunders():
    for blunder in blunders:
        print(blunder)


if __name__ == '__main__':
    conf = config.create_args_object('../config.json')
    engine = chess.engine.SimpleEngine.popen_uci(conf.stockfish_binary_path)

    analysis_time = conf.analysis.get('time')
    depth = conf.analysis.get('depth')

    with open(pgn_filename) as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    moves = game.mainline_moves()
    board = game.board()
    total_moves = math.ceil(len(list(moves)) / 2)

    analyze_game()
    print()
    print_blunders()

    engine.close()
