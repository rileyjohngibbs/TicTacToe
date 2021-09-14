from copy import deepcopy
from random import choice

from tictactoe.games import BaseGame
from tictactoe.constants import Mark

from .base import Player


class PeekAheadAI(Player):
    def get_move(self, game: BaseGame) -> tuple[int, int]:
        options = game.open_squares()
        own_mark = game.next_mark()
        opponent_mark = Mark.X if own_mark is Mark.O else Mark.O
        winning_move, defensive_move = None, None
        for option in options:
            hypothetical_game = game.__class__(deepcopy(game.board))
            hypothetical_game.mark_board(*option, own_mark)
            if hypothetical_game.winner() is own_mark:
                winning_move = option
            if defensive_move is None:
                hypothetical_game.mark_board(*option, opponent_mark, force=True)
                if hypothetical_game.winner() is opponent_mark:
                    defensive_move = option
        move = winning_move or defensive_move or choice(list(options))
        self.speaker(f"{self} claims {move}. Press any key.\n")
        self.listener()
        return move

    def mood(self, game: BaseGame) -> str:
        if len(game.open_squares()) == 1:
            return f"{self} doesn't have much to think about."
        else:
            return f"{self} considers their options."

    def __str__(self):
        return "The Peek Ahead AI Agent"
