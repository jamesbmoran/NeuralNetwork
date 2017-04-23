
from numpy import *
from random import *

# Simple implementation of tic-tac-toe for testing neural network

class tictactoe:
    # Size is the length of one side of the boardStates
    # play_a is a boolean used to set which player to go first
    def __init__(self, size, play_a):
        self.size = size
        # As list so passed by reference
        self.moves = [0]
        # Used to check if any row, col, diag is filled
        self.board = zeros((size, size), dtype = int)
        self.arows = [0 for x in range(size)]
        self.acols = [0 for x in range(size)]
        self.adiag = [0, 0]
        self.brows = [0 for x in range(size)]
        self.bcols = [0 for x in range(size)]
        self.bdiag = [0, 0]
        # Used to keep track of player
        self.a = play_a

    # Make a move on the board
    # 0 is invalid move
    # 1 is valid move
    # 2 is 'a' player win
    # 3 is 'b' player win
    # 4 is a draw

    def move(self, coord):
        x = int(coord/self.size)
        y = int(coord%self.size)


        # Check position isn't taken
        if(self.is_valid(coord)):
            # If 'a' player go
            if self.a:
                # Add peice to the board
                self.board[x][y] = 1
                # Checking win
                if(add_one(self.arows, x) ==  self.size): return 2
                if(add_one(self.acols, y) ==  self.size): return 2
                if (x == y):
                    if(add_one(self.adiag, 0) ==  self.size): return 2
                if (x + y == self.size-1):
                    if(add_one(self.adiag, 1) ==  self.size): return 2

                # Changing player
                self.a = not self.a
            # Else if 'b' player move
            else:

                self.board[x][y] = -1
                # Checking win
                if(add_one(self.brows, x) ==  self.size): return 3
                if(add_one(self.bcols, y) ==  self.size): return 3
                if (x == y):
                    if(add_one(self.bdiag, 0) ==  self.size): return 3
                if (x + y == self.size-1):
                    if(add_one(self.bdiag, 1) ==  self.size): return 3

                # Changing player
                self.a = not self.a


            # Checking the board isn't filled
            if(add_one(self.moves, 0) == self.size**2): return 4

            # Valid move
            return 1
        else:
            # Invalid move
            return 0

    # Returns true if a move is valid
    # To check
    def is_valid(self, coord):
        return self.board[int(coord/self.size)][int(coord%self.size)] == 0



    # Returns a random valid move as a tuple
    def random_move(self):
        return choice([x for x in range(self.size**2) if self.is_valid(x)])

    # Print the board in a readable format
    def print_board(self):
        for x in range(self.size):
            for y in range(self.size):
                print(self.board[x][y], end = "")
            print()

    # Reset the board to orignial state
    # 'play_a' sets which player to go
    def reset_board(self, play_a):
        self.__init__(self.size, play_a)

    # Returns the board as a list
    def board_list(self):
        return self.board.flatten()

# Function for assignment in condition
def add_one(x, i):
    x[i] += 1
    return x[i]



if __name__ == "__main__":
    print("Make a move on the board")
    print("0 is invalid move")
    print("1 is valid move")
    print("2 is 'a' player win")
    print("3 is 'b' player win")
    print("4 is a draw")

    board = tictactoe(3, True)
    move = 0

    while(move < 2):
        board.print_board()
        try:
            # Taking input
            coord = input("Position: ")
            # Adding exit
            if (coord == 'q'): break

            move = board.move(int(coord))

            print(move)

        # Catch wrong inputs
        except (IndexError, ValueError):
            print("Error, please try again")
