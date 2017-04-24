
from numpy import *
from random import choice
from copy import deepcopy
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
                if(add_one(self.brows, x) ==  self.size): return 4
                if(add_one(self.bcols, y) ==  self.size): return 4
                if (x == y):
                    if(add_one(self.bdiag, 0) ==  self.size): return 4
                if (x + y == self.size-1):
                    if(add_one(self.bdiag, 1) ==  self.size): return 4

                # Changing player
                self.a = not self.a


            # Checking the board isn't filled
            if(add_one(self.moves, 0) == self.size**2): return 3

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

    def good_move(self):
        moves = [x for x in range(self.size**2) if self.is_valid(x)]
        boards = [deepcopy(self) for x in range(len(moves))]
        move_scores = []

        for m, b in zip(moves, boards):
            score = b.move(m)
            if score > 1:
                move_scores.append((m, score))
            else:
                if self.a:
                    move_scores.append((m, self.max_move(b)))
                else:
                    move_scores.append((m, self.min_move(b)))

        if self.a:
            minscore = min(move_scores, key=lambda x:x[1])[1]
            return choice(list(filter(lambda x: x[1] == minscore, move_scores)))[0]
        else:
            maxscore = max(move_scores, key=lambda x:x[1])[1]
            return choice(list(filter(lambda x: x[1] == maxscore, move_scores)))[0]

    def max_move(self, next_board):
        # Finding valid moves
        moves = [x for x in range(self.size**2) if next_board.is_valid(x)]
        # Creating boards to apply moves to
        boards = [deepcopy(next_board) for x in range(len(moves))]
        # Recording the scores of the moves
        scores = []
        for m, b in zip(moves, boards):
            score = b.move(m)
            if score > 1:
                scores.append(score)
            else:
                scores.append(self.min_move(b))
        return max(scores)

    def min_move(self, next_board):
        # Finding valid moves
        moves = [x for x in range(self.size**2) if next_board.is_valid(x)]
        # Creating boards to apply moves to
        boards = [deepcopy(next_board) for x in range(len(moves))]
        # Recording the scores of the moves
        scores = []
        for m, b in zip(moves, boards):
            score = b.move(m)
            if score > 1:
                scores.append(score)
            else:
                scores.append(self.max_move(b))
        return min(scores)


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
    print("3 is a draw")
    print("4 is 'b' player win")


    board = tictactoe(3, True)
    move = 0

    while(move < 2):
        board.print_board()
        try:
            if board.a:
                # Taking input
                coord = input("Position: ")
                # Adding exit
                if (coord == 'q'): break
                move = board.move(int(coord))
            else:
                move = board.move(board.good_move())

            print(move)

        # Catch wrong inputs
        except (IndexError, ValueError):
            print("Error, please try again")
