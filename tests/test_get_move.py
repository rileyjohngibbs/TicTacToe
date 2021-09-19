import pytest
from unittest import mock

from tictactoe.constants import Mark
from tictactoe.games import Supergame
from tictactoe.players import FlawlessAI

X = Mark.X
Q = Mark.O
_ = Mark.NOBODY


@pytest.fixture
def agent():
    return FlawlessAI(mock.MagicMock(), mock.MagicMock())


def test_score_short_win_over_long_win(agent):
    board = [
        [X, _, _, _],
        [X, X, Q, _],
        [_, _, Q, _],
        [_, _, _, _],
    ]
    game = Supergame(board)
    assert type(agent.get_move(game)) == tuple
