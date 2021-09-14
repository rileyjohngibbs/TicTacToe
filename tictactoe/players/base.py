from abc import ABC, abstractmethod
from typing import Callable, Tuple

from tictactoe.games import BaseGame


class Player(ABC):
    # speaker: Callable[[str], None]
    # listener: Callable[[], str]

    def __init__(self, speaker: Callable[[str], None], listener: Callable[[], str]):
        self.speaker = speaker
        self.listener = listener

    @abstractmethod
    def get_move(self, game: BaseGame) -> Tuple[int, int]:
        ...

    @abstractmethod
    def mood(self, game: BaseGame) -> str:
        ...
