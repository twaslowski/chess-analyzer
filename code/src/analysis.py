import threading

from chess import *
import chess.engine
import chess.pgn

import config
from move_evaluation import MoveEvaluation


class Analysis:
    def __init__(self, pgn):
        self.conf = config.create_args_object('config.json')
        self.time = int(self.conf.time)  # time the engine gets to take to evaluate a single move
        self.progress: int = 0  # analysis progress, 0 to 100
        self.is_done: bool = False
        self.pgn: pgn = pgn
        self.move_evals: List[MoveEvaluation] = []  # evaluation of all moves
        self.missed_wins: List[MoveEvaluation] = []
        self.blunders: List[MoveEvaluation] = []

    def run(self):
        t1 = threading.Thread(target=self.analyze_game)
        t1.start()

    def analyze_game(self):
        engine = chess.engine.SimpleEngine.popen_uci(self.conf.stockfish_binary_path)

        moves = self.pgn.mainline_moves()
        board = self.pgn.board()
        total_moves = math.ceil(len(list(moves)) / 2)

        move_counter = 1
        prev_analysis = engine.analyse(board, chess.engine.Limit(time=self.time))

        for move in moves:
            # formal stuff
            board.push(move)

            # do analysis for current board state
            analysis = engine.analyse(board, chess.engine.Limit(time=self.time))

            self._evaluate_move(board, move, move_counter, analysis, prev_analysis)

            self.progress = math.floor((move_counter / total_moves) * 100)

            move_counter += 0.5
            prev_analysis = analysis

        self.is_done = True
        engine.close()

    def _evaluate_move(self, board, move, move_counter, current_analysis, prev_analysis):
        self.move_evals.append(
            MoveEvaluation(board=board.copy(),
                           turn=move_counter,
                           move=move,
                           analyses=(prev_analysis, current_analysis)))

    def categorize_evals(self):
        for move_eval in self.move_evals:
            if move_eval.is_missed_win(False):
                self.missed_wins.append(move_eval)
            elif move_eval.is_blunder():
                self.blunders.append(move_eval)
