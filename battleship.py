#! /usr/bin/env python

from collections import namedtuple
from enum import Enum, auto
import random

import click


'''Welcome to Battleship! Below you'll find settings to adjust to your
liking. A few things to note while playing:
Grid Key:
0 - a blank cell on the grid
* - an unhit cell containing a piece of ship
! - a ship cell that has been hit
X - a shot taken that did not hit a ship'''
# Settings
GRID_SIZE = 10
SHIP_MIN = 2
SHIP_MAX = 5
NUM_SHIPS = 3
NUM_TURNS = 10


class Result(Enum):
    RETRY = auto()
    MISS = auto()
    HIT = auto()


ResultTuple = namedtuple('ResultTuple', ['result', 'message'])
ResultTuple.__new__.__defaults__ = (None, '')


class Game(object):
    def __init__(
        self, p1_name=None, p2_name='Computer', is_2p=False, debug=False
    ):
        self.ship_sizes = self.size_ships()
        self.is_2p = is_2p
        self.players = self.setup_players(p1_name, p2_name, debug=debug)
        self._active_player = 0
        self._last_result = ResultTuple(Result.MISS)

    def setup_players(self, p1_name, p2_name, **kwargs):
        return [
            Player(p1_name, self.ship_sizes, **kwargs),
            Player(
                p2_name, self.ship_sizes, is_computer=not self.is_2p, **kwargs
            )
        ]

    # determine ship lengths
    def size_ships(self):
        return [random.randint(SHIP_MIN, SHIP_MAX) for _ in range(NUM_SHIPS)]

    @property
    def over(self):
        if self.is_2p:
            return any(x.board.is_finished for x in self.players)
        else:
            return any(x.out_of_turns for x in self.players)

    @property
    def player(self):
        return self.players[self._active_player]

    @property
    def opponent(self):
        return self.players[{0: 1, 1: 0}[self._active_player]]

    def switch_turns(self):
        self._active_player = {0: 1, 1: 0}[self._active_player]

    def fire_shot(self, guess_row, guess_col):
        resulttuple = self.opponent.board.fire_shot(guess_row, guess_col)
        if resulttuple.result is Result.RETRY:
            return resulttuple
        if self.is_2p:
            self.switch_turns()
        else:
            if resulttuple.result is Result.MISS:
                self.player.use_turn()
        return resulttuple

    def play(self):
        self.setup()
        while not self.over:
            self.do_turn()
        self.end_game()

    def setup(self):
        if self.is_2p:
            for player in self.players:
                player.do_board_setup()

    def do_turn(self):
        self._last_result = ResultTuple(Result.RETRY, self._last_result.message)
        while self._last_result.result is Result.RETRY:
            self.opponent.board.print_board(hide_ships=True)
            if self._last_result.message:
                click.echo(self._last_result.message)
            if not self.is_2p:
                click.echo(
                    f'{self.player.name} has '
                    f'{self.player.turns_remaining} turns remaining.'
                )
            click.echo('Your turn, {}'.format(self.player.name))
            guess_col = get_valid_coordinate('col')
            guess_row = get_valid_coordinate('row')
            self._last_result = self.fire_shot(guess_row, guess_col)

    def end_game(self):
        click.secho('Game over!', bg='green', fg='red')
        if self.is_2p:
            opponent_done = self.opponent.board.is_finished
            winner = self.player if opponent_done else self.opponent
            click.secho('{} wins!'.format(winner.name), fg='green')
        else:
            status = self.opponent.board.is_finished
            result, color = {
                True: ('won', 'green'),
                False: ('lost', 'red')
            }[status]
            click.secho(f'You {result}!', fg=color)
        click.secho('Thanks for playing Battleship!', fg='blue')


class Player(object):
    def __init__(self, name, ship_sizes, is_computer=False, debug=False):
        self.name = name
        self.board = BoardSet(ship_sizes, autofill=is_computer, debug=debug)
        self.turns_remaining = NUM_TURNS

    def use_turn(self):
        self.turns_remaining -= 1

    @property
    def out_of_turns(self):
        return self.turns_remaining <= 0

    def do_board_setup(self):
        click.secho(f"Time to set up {self.name}'s ships", fg='green')
        click.pause()
        for ship in self.board.ship_sizes:
            self.board.player_build_ship(ship)
        click.clear()
        click.secho('Great, all set!', fg='green')
        click.pause()


class BoardSet(object):
    empty_cell = '0'
    ship_cell = click.style('*', fg='blue')
    hit_cell = click.style('!', fg='green')
    miss_cell = click.style('X', fg='red')
    horizontal = 'hor'
    vertical = 'vert'
    valid_orientations = [horizontal, vertical]
    untried = (empty_cell, ship_cell)

    def __init__(self, ship_sizes, autofill=True, debug=False):
        self.size = GRID_SIZE
        self.ship_board = self.generate_board()
        self.ship_sizes = ship_sizes
        self.debug = debug
        if autofill:
            for ship in self.ship_sizes:
                self.autofill_ship(ship)

    def generate_board(self):
        return [[self.empty_cell] * self.size for _ in range(self.size)]

    def _prep_row(self, row, hide_ships):
        if self.debug or not hide_ships:
            return row
        return self._hide_ships(row)

    def print_board(self, hide_ships=False, message=''):
        click.clear()
        for row in self.ship_board:
            click.echo(' '.join(self._prep_row(row, hide_ships)))
        if message:
            click.echo(message)

    def _hide_ships(self, row):
        return [x.replace(self.ship_cell, self.empty_cell) for x in row]

    def fire_shot(self, guess_row, guess_col):
        cell = self.get_cell(guess_row, guess_col)
        if cell in self.untried:
            self.mark_board(
                guess_row, guess_col, {
                    self.empty_cell: self.miss_cell,
                    self.ship_cell: self.hit_cell
                }[cell]
            )
            resulttuple = {
                self.empty_cell: ResultTuple(Result.MISS, 'You missed!'),
                self.ship_cell: ResultTuple(Result.HIT, 'A hit!')
            }[cell]
        else:
            resulttuple = ResultTuple(
                Result.RETRY, 'You already guessed that one!'
            )
        return resulttuple

    def mark_board(self, guess_row, guess_col, mark=None):
        mark = mark or self.miss_cell
        self.ship_board[guess_row][guess_col] = mark
        return self.ship_board

    def get_cell(self, row, col):
        return self.ship_board[row][col]

    @property
    def is_finished(self):
        return not any(self.ship_cell in row for row in self.ship_board)

    def player_build_ship(self, length):
        self.print_board()
        click.secho(f'This ship is {length} cells long.', fg='green')
        orientation = click.prompt(
            'Should it be horizontal (hor) or vertical (vert)?',
            type=click.Choice(self.valid_orientations)
        )
        row_max, col_max = self.get_maxes(orientation, length)
        is_inserted = False
        while not is_inserted:
            click.secho('What cell should it start on?', fg='green')
            start_col = get_valid_coordinate('col', col_max + 1)
            start_row = get_valid_coordinate('row', row_max + 1)
            is_inserted = self.insert_ship(orientation, length,
                                           start_row, start_col)
            if not is_inserted:
                click.secho('That overlaps another ship! Try again!', fg='red')

    def autofill_ship(self, length):
        orientation = random.choice(self.valid_orientations)
        row_max, col_max = self.get_maxes(orientation, length)
        is_inserted = False
        while not is_inserted:
            start_row = random.randint(0, row_max)
            start_col = random.randint(0, col_max)
            is_inserted = self.insert_ship(orientation, length,
                                           start_row, start_col)

    def _build_static_axis(self, start_coord, length):
        return [start_coord] * length

    def _build_dynamic_axis(self, start_coord, length):
        return [start_coord + x for x in range(length)]

    def insert_ship(self, orientation, length, start_row, start_col):
        row_builder, col_builder = {
            self.horizontal: (
                self._build_static_axis, self._build_dynamic_axis
            ),
            self.vertical: (self._build_dynamic_axis, self._build_static_axis)
        }[orientation]
        coords = list(zip(
            row_builder(start_row, length), col_builder(start_col, length)
            ))
        if any(self.get_cell(*x) != self.empty_cell for x in coords):
            return False
        for coord in coords:
            self.mark_board(*coord, mark=self.ship_cell)
        return True

    def get_maxes(self, orientation, length):
        big_max = GRID_SIZE - 1
        small_max = GRID_SIZE - length
        return {
            self.horizontal: (big_max, small_max),
            self.vertical: (small_max, big_max)
        }[orientation]


def get_valid_coordinate(category, biggest=GRID_SIZE):
    msg = f'Enter {category} in range 1-{biggest}'
    return click.prompt(msg, type=click.IntRange(1, biggest)) - 1


def get_player_name(player_num):
    return click.prompt(f'Player {player_num} name?')


# begin game
@click.command()
@click.option(
    '--number-of-players',
    '-n',
    type=click.IntRange(1, 2),
    prompt="How many players?"
)
@click.option('--debug', is_flag=True)
def start_game(number_of_players, debug):
    click.secho("Let's play Battleship!", fg='green')
    game = Game(p1_name=get_player_name(1),
                p2_name=get_player_name(2) if number_of_players == 2 else None,
                is_2p=(number_of_players == 2), debug=debug)
    game.play()


if __name__ == "__main__":
    start_game()
