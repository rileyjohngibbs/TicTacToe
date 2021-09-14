from itertools import product
from typing import Tuple

from base_game import BaseGame
from constants import Mark, VictoryPath

SIZE = 4

class Supergame(BaseGame):
    SIZE = SIZE
    CORNER_PATHS: Tuple[VictoryPath] = (
        {(0, 0), (0, SIZE - 1), (SIZE - 1, 0), (SIZE - 1, SIZE - 1)},
    )
    SQUARE_PATHS: Tuple[VictoryPath] = tuple(
        {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
        for x, y in product(range(SIZE - 1), range(SIZE - 1))
    )
    ROW_PATHS: Tuple[VictoryPath] = tuple(
        {(r, c) for c in range(SIZE)}
        for r in range(SIZE)
    )
    COLUMN_PATHS: Tuple[VictoryPath] = tuple(
        {(r, c) for r in range(SIZE)}
        for c in range(SIZE)
    )
    DIAGONAL_PATHS: Tuple[VictoryPath] = (
        {(r, SIZE - r - 1) for r in range(SIZE)},
        {(r, r) for r in range(SIZE)},
    )
    VICTORY_PATHS: Tuple[VictoryPath] = (
        CORNER_PATHS
        + SQUARE_PATHS
        + ROW_PATHS
        + COLUMN_PATHS
        + DIAGONAL_PATHS
    )

    def winner(self) -> Mark:
        squares_by_mark = self.get_squares_by_mark()
        winner = Mark.NOBODY
        for mark in (Mark.X, Mark.O):
            squares = squares_by_mark[mark]
            for victory_path in self.VICTORY_PATHS:
                if victory_path.issubset(squares):
                    winner = mark
                    break
            if winner is not Mark.NOBODY:
                break
        return winner
