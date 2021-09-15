import chess.pgn
import chess.engine
import math

from chess import WHITE

from src import plotter
from src import config

pgn_filename = '../example_pgn.txt'

blunders = []
mistakes = []
inaccuracies = []

move_eval = {
    "blunders_threshold": 3,
    "mistake_threshold": 1,
    "inaccuracy_threshold": 0.5
}


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


def analyze_game(max_time):
    scores = []
    prev_score = 0
    move_counter = 1
    turn_string = ''

    for move in moves:
        # do analysis for current board state
        analysis = engine.analyse(board, chess.engine.Limit(time=max_time))

        # do the score graph
        score = calculate_absolute_score(analysis.get('score'))
        scores.append(score)

        # blunders, mistakes, inaccuracies logic
        if move_counter > 1:
            if math.fabs(score) - math.fabs(prev_score) > move_eval["blunders_threshold"]:
                blunders.append(generate_move_string(move_algebraic, move_counter))
            elif math.fabs(score) - math.fabs(prev_score) > move_eval["mistake_threshold"]:
                mistakes.append(generate_move_string(move_algebraic, move_counter))
            elif math.fabs(score) - math.fabs(prev_score) > move_eval["inaccuracy_threshold"]:
                inaccuracies.append(generate_move_string(move_algebraic, move_counter))
            prev_score = score

        # formal stuff
        move_algebraic = board.san(move)
        board.push(move)

        if move_counter % 1 != 0:
            turn_string += f'{move_algebraic} ({score})'
            print(turn_string)
            turn_string = ''
        else:
            turn_string = f'{int(move_counter)}. {move_algebraic} ({score}) '

        move_counter += 0.5


if __name__ == '__main__':
    conf = config.create_args_object('../config.json')
    engine = chess.engine.SimpleEngine.popen_uci(conf.stockfish_binary_path)
    analysis_time = conf.analysis.get('time')

    with open(pgn_filename) as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    moves = game.mainline_moves()
    board = game.board()

    analyze_game(analysis_time)
    print(f"blunders: {blunders}")
    print(f"mistakes: {mistakes}")
    print(f"inaccuracies: {inaccuracies}")

    engine.close()
