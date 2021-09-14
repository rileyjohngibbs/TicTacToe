from copy import deepcopy
from itertools import product


def rotate(board, inverse=False):
    new_board = deepcopy(board)
    for j, row in enumerate(board):
        for i, mark in enumerate(row):
            if not inverse:
                new_board[3 - j][i] = mark
            else:
                new_board[j][3 - i] = mark
    return new_board


def vflip(board, inverse=False):
    new_board = deepcopy(board)
    for j, row in enumerate(board):
        for i, mark in enumerate(row):
            new_board[3 - i][j] = mark
    return new_board


def hflip(board, inverse=False):
    new_board = deepcopy(board)
    for j, row in enumerate(board):
        for i, mark in enumerate(row):
            new_board[i][3 - j] = mark
    return new_board


def match(board, target):
    for 