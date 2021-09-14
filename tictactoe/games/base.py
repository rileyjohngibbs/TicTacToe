from abc import ABC, abstractmethod
from copy import deepcopy
from itertools import product
from typing import Optional

from tictactoe.constants import Mark, SquareFilled, Address, VictoryPath


class BaseGame(ABC):
    @property
    @abstractmethod
    def SIZE(self) -> int:
        ...

    @property
    @abstractmethod
    def VICTORY_PATHS(self) -> tuple[VictoryPath, ...]:
        ...

    @property
    @abstractmethod
    def NAME(self) -> str:
        ...

    @abstractmethod
    def winner(self) -> Mark:
        ...

    board: list[list[Mark]]

    def __init__(self, starting_board: Optional[list[list[Mark]]] = None):
        if starting_board:
            self.board = starting_board
        else:
            self.board = [
                [Mark.NOBODY for _ in range(self.SIZE)] for _ in range(self.SIZE)
            ]

    def get_board(self) -> list[list[Mark]]:
        return deepcopy(self.board)

    def get_square_mark(self, row: int, column: int) -> Mark:
        return self.board[row][column]

    def open_squares(self) -> set[Address]:
        return self.get_squares_by_mark()[Mark.NOBODY]

    def next_mark(self) -> Mark:
        squares_by_mark = self.get_squares_by_mark()
        if len(squares_by_mark[Mark.NOBODY]) == 0:
            next_mark = Mark.NOBODY
        elif len(squares_by_mark[Mark.X]) > len(squares_by_mark[Mark.O]):
            next_mark = Mark.O
        else:
            next_mark = Mark.X
        return next_mark

    def mark_board(
        self, row: int, col: int, mark: Optional[Mark] = None, force: bool = False
    ) -> None:
        if self.board[row][col] is not Mark.NOBODY and not force:
            raise SquareFilled(self.board[row][col])
        if mark is None:
            mark = self.next_mark()
        self.board[row][col] = mark

    def get_squares_by_mark(self) -> dict[Mark, set[Address]]:
        addresses = product(range(self.SIZE), range(self.SIZE))
        squares_by_mark: dict[Mark, set[Address]] = {m: set() for m in Mark}
        for address in addresses:
            mark = self.get_square_mark(*address)
            squares_by_mark[mark].add(address)
        return squares_by_mark
