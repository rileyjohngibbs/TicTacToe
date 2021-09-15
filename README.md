# Tic-Tac-Toe

Author: Riley John Gibbs

## Requirements

This requires Python 3, probably at least 3.7, but this hasn't been fully tested. Python 3.8 or 3.9 is recommended.

There are no other dependencies for using this.

## Usage

Download or clone this repo. Navigate in a shell to the repo's root directory and use:

```bash
python3.9 -m tictactoe
```

## Rules of Super Tic-Tac-Toe

Super Tic-Tac-Toe works like Tic-Tac-Toe with the following differences:

- The board is four squares on a side instead of three.
- Three squares in a row is not a victory; the player must have four squares.
- A player may also win by capturing all four corner squares of the board.
- A player may also win by capturing four adjacent squares forming a larger square. For example, this is a win for `X`:

    <img src="https://user-images.githubusercontent.com/5668445/133481670-d31ad93d-c017-4605-a312-f5a1314fa6fc.png" width=75 />
