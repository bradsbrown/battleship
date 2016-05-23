# import random for ship coord calcuations
import random

# Settings
# (adjust these values to your liking)
grid_size = 10
ship_min = 2
ship_max = 5
num_ships = 3
num_turns = 10


# create board and lay out method to display it
def generate_board(size):
    board = []
    for x in range(size):
        board.append(["O"] * size)
    return board

# prints board with neat fomatting and a spacer above for visibility
def print_board(board):
    spacer = 12
    for i in range(spacer):
        print "."
    for row in board:
        print " ".join(row)
    return board


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


# mark a non-hit guess with an "X"
def add_guess(guess_coord, board):
    guess_row = guess_coord[0]
    guess_col = guess_coord[1]
    board[guess_row - 1][guess_col - 1] = "X"
    return board


# mark all ship cells on board with an "*"
def show_ships(ship_coords, board):
    for i in range(0, len(ship_coords)):
        # demarcate ship locations and hits, print board
        board[ship_coords[i][0]-1][ship_coords[i][1]-1] = "*"
    return board


# give user 'guesses' chances to guess the correct "ship" cell
def play_game(ship_coords, grid_size, board):
    turn = 1
    guess_coord = []
    while True:
        print "Turn", turn
        print "Row/Column Range: 1 -", grid_size
        guess_row = int(raw_input("Guess Row:"))
        guess_col = int(raw_input("Guess Col:"))
        # check if row and column guesses match the ship location
        guess_coord = [guess_row, guess_col]
        if check_guess(guess_coord, ship_coords) is True:
            print "Congratulations! You sunk a battleship!"
            board = show_ships(ship_coords, board)
            board = add_guess(guess_coord, board)
            print_board(board)
            break
        else:
            row_range = range(0, grid_size)
            if guess_row - 1 not in row_range or guess_col - 1 not in row_range:
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


# begin game
def start_game(grid_size, num_ships, ship_min, ship_max, num_turns):
    board = generate_board(grid_size)
    ship_length = size_ships(num_ships)
    print '''Let's play Battleship!
             How many players are there?'''
    option = ''
    choices = ['1', '2']
    while option not in choices:
        option = raw_input("1 or 2?")
    if option == '1':
        ship_is_horizontal = orient_ships(num_ships)
        ship_coords = []
        for i in range(0, len(ship_is_horizontal)):
            this_ship = get_coords(ship_is_horizontal[i], ship_length[i], grid_size)
            for item in this_ship:
                if item in ship_coords:
                    i = i-1
                else:
                    ship_coords.extend(this_ship)
        print_board(board)
        play_game(ship_coords, grid_size, board)
    else:
        return


start_game(grid_size, num_ships, ship_min, ship_max, num_turns)
