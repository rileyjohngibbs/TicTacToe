from curses import wrapper

from tictactoe.constants import Mark, SquareFilled
from tictactoe.games import BaseGame, Game, Supergame
from tictactoe.players import FlawlessAI, Human, PeekAheadAI, Player, RandomAI


def main(stdscr):
    game_type = ask_game_type(stdscr)
    game = game_type()
    player_x_type = ask_player_type(stdscr, "X")
    player_o_type = ask_player_type(stdscr, "O")
    players = {
        Mark.X: player_x_type(speaker=stdscr.addstr, listener=stdscr.getkey),
        Mark.O: player_o_type(speaker=stdscr.addstr, listener=stdscr.getkey),
    }
    next_mark = game.next_mark()
    winner = game.winner()
    stdscr.clear()
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


def ask_game_type(stdscr) -> type[BaseGame]:
    game_choices = [Game, Supergame]
    stdscr.addstr("What kind of game do you want to play?\n")
    for i, game in enumerate(game_choices):
        stdscr.addstr(f"{i}: {game.NAME}\n")
    answer = "-1"
    while answer not in [str(x) for x in range(len(game_choices))]:
        answer = stdscr.getkey()
    return game_choices[int(answer)]


def ask_player_type(stdscr, player_name: str) -> type[Player]:
    player_choices = [Human, RandomAI, PeekAheadAI, FlawlessAI]
    stdscr.addstr(f"Who will be {player_name}?\n")
    for i, player in enumerate(player_choices):
        stdscr.addstr(f"{i}: {player.NAME}\n")
    answer = "-1"
    while answer not in [str(x) for x in range(len(player_choices))]:
        answer = stdscr.getkey()
    return player_choices[int(answer)]


def display_game(game: Game, players: dict[Mark, Player]) -> str:
    header = f"X: {players[Mark.X]}\nO: {players[Mark.O]}"
    board = f"\n{'+'.join('-' for _ in range(game.SIZE))}\n".join(
        "|".join(str(square) for square in row) for row in game.board
    )
    return f"{header}\n\n{board}\n"


if __name__ == "__main__":
    wrapper(main)
