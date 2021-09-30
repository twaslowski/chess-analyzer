import math
from dataclasses import dataclass
from typing import Tuple

import chess
from chess.engine import InfoDict

import board_util


@dataclass()
class MoveEvaluation:
    board: chess.Board
    turn: int
    move: chess.Move
    analyses: Tuple[InfoDict, InfoDict]  # prev_analysis is 0, current_analysis is 1

    def __post_init__(self):
        self.prev_analysis = self.analyses[0]
        self.prev_score = self.prev_analysis.get('score')
        self.current_analysis = self.analyses[1]
        self.current_score = self.current_analysis.get('score')
        self.continuation = self.prev_analysis.get('pv')[:6]

    def stringify(self) -> str:
        # setup
        prev_move = self.board.pop()
        move_algebraic = self.board.san(self.move)

        result_string = ''
        result_string += f"{board_util.generate_turn_string(self.turn, move_algebraic, True)}"
        result_string += f"({str(self.prev_score)} to {str(self.current_score)})\n"
        result_string += f"Alternative and Continuation: {self._generate_alternative_line_algebraic(prev_move)}" \
                         f"(depth: {self.prev_analysis.get('depth')})\n"
        return result_string

    def _generate_alternative_line_algebraic(self, prev_move) -> str:
        # create string for alternative line
        turn_counter = self.turn
        alternative_line_algebraic_string = ''
        for i in range(len(self.continuation)):
            move_algebraic = self.board.san(self.continuation[i])
            if i == 0:
                turn_string = board_util.generate_turn_string(turn_counter, move_algebraic, True)
            else:
                turn_string = board_util.generate_turn_string(turn_counter, move_algebraic, False)
            alternative_line_algebraic_string += f"{turn_string}"
            self.board.push(self.continuation[i])
            turn_counter += 0.5

        # clean up
        for i in range(len(self.continuation)):
            self.board.pop()
        self.board.push(prev_move)

        return alternative_line_algebraic_string


def _calculate_absolute_score(relative_score):
    if relative_score.white().is_mate():
        return -100
    else:
        return int(str(relative_score.white())) / 100


def _is_significant(prev_score, score):
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
