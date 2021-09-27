import math


def generate_turn_string(move_counter: float, move_algebraic: str, use_context: bool) -> str:
    # black to move
    # when black moves, the notation can either be 10. ..b4 or just b4, depending on context
    if move_counter % 1 != 0:
        prefix = f"{math.floor(move_counter)}. .." if use_context else ''
        return f"{prefix}{move_algebraic}"
    # white to move
    else:
        return f'{int(move_counter)}. {move_algebraic}'
