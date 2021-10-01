import unittest
import move_evaluation
from chess.engine import *
from chess import WHITE, BLACK


class MoveEvaluationTest(unittest.TestCase):
    mate_in_four_white = Mate(4)
    mate_in_five_white = Mate(5)
    good_score_for_white = Cp(2000)

    def test_missed_win_for_black(self):
        self.assertTrue(move_evaluation._is_missed_win(self.mate_in_four_white,
                                                       self.good_score_for_white,
                                                       recognize_slower_mate=True))

    def test_recognize_slower_mate(self):
        self.assertTrue(move_evaluation._is_missed_win(self.mate_in_four_white,
                                                       self.mate_in_five_white,
                                                       recognize_slower_mate=True))

    def test_dont_recognize_slower_mate(self):
        self.assertFalse(move_evaluation._is_missed_win(self.mate_in_four_white,
                                                        self.mate_in_five_white,
                                                        recognize_slower_mate=False))

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


if __name__ == '__main__':
    unittest.main()
