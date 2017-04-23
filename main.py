
from tictactoe import *
from network import *
from random import *
from numpy import *


# Initalise board and neural network
learning_rate = 0.1
size = 3
board = tictactoe(size, True)

# To print statistics
wins = 0
draws = 0
losses = 0
games = 1

# Loading or making a new net
start = False
while not start:
    net_type = input("'N' for new net, 'L' to load a saved net: ")
    if (net_type == 'N'):
        net = neuralnetwork([9, 1000, 100, 50, 9], sigmoid, sigmoidPrime)
        start = True
    elif (net_type == 'L'):
        load_file = input("Enter file with saved net: ")
        net = load_net(load_file)
        start = True

iterations = int(input("Number of iterations: "))
net_file = input("Enter file name: ")

for i in range(iterations):
    # Initalise list for training
    # List of outputs
    moves_made = []
    # List of List of activations
    acts_list = []
    # List of list of z values
    zs_list = []
    # Result
    result = 0

    while(result < 2):
        if board.a:
            # Get board in correct format
            curr_board = board.board_list()
            curr_board.shape = (size*size, 1)

            # Find what is output by the neural net
            # Recording intermediate values
            output = net.run_values(curr_board)
            output_move = output[0][-1]
            acts_list.append(output[0])
            zs_list.append(output[1])

            # Find the move chosen by the net, make it into an array, add it to array for training
            net_move =  sorted(list(filter(lambda x: board.is_valid(x[0]), enumerate(output_move))), key = lambda x:x[1], reverse = True)[0][0]
            move = zeros((size*size, 1))
            move[net_move] = 1
            moves_made.append(move)

            # Make the move
            result = board.move(net_move)
        else:
            result = board.move(board.random_move())

    if result == 2:
        wins += 1
        net.batch(acts_list, zs_list, moves_made, learning_rate)
    elif result == 3:
        losses += 1
        net.batch(acts_list, zs_list, moves_made, -learning_rate)
    elif result == 4:
        draws += 1
        net.batch(acts_list, zs_list, moves_made, learning_rate)


    print("Games:%d, Wins: %d, Losses %d, Draws: %d, Win Rate: %f" %(games, wins, losses, draws, (float(wins+draws)/games)), end = "\r")
    board.reset_board(choice([True, False]))
    games +=1

print()
net.save_net(net_file)
