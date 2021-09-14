from random import choice

from tictactoe.games import BaseGame

from .base import Player


class RandomAI(Player):
    def get_move(self, game: BaseGame) -> tuple[int, int]:
        options = game.open_squares()
        move = choice(list(options))
        self.speaker(f"{self} claims {move}. Press any key.\n")
        self.listener()
        return move

    def mood(self, game: BaseGame) -> str:
        return f"{self} is feeling impulsive."

    def __str__(self):
        return "The Random AI Agent"
