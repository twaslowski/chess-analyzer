import unittest
import move_evaluation
from chess.engine import *
from chess import WHITE, BLACK


class MoveEvaluationTest(unittest.TestCase):

    def test_absolute_score_black(self):
        self.assertEqual(
            move_evaluation._make_score_absolute(PovScore(Cp(-200), BLACK)), Cp(200))

    def test_absolute_score_white(self):
        self.assertEqual(
            move_evaluation._make_score_absolute(PovScore(Cp(-200), WHITE)), Cp(-200))

    def test_absolute_score_black_mate(self):
        self.assertEqual(
            move_evaluation._make_score_absolute(PovScore(Mate(5), BLACK)), Mate(-5))

    def test_absolute_score_white_mate(self):
        self.assertEqual(
            move_evaluation._make_score_absolute(PovScore(Mate(5), WHITE)), Mate(5))

    def test_format_score(self):
        self.assertEqual(move_evaluation._format_score(Cp(583)), "5.83")

    def test_format_score_negative(self):
        self.assertEqual(move_evaluation._format_score(Cp(-583)), "-5.83")

    def test_format_score_mate_negative(self):
        self.assertEqual(move_evaluation._format_score(Mate(-4)), "#4")

    def test_format_score_mate(self):
        self.assertEqual(move_evaluation._format_score(Mate(4)), "#4")


if __name__ == '__main__':
    unittest.main()
