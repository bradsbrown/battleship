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
board = []
for x in range(grid_size):
    board.append(["O"] * grid_size)


def print_board(board):
    for row in board:
        print " ".join(row)

# begin game
print "Let's play Battleship!"
print_board(board)

# determine ship orientation
ship_is_horizontal = []
align_ship = []
while len(align_ship) < num_ships:
    align_ship.append(random.randint(0, 1))
for i in range(0, num_ships):
    if align_ship[i] == 1:
        ship_is_horizontal.append(False)
    else:
        ship_is_horizontal.append(True)

# determine ship lengths
ship_length = []
for i in range(0, num_ships):
    ship_length.append(random.randint(ship_min, ship_max))

# choose starting point for ship, determine all cells for ship
ship_coords = []
for i in range(0, num_ships):
    # set coords for vertical ship
    if ship_is_horizontal[i] is False:
        # determine row
        ship_row = 1 + random.randint(1, len(board[0]) - 1 -
                                      (ship_length[i] - 1))
        # determine column
        ship_col = 1 + random.randint(0, len(board[0]) - 1)
    # set coords for horizontal ship
    else:
        # determine row
        ship_row = 1 + random.randint(1, len(board[0]) - 1)
        # determine column
        ship_col = 1 + random.randint(0, len(board[0]) - 1 -
                                      (ship_length[i] - 1))
    # determine all coordinate points for ship location
    single_ship = []
    if ship_is_horizontal[i] is True:
        for j in range(0, ship_length[i]):
            single_ship.append([ship_row, ship_col + j])
    else:
        for j in range(0, ship_length[i]):
            single_ship.append([ship_row + j, ship_col])
    match_found = False
    for j in range(0, len(single_ship)):
        if single_ship[j] in ship_coords:
            match_found = True
    if match_found is False:
        ship_coords.extend(single_ship)
    else:
        i = i - 1


# give user 'guesses' chances to guess the correct "ship" cell
turn = 1
guess_coord = []
while True:
    print "Turn", turn
    print "Row/Column Range: 1 -", grid_size
    guess_row = int(raw_input("Guess Row:"))
    guess_col = int(raw_input("Guess Col:"))
    # check if row and column guesses match the ship location
    guess_coord = [guess_row, guess_col]
    if str(guess_coord) in str(ship_coords):
        print "Congratulations! You sunk my battleship!"
        for i in range(0, len(ship_coords)):
            # demarcate ship locations and hits, print board
            board[ship_coords[i][0]-1][ship_coords[i][1]-1] = "*"
        board[guess_row - 1][guess_col - 1] = "X"
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
            board[guess_row - 1][guess_col - 1] = "X"
            turn = turn + 1
        if turn == num_turns + 1:
            print "Game Over"
            print_board(board)
            break
        else:
            print_board(board)
