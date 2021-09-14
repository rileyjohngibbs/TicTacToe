from itertools import product

from tictactoe.constants import Mark, VictoryPath

from .base import BaseGame

SUPERGAME_SIZE = 4  # Was getting a NameError before so /shrug
CORNER_PATHS: tuple[VictoryPath, ...] = (
    {
        (0, 0),
        (0, SUPERGAME_SIZE - 1),
        (SUPERGAME_SIZE - 1, 0),
        (SUPERGAME_SIZE - 1, SUPERGAME_SIZE - 1),
    },
)
SQUARE_PATHS: tuple[VictoryPath, ...] = tuple(
    {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
    for x, y in product(range(SUPERGAME_SIZE - 1), range(SUPERGAME_SIZE - 1))
)
ROW_PATHS: tuple[VictoryPath, ...] = tuple(
    {(r, c) for c in range(SUPERGAME_SIZE)} for r in range(SUPERGAME_SIZE)
)
COLUMN_PATHS: tuple[VictoryPath, ...] = tuple(
    {(r, c) for r in range(SUPERGAME_SIZE)} for c in range(SUPERGAME_SIZE)
)
DIAGONAL_PATHS: tuple[VictoryPath, ...] = (
    {(r, SUPERGAME_SIZE - r - 1) for r in range(SUPERGAME_SIZE)},
    {(r, r) for r in range(SUPERGAME_SIZE)},
)


class Supergame(BaseGame):
    SIZE = SUPERGAME_SIZE
    VICTORY_PATHS: tuple[VictoryPath, ...] = (
        CORNER_PATHS + SQUARE_PATHS + ROW_PATHS + COLUMN_PATHS + DIAGONAL_PATHS
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
