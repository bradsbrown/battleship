import os
import random
from six.moves import input


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


# pull console height for use in screen clearing
SCREEN_HEIGHT = int(os.popen('stty size', 'r').read().split()[0])


class Game(object):
    def __init__(self, p1_name, p2_name='Computer', is_2p=False):
        self.ship_sizes = self.size_ships()
        self.is_2p = is_2p
        self.players = self.setup_players(p1_name, p2_name, self.is_2p)
        self._active_player = 0

    def setup_players(self, p1_name, p2_name, is_2p):
        if is_2p:
            return [Player(p1_name, self.ship_sizes, is_computer=False),
                    Player(p2_name, self.ship_sizes, is_computer=False)]
        return [Player(p1_name, self.ship_sizes, is_computer=False),
                Player(p2_name, self.ship_sizes)]

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
        result = self.opponent.board.fire_shot(guess_row, guess_col)
        if result is 'retry':
            return result
        if self.is_2p:
            self.switch_turns()
        else:
            if result == 'miss':
                self.player.use_turn()
            message = 'You have {} turns remaining'
            print(message.format(self.player.turns_remaining))
        return None

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
        result = 'retry'
        while result == 'retry':
            self.opponent.board.print_board()
            print('Your turn, {}'.format(self.player.name))
            guess_row = get_valid_coordinate('row')
            guess_col = get_valid_coordinate('col')
            result = self.fire_shot(guess_row, guess_col)

    def end_game(self):
        print('Game over!')
        if self.is_2p:
            opponent_done = self.opponent.board.is_finished
            winner = self.player if opponent_done else self.opponent
            print('{} wins!'.format(winner.name))
        else:
            won = self.opponent.board.is_finished
            print('You {}!'.format({True: 'won', False: 'lost'}[won]))
        print('Thanks for playing Battleship!')


class Player(object):
    def __init__(self, name, ship_sizes, is_computer=True):
        self.name = name
        self.board = BoardSet(ship_sizes, autofill=is_computer)
        self.turns_remaining = NUM_TURNS

    def use_turn(self):
        self.turns_remaining -= 1

    @property
    def out_of_turns(self):
        return self.turns_remaining <= 0

    def do_board_setup(self):
        print('Ok, {}, time to set up your ships'.format(self.name))
        input('Press Enter to begin')
        for ship in self.board.ship_sizes:
            self.board.player_build_ship(ship)
        clear_screen()
        print('Great, all set!')
        input('Press Enter to continue')


class BoardSet(object):
    def __init__(self, ship_sizes, autofill=True):
        self.size = GRID_SIZE
        self.ship_board = self.generate_board()
        self.ship_sizes = ship_sizes
        if autofill:
            for ship in self.ship_sizes:
                self.autofill_ship(ship)

    def generate_board(self):
        return [["0"] * self.size for _ in range(self.size)]

    def print_board(self, hide_ships=False, message=''):
        clear_screen(buff_size=self.size)
        for row in self.ship_board:
            row = self._hide_ships(row) if hide_ships else row
            print(" ".join(row))
        print(message)

    def _hide_ships(self, row):
        return [x.replace('*', '0') for x in row]

    def fire_shot(self, guess_row, guess_col):
        cell = self.get_cell(guess_row, guess_col)
        if cell in ('*', '0'):
            if cell == '*':
                mark, message, result = '!', 'A hit!', 'hit'
            else:
                mark, message, result = 'X', 'You missed!', 'miss'
            self.mark_board(guess_row, guess_col, mark)
        else:
            message, result = "You already guessed that one!", 'retry'
        self.print_board(hide_ships=True, message=message)
        return result

    def mark_board(self, guess_row, guess_col, mark='X'):
        self.ship_board[guess_row][guess_col] = mark
        return self.ship_board

    def get_cell(self, row, col):
        return self.ship_board[row][col]

    @property
    def is_finished(self):
        return not any('*' in row for row in self.ship_board)

    def player_build_ship(self, length):
        self.print_board()
        print('This ship is {} cells long.'.format(length))
        print('Should it be horizontal or vertical?')
        orientation = get_valid_orientation()
        row_max, col_max = self.get_maxes(orientation, length)
        is_inserted = False
        while not is_inserted:
            print('What cell should it start on?')
            start_row = get_valid_coordinate('row', row_max + 1)
            start_col = get_valid_coordinate('col', col_max + 1)
            is_inserted = self.insert_ship(orientation, length,
                                           start_row, start_col)
            if not is_inserted:
                print('That overlaps another ship! Try again!')

    def autofill_ship(self, length):
        orientation = random.choice(['hor', 'vert'])
        row_max, col_max = self.get_maxes(orientation, length)
        is_inserted = False
        while not is_inserted:
            start_row = random.randint(0, row_max)
            start_col = random.randint(0, col_max)
            is_inserted = self.insert_ship(orientation, length,
                                           start_row, start_col)

    def insert_ship(self, orientation, length, start_row, start_col):
        if orientation == 'hor':
            rows = [start_row] * length
            cols = [start_col + x for x in range(length)]
        else:
            rows = [start_row + x for x in range(length)]
            cols = [start_col] * length
        coords = zip(rows, cols)
        if any(self.get_cell(*x) != '0' for x in coords):
            return False
        for coord in coords:
            self.mark_board(*coord, mark='*')
        return True

    def get_maxes(self, orientation, length):
        row_max, col_max = GRID_SIZE - 1, GRID_SIZE - length
        if orientation == 'vert':
            row_max, col_max = col_max, row_max
        return row_max, col_max


def clear_screen(buff_size=0):
    print('\n'.join('.' * (SCREEN_HEIGHT - buff_size)))


def get_valid_orientation():
    orientation = ''
    while orientation not in ('hor', 'vert'):
        orientation = input("'hor' or 'vert':")
    return orientation


def get_valid_coordinate(category, biggest=GRID_SIZE):
    coordinate = 0
    while coordinate not in (list(range(1, biggest + 1))):
        coordinate = input("Enter {} in range 1-{}:".format(category, biggest))
        coordinate = int(coordinate) if coordinate.isdigit() else coordinate
    # players input in a range that starts at 1,
    # the game logic uses a 0-indexed board
    return coordinate - 1


def get_number_of_players():
    num_players = 0
    while num_players not in (1, 2):
        num_players = input("1 or 2?")
        if num_players.isdigit():
            num_players = int(num_players)
    return num_players


def get_names(num_players):
    names = []
    for x in range(num_players):
        name = input("Player {} name?".format(x + 1))
        print("Welcome, {}!".format(name))
        names.append(name)
    return names


# begin game
def start_game():
    print('''Let's play Battleship!
             How many players are there?''')
    num_players = get_number_of_players()
    names = get_names(num_players)
    game = Game(p1_name=names[0],
                p2_name=names[1] if num_players == 2 else None,
                is_2p=(num_players == 2))
    game.play()


start_game()
