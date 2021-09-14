from enum import Enum
from typing import Set, Tuple


class Mark(Enum):
    NOBODY = 0
    X = 1
    O = 2

    def __str__(self):
        if self is self.NOBODY:
            return " "
        else:
            return self.name


class SquareFilled(Exception):
    pass


Address = Tuple[int, int]
VictoryPath = Set[Address]