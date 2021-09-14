import chess.pgn
import chess.engine
import math
from src import plotter
from src import config

pgn_filename = '../example_pgn.txt'

blunders = []
mistakes = []
inaccuracies = []


def calculate_absolute_score(relative_score):
    if relative_score.white().is_mate():
        return -100
    else:
        return int(str(relative_score.white())) / 100


def analyze_game():
    scores = []
    prev_score = 0
    move_counter = 0
    turn_string = ''

    for move in moves:
        # formal stuff
        move_algebraic = board.san(move)
        board.push(move)
        analysis = engine.analyse(board, chess.engine.Limit(time=0.1))

        # do the score graph
        score = calculate_absolute_score(analysis['score'])
        scores.append(score)

        # blunders, mistakes, inaccuracies logic
        if math.fabs(score) - math.fabs(prev_score) > 2:
            blunders.append(move_algebraic)
        prev_score = score

        move_counter += 0.5
        if move_counter % 1 == 0:
            turn_string += f'{move_algebraic}: ({score})'
            print(turn_string)
            turn_string = ''
        else:
            turn_string = f'{move_algebraic}: ({score}) – '


if __name__ == '__main__':
    conf = config.create_args_object('../config.json')
    engine = chess.engine.SimpleEngine.popen_uci(conf.stockfish_binary_path)

    with open(pgn_filename) as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    moves = game.mainline_moves()
    board = game.board()

    analyze_game()
    engine.close()
