import io
import time
import unittest

from chess import Board, pgn

from move_evaluation import MoveEvaluation
from analysis import Analysis


class AnalysisTest(unittest.TestCase):
    board = Board()

    analysis = Analysis(pgn.read_game(io.StringIO('1. f3 e6 2. g4 Nc6 3. Nc3 Qh4#')), '../../config.test.json')
    analysis.run()

    while not analysis.is_done:
        print(f"Progress: {analysis.progress}")
        time.sleep(1)

    analysis.categorize_evals()

    def test_blunders(self):
        self.assertEqual(len(self.analysis.blunders), 2)  # g4 and Nc3 both blunder #-1 respectively

    def test_missed_wins(self):
        print(self.analysis.missed_wins[0].stringify())
        self.assertEqual(len(self.analysis.missed_wins), 1)  # 2. ..Nc6 blunders #1
