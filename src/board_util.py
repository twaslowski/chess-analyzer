import math


def generate_turn_string(move_counter: float, move_algebraic: str, use_context: bool) -> str:
    if move_counter % 1 != 0:
        prefix = f"{math.floor(move_counter)}. .." if use_context else ' '
        return f"{prefix}{move_algebraic} "
    else:
        return f'{int(move_counter)}. {move_algebraic}'
