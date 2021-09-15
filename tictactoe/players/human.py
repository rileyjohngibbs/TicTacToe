from typing import Set, Tuple

from tictactoe.games import BaseGame

from .base import Player


class Human(Player):
    NAME = "The Human"

    def get_move(self, game: BaseGame) -> Tuple[int, int]:
        self.speaker("Where do you go?\nRow: ")

        valid_keys = self.valid_index_keys(game)

        rkey = "-1"
        while rkey not in valid_keys:
            rkey = self.listener()
        row = int(rkey)
        self.speaker(f"{row}, Column: ")

        ckey = "-1"
        while ckey not in valid_keys:
            ckey = self.listener()
        col = int(ckey)
        self.speaker(f"{col}\n")

        move = (row, col)
        self.speaker(f"{self} claims {move}. Press any key.\n")
        self.listener()
        return row, col

    def valid_index_keys(self, game: BaseGame) -> Set[str]:
        return {str(n) for n in range(game.SIZE)}

    def mood(self, game: BaseGame) -> str:
        return "It's your turn."
