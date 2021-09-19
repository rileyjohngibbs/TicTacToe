from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
import math
from random import choice
import time
from typing import Any, Set, Tuple, cast

from tictactoe.players.base import Player
from tictactoe.games import BaseGame, Game, Supergame
from tictactoe.constants import Address, Mark


@dataclass
class MoveScore:
    score: float
    depth: int

    def __neg__(self) -> "MoveScore":
        return MoveScore(-self.score, self.depth)

    def __lt__(self, other: Any) -> bool:
        if type(other) != MoveScore:
            raise TypeError(f"Cannot compare MoveScore to type {type(other)}")
        return self._comp_tuple() < cast(MoveScore, other)._comp_tuple()

    def __eq__(self, other: Any) -> bool:
        if type(other) != MoveScore:
            raise TypeError(f"Cannot compare MoveScore to type {type(other)}")
        return self._comp_tuple() == cast(MoveScore, other)._comp_tuple()

    def _comp_tuple(self) -> Tuple[float, int]:
        if self.score < 0:
            depth = self.depth
        else:
            depth = -self.depth
        return (self.score, depth)

    def bump(self) -> "MoveScore":
        return MoveScore(self.score, self.depth + 1)


class FlawlessAI(Player):
    NAME = "The Flawless AI Agent"
    TIME_CUTOFF = 3

    def get_move(self, game: BaseGame) -> Tuple[int, int]:
        if self.is_first_move(game):
            if type(game) == Game:
                move = self.first_move_of_game(cast(Game, game))
            else:
                move = self.first_move_of_supergame(cast(Supergame, game))
        elif type(game) == Supergame and self.is_second_move(game):
            move = self.second_move_of_supergame(cast(Supergame, game))
        else:
            start_time = time.time()
            depth = 0
            while time.time() - start_time < self.TIME_CUTOFF:
                best_score = MoveScore(-2.0, 0)
                move = (game.SIZE, game.SIZE)
                for option in game.open_squares():
                    opt_score = self.score_move(game, option, depth)
                    if opt_score > best_score:
                        best_score = opt_score
                        move = option
                    if best_score.score == 1.0:
                        break
                depth += 1
                if best_score.score == 1.0:
                    break
        self.speaker(f"{self} claims {move}. Press any key.\n")
        self.listener()
        return move

    def is_first_move(self, game: BaseGame) -> bool:
        return len(game.open_squares()) >= game.SIZE ** 2 - 1

    def is_second_move(self, game: BaseGame) -> bool:
        return game.SIZE ** 2 - 3 <= len(game.open_squares()) < game.SIZE ** 2 - 1

    def first_move_of_game(self, game: Game) -> Address:
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
                    1 + 1 * (marked_square[0] > 1),
                    1 + 1 * (marked_square[1] > 1),
                )

    def second_move_of_supergame(self, game: Supergame) -> Address:
        squares_by_mark = game.get_squares_by_mark()
        if game.next_mark() is Mark.O:
            if squares_by_mark[Mark.X] == {(1, 1), (1, 2)}:
                if squares_by_mark[Mark.O] == {(2, 1)}:
                    move = (1, 3)
                else:
                    move = (1, 0)
            elif squares_by_mark[Mark.X] == {(2, 1), (2, 2)}:
                if squares_by_mark[Mark.O] == {(1, 1)}:
                    move = (2, 3)
                else:
                    move = (2, 0)
            else:
                move = max(squares_by_mark[Mark.NOBODY], key=lambda m: self.score_move(game, m, 2))
        if game.next_mark() is Mark.X:
            if squares_by_mark[Mark.O] == {(2, 2)}:
                move = (1, 0)
            elif squares_by_mark[Mark.O] & {(1, 2)}:
                move = (2, 1)
            else:
                move = (1, 2)
        return move

    def mood(self, game: BaseGame) -> str:
        if self.is_first_move(game):
            return f"{self} doesn't need to think about their first move."
        else:
            return f"{self} considers all possible outcomes before making their move."

    def score_move(self, game: BaseGame, move: Address, depth: int) -> MoveScore:
        hypothetical_game = game.__class__(deepcopy(game.board))
        hypothetical_game.mark_board(*move)

        winner = hypothetical_game.winner()
        if winner is not Mark.NOBODY:
            return MoveScore(1, 0)

        if depth == 0:
            state_score = self.score_game_state(hypothetical_game)
            if state_score > 0:
                # Favors X, which is good if X just went
                return MoveScore(state_score, 0)
            elif state_score < 0:
                # Favors O, which is good if O just went
                sign = -1 if hypothetical_game.get_square_mark(*move) is Mark.O else 1
                return MoveScore(sign * state_score, 0)
            else:
                return MoveScore(0.0, 0)

        next_moves = hypothetical_game.open_squares()
        if not next_moves:  # Tie game
            return MoveScore(0.0, 0)

        minimized_score = MoveScore(2.0, 0)
        for next_move in next_moves:
            score = -self.score_move(hypothetical_game, next_move, depth - 1).bump()
            if score < minimized_score or score == minimized_score and choice([0, 1]):
                minimized_score = score
                if minimized_score.score == -1.0:
                    break
        return minimized_score

    def score_game_state(self, game: BaseGame) -> float:
        """A score of 1 means an X victory and a score of -1 means an O victory."""
        path_scores_sum = 0
        for path in game.VICTORY_PATHS:
            score = self.score_path(game, path)
            if score == game.SIZE ** 2:
                return 1
            if score == -game.SIZE ** 2:
                return -1
            path_scores_sum += score
        return 2 / (1 + math.e ** (-path_scores_sum)) - 1

    def score_path(self, game: BaseGame, path: Set[Address]) -> int:
        """As a convention, O is negative and X is positive."""
        marks_counter = Counter(game.get_square_mark(*address) for address in path)
        x_count = marks_counter.get(Mark.X, 0)
        o_count = marks_counter.get(Mark.O, 0)
        if x_count and o_count:
            score = 0
        else:
            score = x_count ** 2 - o_count ** 2
        return score
