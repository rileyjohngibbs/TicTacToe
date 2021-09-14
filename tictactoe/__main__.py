from curses import wrapper

from tictactoe.constants import Mark, SquareFilled
from tictactoe.games import Game, Supergame
from tictactoe.players import FlawlessAI, Human, PeekAheadAI, Player, RandomAI


def main(stdscr):
    game = Supergame()
    players = {
        Mark.X: Human(speaker=stdscr.addstr, listener=stdscr.getkey),
        Mark.O: FlawlessAI(
            speaker=lambda m: stdscr.addstr(m) or stdscr.refresh(),
            listener=stdscr.getkey,
        ),
    }
    next_mark = game.next_mark()
    winner = game.winner()
    stdscr.addstr(display_game(game, players) + "\n")
    while winner is Mark.NOBODY and next_mark is not Mark.NOBODY:
        current_player = players[next_mark]
        stdscr.addstr(current_player.mood(game) + "\n")
        stdscr.refresh()
        move = current_player.get_move(game)
        stdscr.clear()
        try:
            game.mark_board(*move)
        except SquareFilled:
            if type(players[next_mark]) == Human:
                stdscr.addstr(display_game(game, players) + "\n")
                stdscr.addstr("That square is filled already." + "\n")
                continue
            else:
                raise
        stdscr.addstr(display_game(game, players) + "\n")
        next_mark = game.next_mark()
        winner = game.winner()
    if winner is not Mark.NOBODY:
        stdscr.addstr(f"The winner is {players[winner]}!\n")
    else:
        stdscr.addstr("Cat's game!\n")
    stdscr.getkey()


def display_game(game: Game, players: dict[Mark, Player]) -> str:
    header = f"X: {players[Mark.X]}\nO: {players[Mark.O]}"
    board = f"\n{'+'.join('-' for _ in range(game.SIZE))}\n".join(
        "|".join(str(square) for square in row) for row in game.board
    )
    return f"{header}\n\n{board}\n"


if __name__ == "__main__":
    wrapper(main)
