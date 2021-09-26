import chess
import chess.pgn
import chess.engine
import math
from Blunder import Blunder
import config
import threading
import logging


class Analysis:
    def __init__(self, pgn):
        self.pgn = pgn
        self.progress: int = 0
        self.is_done = False
        self.conf = config.create_args_object('config.json')
        self.depth = int(self.conf.analysis.get('depth'))
        self.blunders = []

    def run(self):
        t1 = threading.Thread(target=self.analyze_game)
        t1.start()

    def analyze_game(self):
        engine = chess.engine.SimpleEngine.popen_uci(self.conf.stockfish_binary_path)

        moves = self.pgn.mainline_moves()
        board = self.pgn.board()
        total_moves = math.ceil(len(list(moves)) / 2)

        scores = []
        prev_score = 0
        move_counter = 1
        prev_analysis = {}

        for move in moves:
            # formal stuff
            board.push(move)

            # do analysis for current board state
            analysis = engine.analyse(board, chess.engine.Limit(depth=self.depth))

            # do the score graph
            score_relative = analysis.get('score')
            score_absolute = _calculate_absolute_score(score_relative)
            scores.append(score_absolute)

            # blunders, mistakes, inaccuracies logic
            self._evaluate_move(board, move, move_counter, prev_score, score_absolute, prev_analysis)
            prev_score = score_absolute

            self.progress = math.floor((move_counter / total_moves) * 100)

            move_counter += 0.5
            prev_analysis = analysis

        self.is_done = True
        engine.close()

    def _evaluate_move(self, board, move, move_counter, prev_score, score, prev_analysis):
        if move_counter > 1:
            if _is_blunder(prev_score, score):
                self.blunders.append(
                    Blunder(board.copy(), (prev_score, score), move_counter, move, prev_analysis.get('pv')[:6]))


def _calculate_absolute_score(relative_score):
    if relative_score.white().is_mate():
        return -100
    else:
        return int(str(relative_score.white())) / 100


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
