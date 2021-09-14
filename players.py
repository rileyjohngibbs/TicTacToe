from abc import ABC, abstractmethod
from collections import Counter
from copy import deepcopy
import math
from random import choice
import time
from typing import Set, Tuple

from base_game import BaseGame, Mark
from constants import Address
from game import Game
from supergame import Supergame


class Player(ABC):
    def __init__(self, speaker, listener):
        self.speaker = speaker
        self.listener = listener

    @abstractmethod
    def get_move(self, game: BaseGame) -> Tuple[int, int]:
        ...

    @abstractmethod
    def mood(self, game: BaseGame) -> str:
        ...


class Human(Player):
    def get_move(self, game: BaseGame) -> Tuple[int, int]:
        self.speaker("Where do you go?\nRow: ")

        valid_keys = self.valid_index_keys(game)

        rkey = None
        while rkey not in valid_keys:
            rkey = self.listener()
        row = int(rkey)
        self.speaker(f"{row}, Column: ")

        ckey = None
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
        return f"It's your turn."

    def __str__(self):
        return "The Human"


class RandomAI(Player):
    def get_move(self, game: BaseGame) -> Tuple[int, int]:
        options = game.open_squares()
        move = choice(list(options))
        self.speaker(f"{self} claims {move}. Press any key.\n")
        self.listener()
        return move

    def mood(self, game: BaseGame) -> str:
        return f"{self} is feeling impulsive."

    def __str__(self):
        return "The Random AI Agent"


class PeekAheadAI(Player):
    def get_move(self, game: BaseGame) -> Tuple[int, int]:
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


class FlawlessAI(Player):
    TIME_CUTOFF = 3

    def get_move(self, game: BaseGame) -> Tuple[int, int]:
        if self.is_first_move(game):
            if type(game) == Game:
                move = self.first_move_of_game(game)
            else:
                move = self.first_move_of_supergame(game)
        else:
            start_time = time.time()
            depth = 0
            while time.time() - start_time < self.TIME_CUTOFF:
                best_score = -2
                move = None
                for option in game.open_squares():
                    opt_score = self.score_move(game, option, depth)
                    if opt_score > best_score:
                        best_score = opt_score
                        move = option
                    if best_score == 1:
                        break
                depth += 1
                if best_score == 1:
                    break
        self.speaker(f"{self} claims {move}. Press any key.\n")
        self.listener()
        return move

    def is_first_move(self, game: BaseGame) -> bool:
        return len(game.open_squares()) >= game.SIZE**2 - 1

    def first_move_of_game(self, game: BaseGame) -> Address:
        options = game.open_squares()
        if len(options) == 9 or game.get_square_mark(1, 1) is not Mark.NOBODY:
            return choice(((0, 0), (0, 2), (2, 0), (2, 2)))
        else:
            return (1, 1)
    
    def first_move_of_supergame(self, game: Supergame) -> Address:
        squares_by_mark = game.get_squares_by_mark()
        options = squares_by_mark[Mark.NOBODY]
        if len(options) == 16:
            return (1, 1)
        else:
            marked_square = (squares_by_mark[Mark.X] | squares_by_mark[Mark.O]).pop()
            if marked_square in ((1, 1), (1, 2), (2, 1), (2, 2)):
                row = game.SIZE - marked_square[0] - 1
                column = marked_square[1]
                return (row, column)
            else:
                return (
                    1 + 1 * (marked_square[0] <= 1),
                    1 + 1 * (marked_square[1] <= 1),
                )

    def mood(self, game: BaseGame) -> str:
        if self.is_first_move(game):
            return f"{self} doesn't need to think about their first move."
        else:
            return f"{self} considers all possible outcomes before making their move."
    
    def score_move(self, game: BaseGame, move: Address, depth: int) -> float:
        hypothetical_game = game.__class__(deepcopy(game.board))
        hypothetical_game.mark_board(*move)
        sign = -1 if hypothetical_game.get_square_mark(*move) is Mark.O else 1
        
        winner = hypothetical_game.winner()
        if winner is not Mark.NOBODY:
            return 1

        if depth == 0:
            score = self.score_game_state(hypothetical_game)
            if score > 0:
                # Favors X, which is good if X just went
                return score
            elif score < 0:
                # Favors O, which is good if O just went
                return sign * score
            else:
                return 0

        next_moves = hypothetical_game.open_squares()
        best_score = 2
        for next_move in next_moves:
            score = -self.score_move(hypothetical_game, next_move, depth - 1)
            if score < best_score or score == best_score and choice([0, 1]):
                best_score = score
        return best_score
    
    def score_game_state(self, game: BaseGame) -> float:
        """A score of 1 means an X victory and a score of -1 means an O victory."""
        path_scores_sum = 0
        for path in game.VICTORY_PATHS:
            score = self.score_path(game, path)
            if score == game.SIZE**2:
                return 1
            if score == -game.SIZE**2:
                return -1
            path_scores_sum += score
        return 2 / (1 + math.e**(-path_scores_sum)) - 1
        
    
    def score_path(self, game: BaseGame, path: Set[Address]) -> int:
        """As a convention, O is negative and X is positive."""
        marks_counter = Counter(game.get_square_mark(*address) for address in path)
        x_count = marks_counter.get(Mark.X, 0)
        o_count = marks_counter.get(Mark.O, 0)
        if x_count and o_count:
            score = 0
        else:
            score = x_count**2 - o_count**2
        return score

    def __str__(self) -> str:
        return "The Flawless AI Agent"
