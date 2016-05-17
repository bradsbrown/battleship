import random
# create board and lay out method to display it
board = []
for x in range(5):
    board.append(["O"] * 5)
def print_board(board):
    for row in board:
        print " ".join(row)

# begin game, assign one random cell to be the "ship"
print "Let's play Battleship!"
print_board(board)

ship_is_horizontal = True

def get_ship_length():
    return random.randint(1,3)

ship_length = get_ship_length()

def random_row(board):
    if ship_is_horizontal == False:
        return random.randint(0, len(board[0]) -1 - ship_length)
    else:
        return random.randint(0, len(board[0]) - 1)

def random_col(board):
    if ship_is_horizontal == True:
        return random.randint(0, len(board[0]) - 1 - ship_length)
    else:
        return random.randint(0, len(board[0]) - 1)

ship_row = random_row(board)
ship_col = random_col(board)

def get_ship_row_range(board):
    ship_row_range = []
    if ship_is_horizontal == False:
        ship_row_range.append(ship_row + 1)
        ship_row_range.append(ship_row + ship_length)
    else:
        ship_row_range.append(ship_row + 1)
        ship_row_range.append(ship_row + 1)
    return ship_row_range

def get_ship_col_range(board):
    ship_col_range = []
    if ship_is_horizontal == True:
        ship_col_range.append(ship_col + 1)
        ship_col_range.append(ship_col + ship_length)
    else:
        ship_col_range.append(ship_col + 1)
        ship_col_range.append(ship_col + 1)
    return ship_col_range

ship_row_set = get_ship_row_range(board)
ship_col_set = get_ship_col_range(board)

# FOR TESTING ONLY, remove these lines before actual play
print ship_row
print ship_col
print "Row: ", ship_row_set[0], " - ", ship_row_set[1]
print "Col: ", ship_col_set[0], " - ", ship_col_set[1]

# give user three chances to guess the correct "ship" cell
turn = 1
while True:
    print "Turn", turn
    guess_row = int(raw_input("Guess Row(1-5):"))
    guess_col = int(raw_input("Guess Col(1-5):"))
    # check if row and column guesses match the ship location
    guess_row_match = False
    guess_col_match = False
    if guess_row == ship_row_set[0] or guess_row == ship_row_set[1]:
        guess_row_match = True
    elif ship_row_set[0] < guess_row < ship_row_set[1]:
        guess_row_match = True
    if guess_col == ship_col_set[0] or guess_col == ship_col_set[1]:
        guess_col_match = True
    elif ship_col_set[0] < guess_col < ship_col_set[1]:
        guess_col_match = True
    if guess_col_match and guess_row_match:
        print "Congratulations! You sunk my battleship!"
        break
    else:
        row_range = range(0,5)
        if guess_row - 1 not in row_range or guess_col - 1 not in row_range:
             print "Oops, that's not even in the ocean."
        elif(board[guess_row - 1][guess_col - 1] == "X"):
            print "You guessed that one already."
        else:
            print "You missed my battleship!"
            board[guess_row - 1][guess_col - 1] = "X"
            turn = turn + 1
        if turn == 4:
            print "Game Over"
            print_board(board)
            break
        else:
            print_board(board)

# Ideas 1 - multiple ships
# Ideas 2 - different sizes
# Ideas 3 - two-player game
# Ideas 4 - rematches, stats
