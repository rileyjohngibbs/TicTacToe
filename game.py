from typing import Tuple

from base_game import BaseGame
from constants import Mark, VictoryPath


class Game(BaseGame):
    SIZE = 3
    VICTORY_PATHS: Tuple[VictoryPath] = (
        # Horizontal
        {(0, 0), (0, 1), (0, 2)},
        {(1, 0), (1, 1), (1, 2)},
        {(2, 0), (2, 1), (2, 2)},
        # Vertical
        {(0, 0), (1, 0), (2, 0)},
        {(0, 1), (1, 1), (2, 1)},
        {(0, 2), (1, 2), (2, 2)},
        # Diagonals
        {(0, 0), (1, 1), (2, 2)},
        {(2, 0), (1, 1), (0, 2)},
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