# import random for ship coord calcuations
import random
# import os for screen size measurement
import os


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
    """monitors game state"""
    player_qty = ['1', '2']
    players = ["Player 1", "Player 2"]
    active_player = 1

    def __init__(self, on=True, num_players=''):
        self.on = on
        self.num_players = num_players


class BoardSet(object):
    def __init__(self):
        self.size = GRID_SIZE
        self.ship_board = self.generate_board()
        self.guess_board = self.generate_board()

    def generate_board(self):
        board = []
        for x in range(self.size):
            board.append(["O"] * self.size)
        return board

    def print_board(self, board):
        for i in range(SCREEN_HEIGHT):
            print "."
        for row in board:
            print " ".join(row)

    def add_guess(self, guess_coord, board, guess='X'):
        guess_row = guess_coord[0]
        guess_col = guess_coord[1]
        board[guess_row - 1][guess_col - 1] = guess
        return board

    def check_hit(self, guess_row, guess_col, board):
        if board[guess_row - 1][guess_col - 1] == '*':
            return True
        else:
            return False

    '''These functions are used specifically for 1p play to generate ships'''
    # return orientation for ship
    def orient_ships(self):
        ship_is_horizontal = []
        while len(ship_is_horizontal) < NUM_SHIPS:
            orientation = random.randint(0, 1)
            if orientation == 1:
                ship_is_horizontal.append(False)
            else:
                ship_is_horizontal.append(True)
        return ship_is_horizontal

    # determine ship lengths
    def size_ships(self):
        SHIP_LENGTH = []
        for i in range(0, NUM_SHIPS):
            SHIP_LENGTH.append(random.randint(SHIP_MIN, SHIP_MAX))
        return SHIP_LENGTH

    # choose starting point for ship, determine all cells for ship
    def get_coords(self, ship_is_horizontal, SHIP_LENGTH, size=GRID_SIZE):
        single_ship = []
        # choose ship starting point
        if ship_is_horizontal is False:
            # determine row
            ship_row = 1 + random.randint(1, size - 1 -
                                          (SHIP_LENGTH - 1))
            # determine column
            ship_col = 1 + random.randint(0, size - 1)
        # set coords for horizontal ship
        else:
            # determine row
            ship_row = 1 + random.randint(1, size - 1)
            # determine column
            ship_col = 1 + random.randint(0, size - 1 -
                                          (SHIP_LENGTH - 1))
        # determine all coordinate points for ship location
        if ship_is_horizontal is True:
            for j in range(0, SHIP_LENGTH):
                single_ship.append([ship_row, ship_col + j])
        else:
            for j in range(0, SHIP_LENGTH):
                single_ship.append([ship_row + j, ship_col])
        return single_ship

G = Game()
P1 = BoardSet()
P2 = BoardSet()
SHIP_LENGTH = P1.size_ships()
ship_boards = [P1.ship_board, P2.ship_board]
p_boardsets = [P1, P2]


'''Below are some universal functions that work in both 1p and 2p play'''


# clears screen
def clear_screen():
    for i in range(0, SCREEN_HEIGHT):
        print "."


# returns input for either a coord guess or orientation, verifies input
def get_valid_input(cat, biggest=GRID_SIZE):
    if cat == 'row' or cat == 'col':
        while True:
            try:
                number = raw_input("Guess %s:" % cat)
                number = int(number)
            except ValueError:
                pass
            if number in range(1, biggest + 1):
                break
            print "Please enter a number in the range 1 - %s" % biggest
        return number
    elif cat == 'ori':
        while True:
            ori = raw_input("'hor' or 'vert':")
            if ori == 'hor' or ori == 'vert':
                return ori
            else:
                print "Please enter 'hor' or 'vert'"


def check_for_unhit_ships(board):
    '''validate that there are still unhit ship cells to try for,
    return True if so, False if not'''
    for row in board:
        if '*' in row:
            return True
    return False


'''2p specific functions'''


# inputs a player guess, marks for hit or miss
def guess_2p(player, board, guess_board, player_num):
    p_BoardSet = p_boardsets[player_num]
    clear_screen()
    print "Ok %s, your guess." % player
    guess_row = get_valid_input('row')
    guess_col = get_valid_input('col')
    if p_BoardSet.check_hit(guess_row, guess_col, board):
        p_BoardSet.add_guess((guess_row, guess_col), board, '!')
        p_BoardSet.add_guess((guess_row, guess_col), guess_board, '!')
        p_BoardSet.print_board(guess_board)
        print "A hit!"
        if not check_for_unhit_ships(board):
            G.on = False
            print "%s wins!" % player
        else:
            raw_input("Press Return To Continue...")
    else:
        p_BoardSet.add_guess((guess_row, guess_col), guess_board)
        p_BoardSet.print_board(guess_board)
        print "A miss!"
        raw_input("Press Return To Continue")


'''Actual game flow for 1p'''


# give user 'guesses' chances to guess the correct "ship" cell
def play_1p_game():
    guesses = NUM_TURNS
    while G.on:
        if not check_for_unhit_ships(P2.ship_board):
            G.on = False
            print "Congratulations %s, you won!" % G.players[0]
            return

        # Get the user's guess
        print "Remaining guesses:", guesses
        print "Row/Column Range: 1 -", GRID_SIZE
        guess_row = get_valid_input('row')
        guess_col = get_valid_input('col')
        guess_coord = [guess_row, guess_col]

        # check if row and column guesses match a ship cell
        if P1.check_hit(guess_row, guess_col, P2.ship_board) is True:
            # if hit, update guess board and opponent ship board with hit
            P1.add_guess(guess_coord, P1.guess_board, '!')
            P2.add_guess(guess_coord, P2.ship_board, '!')
            P1.print_board(P1.guess_board)
            guesses = NUM_TURNS
            print "You got a hit! Your guess count is reset to %s." % guesses
            raw_input("Press Return to continue...")
            P1.print_board(P1.guess_board)

        else:
            # check that the miss wasn't a previous guess
            if(P1.guess_board[guess_row - 1][guess_col - 1] == "X"):
                print "You guessed that one already."
                raw_input("Press Return to continue...")

            else:
                # if not, mark the miss on both boards, and decrement guesses
                print "You missed my battleship!"
                P1.add_guess(guess_coord, P1.guess_board)
                P2.add_guess(guess_coord, P2.ship_board)
                guesses -= 1
                raw_input("Press Return to continue...")

            if guesses == 0:
                # if out of guesses, end game
                P2.print_board(P2.ship_board)
                print "Game Over"
                print "%s was too sneaky for you!" % G.players[1]
                G.on = False

            else:
                P1.print_board(P1.guess_board)


# creates board, determines ship coords, starts game
def setup_P1():
    G.players[1] = "Computer"
    G.players[0] = raw_input("What is your name?")
    SHIP_LENGTH = P2.size_ships()
    ship_is_horizontal = P2.orient_ships()
    ship_coords = []
    for i in range(0, len(ship_is_horizontal)):
        this_ship = P2.get_coords(ship_is_horizontal[i], SHIP_LENGTH[i])
        for item in this_ship:
            if item in ship_coords:
                i = i-1
            else:
                ship_coords.extend(this_ship)
    for coord in ship_coords:
        P2.add_guess(coord, P2.ship_board, '*')
    P1.print_board(P1.guess_board)
    play_1p_game()


'''Actual 2p game flow'''


# alternates player guesses until one player hits all opponent ship cells
def play_2p_game(players, ship_boards):
    P1_name = players[0]
    P2_name = players[1]
    P1_board = P1.ship_board
    P2_board = P2.ship_board
    P1_guesses = P1.guess_board
    P2_guesses = P2.guess_board
    for i in range(0, SCREEN_HEIGHT):
        print "."
    while True:
        # Player 1 turn
        if G.on:
            guess_2p(P1_name, P2_board, P1_guesses, 0)
        else:
            break
        if G.on:
            # Player 2 turn
            guess_2p(P2_name, P1_board, P2_guesses, 1)
        else:
            break


# input player names and select ship locations
def setup_P2():
    for i in range(0, len(G.players)):
        player = p_boardsets[i]
        player_board = player.ship_board
        player.print_board(player_board)
        G.players[i] = raw_input("Hello, %s, what is your name?"
                                 % G.players[i])
        name = G.players[i]
        print "Ok, %s, let's set up your ships." % name
        j = 0
        while j < len(SHIP_LENGTH):
            ship = SHIP_LENGTH[j]
            print "This ship is %s blocks long." % ship
            print "Should it be horizontal or vertical?"
            orientation = get_valid_input('ori')
            if orientation == 'hor':
                ship_is_horizontal = True
            else:
                ship_is_horizontal = False
            print "What row do you want it to start on?"
            if ship_is_horizontal:
                ship_row = get_valid_input('row', GRID_SIZE - (ship - 1))
            else:
                ship_row = get_valid_input('row')
            print "What column?"
            if ship_is_horizontal:
                ship_col = get_valid_input('col')
            else:
                ship_col = get_valid_input('col', GRID_SIZE - (ship - 1))
            coords = []
            for y in range(0, ship):
                if ship_is_horizontal:
                    coords.append((ship_row, ship_col+y))
                else:
                    coords.append((ship_row+y, ship_col))
            overlap = False
            for coord in coords:
                if player_board[coord[0]-1][coord[1]-1] == '*':
                    overlap = True
            if not overlap:
                for coord in coords:
                    player_board = player.add_guess(coord, player_board, '*')
                print "Here is your board!"
                player.print_board(player_board)
                j += 1
            else:
                print "Sorry, that ship overlaps another one. Let's try again."
        raw_input("Press Return to continue...")
    play_2p_game(G.players, ship_boards)
    return


'''Game intro, determines mode'''


# begin game
def start_game():
    print '''Let's play Battleship!
             How many players are there?'''
    while G.num_players not in G.player_qty:
        G.num_players = raw_input("1 or 2?")
    if G.num_players == '1':
        setup_P1()
    else:
        setup_P2()


start_game()
