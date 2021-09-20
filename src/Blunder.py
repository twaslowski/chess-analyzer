import chess
from typing import Tuple, List
from dataclasses import dataclass
import board_util


@dataclass()
class Blunder:
    board: chess.Board
    scores: Tuple[float, float]  # prev_score is 0, new_score is 1
    turn: int
    move: chess.Move
    continuation: List[chess.Move]

    def stringify(self) -> str:
        # setup
        prev_move = self.board.pop()
        move_algebraic = self.board.san(self.move)

        result_string = ''
        result_string += f"{board_util.generate_turn_string(self.turn, move_algebraic, True)}"
        result_string += f"({str(self.scores[0])} to {str(self.scores[1])})\n"
        result_string += f"Alternative and Continuation: {self._generate_alternative_line_algebraic(prev_move)}"
        return result_string

    def _generate_alternative_line_algebraic(self, prev_move) -> str:
        # create string for alternative line
        turn_counter = self.turn
        alternative_line_algebraic_string = ''
        for move in self.continuation:
            move_algebraic = self.board.san(move)
            turn_string = board_util.generate_turn_string(turn_counter, move_algebraic, True)
            alternative_line_algebraic_string += f"{turn_string} "
            self.board.push(move)
            turn_counter += 0.5

        # clean up
        for i in range(len(self.continuation)):
            self.board.pop()
        self.board.push(prev_move)

        return alternative_line_algebraic_string
