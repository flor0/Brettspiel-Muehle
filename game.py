import gameutil, copy, ai_minimax_alpha_beta
import numpy as np


#
# Define game functions
#

def canmove(ringpos, stellepos):
    if stellepos % 2 == 0:  # Men on the edges
        if spielfeld[ringpos][(stellepos+1) % 8] == 0 or spielfeld[ringpos][(stellepos-1) % 8] == 0:  # Sideways
            return True
    else:  # Men on the center fields
        if spielfeld[ringpos][(stellepos+1) % 8] == 0 or spielfeld[ringpos][(stellepos-1) % 8] == 0:  # Sideways
            return True
        if ringpos == 0:  # Outer ring
            if spielfeld[1][stellepos] == 0:
                return True
        if ringpos == 1:  # Center ring
            if spielfeld[0][stellepos] == 0 or spielfeld[2][stellepos] == 0:
                return True
        if ringpos == 2:  # Inner ring
            if spielfeld[1][stellepos] == 0:
                return True
    return False


def canmoveatall(player):
    for ring in range(len(board)):
        for stelle in range(len(board[ring])):
            if spielfeld[ring][position] == player:
                if canmove(ring, position):
                    return True
    return False


#
# Initialize game variables
#

set_remaining = 18  # Remaining men to place on the board
remaining = {1:9, 2:9}  # Remaining men from each player
player_colors = {1:"White", 2:"Black"}  # Converting integer to string representation of player
board = [[0 for j in range(8)] for i in range(3)]   # Initialise board at zero-state
turn = False # White begins
turn_to_player = {False:1, True:2}
done = False

# Arbitrary color choice
player_human = 1
player_ai = 2

while not done:
    # AI's turn
    if turn:
        if set_remaining > 0:   # Game phase 1, placing
            set_remaining -= 1
            # Call AI
            drivers.place(AI_CHOICE)

        else:   # Game phase 2, moving
            pass

    # Human's turn
    else:
        if set_remaining > 0:   # Game phase 1, placing
            set_remaining -= 1
            drivers.await_changes()
            if board[HUMAN_PLACED[0]][HUMAN_PLACED[1]] == 0:
                board[HUMAN_PLACED[0]][HUMAN_PLACED[1]] = player_human
        else:   # Game phase 2, moving
            pass
    #
    # Check victory conditions
    #

    # Victory by no men left
    if remaining[1] < 3:    # If Black wins
        print("Black won!")
        done = True
    elif remaining[2] < 3:  # If White wins
        print("White won!")
        done = True

    # Victory by unable to move
    if not canmoveatall(1):  # If White can't move, Black wins
        print("Black won!")
        done = True
    if not canmoveatall(2):  # If Black can't move, White wins
        print("White won!")
        done = True




