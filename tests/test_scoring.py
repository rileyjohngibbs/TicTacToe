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


def test_score_supergame_x_victory(agent):
    board = [
        [X, X, X, X],
        [Q, _, Q, _],
        [_, Q, _, Q],
        [_, _, _, _],
    ]
    game = Supergame(board)
    assert agent.score_game_state(game) == 1


def test_score_supergame_o_victory(agent):
    board = [
        [X, _, X, _],
        [Q, Q, Q, Q],
        [_, X, _, X],
        [_, _, _, _],
    ]
    game = Supergame(board)
    assert agent.score_game_state(game) == -1


def test_score_tie(agent):
    board = [
        [X, X, Q, Q],
        [Q, Q, X, X],
        [X, X, Q, Q],
        [Q, Q, X, X],
    ]
    game = Supergame(board)
    assert agent.score_game_state(game) == 0


def test_score_winning_move(agent):
    board = [
        [X, X, X, _],
        [Q, Q, Q, _],
        [_, _, _, _],
        [_, _, _, _],
    ]
    game = Supergame(board)
    assert agent.score_move(game, (0, 3), 1).score == 1


def test_score_miss_block(agent):
    board = [
        [X, X, X, _],
        [Q, Q, Q, _],
        [_, _, _, _],
        [_, _, _, _],
    ]
    game = Supergame(board)
    assert agent.score_move(game, (2, 3), 1).score == -1


def test_score_miss_block_o(agent):
    board = [
        [_, _, _, _],
        [X, X, X, _],
        [_, Q, Q, _],
        [_, _, _, _],
    ]
    game = Supergame(board)
    assert agent.score_move(game, (2, 0), 1).score == -1


def test_score_force_tie(agent):
    board = [
        [_, Q, _, X],
        [X, X, Q, X],
        [Q, X, _, Q],
        [Q, _, X, _],
    ]
    game = Supergame(board)
    assert agent.score_move(game, (2, 2), 5).score == 0


@pytest.mark.parametrize("move", [(0, 0), (2, 2)])
def test_score_bad_second_move(agent, move):
    board = [
        [_, _, _, _],
        [_, X, X, _],
        [_, Q, _, _],
        [_, _, _, _],
    ]
    game = Supergame(board)
    assert agent.score_move(game, move, 5).score == -1


@pytest.mark.parametrize("move", [(1, 3)])
def test_score_good_second_move(agent, move):
    board = [
        [_, _, _, _],
        [_, X, X, _],
        [_, Q, _, _],
        [_, _, _, _],
    ]
    game = Supergame(board)
    assert agent.score_move(game, move, 5).score > -1


@pytest.mark.parametrize("center,move", [
    ((X, X, Q, _), (1, 3)),
    ((X, X, _, Q), (1, 0)),
    ((Q, _, X, X), (2, 3)),
    ((_, Q, X, X), (2, 0)),
])
def test_pick_second_move(agent, center, move):
    board = [
        [_, _, _, _],
        [_, *center[:2], _],
        [_, *center[2:], _],
        [_, _, _, _],
    ]
    game = Supergame(board)
    assert agent.get_move(game) == move


def test_score_long_loss_over_short_loss(agent):
    board = [
        [X, X, _, _],
        [_, X, _, _],
        [_, _, _, _],
        [Q, Q, _, _],
    ]
    game = Supergame(board)
    assert agent.score_move(game, (1, 0), 3) > agent.score_move(game, (3, 3), 3)
