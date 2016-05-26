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
grid_size = 10
ship_min = 2
ship_max = 5
num_ships = 1
num_turns = 10

# pull console height for use in screen clearing
height, width = os.popen('stty size', 'r').read().split()
screen_height = int(height)


class Game(object):
    """monitors game state"""
    def __init__(self, on=True):
        self.on = on

g = Game()


# create board and lay out method to display it
def generate_board(size):
    board = []
    for x in range(size):
        board.append(["O"] * size)
    return board


# prints board with neat fomatting and a spacer above for visibility
def print_board(board):
    spacer = screen_height
    for i in range(spacer):
        print "."
    for row in board:
        print " ".join(row)
    return board


# clears screen
def clear_screen():
    for i in range(0, screen_height):
        print "."


# return orientation for ship
def orient_ships(num_ships):
    ship_is_horizontal = []
    while len(ship_is_horizontal) < num_ships:
        orientation = random.randint(0, 1)
        if orientation == 1:
            ship_is_horizontal.append(False)
        else:
            ship_is_horizontal.append(True)
    return ship_is_horizontal


# determine ship lengths
def size_ships(num_ships):
    ship_length = []
    for i in range(0, num_ships):
        ship_length.append(random.randint(ship_min, ship_max))
    return ship_length


# choose starting point for ship, determine all cells for ship
def get_coords(ship_is_horizontal, ship_length, size):
    single_ship = []
    # choose ship starting point
    if ship_is_horizontal is False:
        # determine row
        ship_row = 1 + random.randint(1, size - 1 -
                                      (ship_length - 1))
        # determine column
        ship_col = 1 + random.randint(0, size - 1)
    # set coords for horizontal ship
    else:
        # determine row
        ship_row = 1 + random.randint(1, size - 1)
        # determine column
        ship_col = 1 + random.randint(0, size - 1 -
                                      (ship_length - 1))
    # determine all coordinate points for ship location
    if ship_is_horizontal is True:
        for j in range(0, ship_length):
            single_ship.append([ship_row, ship_col + j])
    else:
        for j in range(0, ship_length):
            single_ship.append([ship_row + j, ship_col])
    return single_ship


# checks a guess against the set of ship cells to verify a hit
def check_guess(guess_cord, ship_coords):
    if str(guess_cord) in str(ship_coords):
        return True
    else:
        return False


# mark a specific cell, default to marking non-hit guess with "X"
def add_guess(guess_coord, board, guess='X'):
    guess_row = guess_coord[0]
    guess_col = guess_coord[1]
    board[guess_row - 1][guess_col - 1] = guess
    return board


# mark all ship cells on board with an "*"
def show_ships(ship_coords, board):
    for i in range(0, len(ship_coords)):
        # demarcate ship locations and hits, print board
        board[ship_coords[i][0]-1][ship_coords[i][1]-1] = "*"
    return board


# returns input for either a coord guess or orientation, verifies input
def get_valid_input(cat, biggest=grid_size):
    if cat == 'row' or cat == 'col':
        while True:
            try:
                number = raw_input("Guess %s:" % cat)
                number = int(number)
            except ValueError:
                pass
            if number in range(1, biggest):
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


# give user 'guesses' chances to guess the correct "ship" cell
def play_1p_game(ship_coords, board):
    turn = 1
    guess_coord = []
    while True:
        print "Turn", turn
        print "Row/Column Range: 1 -", grid_size
        guess_row = get_valid_input('row')
        guess_col = get_valid_input('col')
        # check if row and column guesses match the ship location
        guess_coord = [guess_row, guess_col]
        if check_guess(guess_coord, ship_coords) is True:
            board = show_ships(ship_coords, board)
            board = add_guess(guess_coord, board)
            print_board(board)
            print "Congratulations! You sunk a battleship!"
            break
        else:
            row_range = range(0, grid_size)
            if guess_row - 1 not in row_range or\
                    guess_col - 1 not in row_range:
                print "Oops, that's not even in the ocean."
            elif(board[guess_row - 1][guess_col - 1] == "X"):
                print "You guessed that one already."
            else:
                print "You missed my battleship!"
                board = add_guess(guess_coord, board)
                turn += 1
            if turn == num_turns + 1:
                print "Game Over"
                print_board(board)
                break
            else:
                print_board(board)


# creates board, determines ship coords, starts game
def setup_p1():
    board = generate_board(grid_size)
    ship_length = size_ships(num_ships)
    ship_is_horizontal = orient_ships(num_ships)
    ship_coords = []
    for i in range(0, len(ship_is_horizontal)):
        this_ship = get_coords(ship_is_horizontal[i], ship_length[i],
                               grid_size)
        for item in this_ship:
            if item in ship_coords:
                i = i-1
            else:
                ship_coords.extend(this_ship)
    print_board(board)
    play_1p_game(ship_coords, board)


# checks a given set of coordinates against a board for a hit
def check_2p(guess_row, guess_col, board):
    if board[guess_row - 1][guess_col - 1] == '*':
        return True
    else:
        return False


# inputs a player guess, marks for hit or miss
def guess_2p(player, board, guess_board):
    clear_screen()
    print "Ok %s, your guess." % player
    guess_row = get_valid_input('row')
    guess_col = get_valid_input('col')
    if check_2p(guess_row, guess_col, board):
        board = add_guess((guess_row, guess_col), board, '!')
        guess_board = add_guess((guess_row, guess_col), guess_board, '!')
        print_board(guess_board)
        print "A hit!"
        g.on = False
        for row in board:
            if g.on:
                break
            else:
                for entry in row:
                    if g.on:
                        break
                    else:
                        if entry == '*':
                            g.on = True
        if g.on is False:
            print "%s wins!" % player
        else:
            raw_input("Press Return To Continue...")
    else:
        guess_board = add_guess((guess_row, guess_col), guess_board)
        print_board(guess_board)
        print "A miss!"
        raw_input("Press Return To Continue")


# alternates player guesses until one player hits all opponent ship cells
def play_2p_game(players, ship_boards):
    p1 = players[0]
    p2 = players[1]
    p1_board = ship_boards[0]
    p2_board = ship_boards[1]
    p1_guesses = generate_board(grid_size)
    p2_guesses = generate_board(grid_size)
    for i in range(0, screen_height):
        print "."
    while True:
        # Player 1 turn
        if g.on:
            guess_2p(p1, p2_board, p1_guesses)
        else:
            break
        if g.on:
            # Player 2 turn
            guess_2p(p2, p1_board, p2_guesses)
        else:
            break


# input player names and select ship locations
def setup_p2():
    players = ["Player 1", "Player 2"]
    ship_length = size_ships(num_ships)
    ship_boards = []
    for i in range(0, len(players)):
        board = generate_board(grid_size)
        ship_boards.append(board)
        player_board = ship_boards[i]
        print_board(player_board)
        players[i] = raw_input("Hello, %s, what is your name?" % players[i])
        name = players[i]
        print "Ok, %s, let's set up your ships." % name
        for ship in ship_length:
            print "This ship is %s blocks long." % ship
            print "Should it be horizontal or vertical?"
            orientation = get_valid_input('ori')
            if orientation == 'hor':
                ship_is_horizontal = True
            else:
                ship_is_horizontal = False
            print "What row do you want it to start on?"
            if ship_is_horizontal:
                ship_row = get_valid_input('row', grid_size - (ship - 1))
            else:
                ship_row = get_valid_input('row')
            print "What column?"
            if ship_is_horizontal:
                ship_col = get_valid_input('col')
            else:
                ship_col = get_valid_input('col', grid_size - (ship - 1))
            coords = []
            for y in range(0, ship):
                if ship_is_horizontal:
                    coords.append((ship_row, ship_col+y))
                else:
                    coords.append((ship_row+y, ship_col))
            for coord in coords:
                player_board = add_guess(coord, player_board, '*')
            print "Here is your board!"
            print_board(player_board)
        raw_input("Press Return to continue...")
    play_2p_game(players, ship_boards)
    return


# begin game
def start_game():
    print '''Let's play Battleship!
             How many players are there?'''
    option = ''
    choices = ['1', '2']
    while option not in choices:
        option = raw_input("1 or 2?")
    if option == '1':
        setup_p1()
    else:
        setup_p2()


start_game()
