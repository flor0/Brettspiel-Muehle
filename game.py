import gameutil, copy, ai_minimax_alpha_beta, random
import numpy as np


#
# Define game functions
#

def possiblemoves(ringpos, stellepos, spielfeld):
    possiblemoves = []
    if stellepos % 2 == 0:  # Men on the edges
        if spielfeld[ringpos][(stellepos + 1) % 8] == 0:  # Sideways
            possiblemoves.append((ringpos, (stellepos + 1) % 8))
        if spielfeld[ringpos][(stellepos - 1) % 8] == 0:
            possiblemoves.append((ringpos, (stellepos - 1) % 8))
    else:  # Men on the center fields
        if spielfeld[ringpos][(stellepos + 1) % 8] == 0:
            possiblemoves.append((ringpos, stellepos + 1 % 8))
        if spielfeld[ringpos][(stellepos - 1) % 8] == 0:  # Sideways
            possiblemoves.append((ringpos, stellepos - 1 % 8))
        if ringpos == 0:  # Outer ring
            if spielfeld[1][stellepos] == 0:
                possiblemoves.append((1, stellepos))
        if ringpos == 1:  # Center ring
            if spielfeld[0][stellepos] == 0:
                possiblemoves.append((0, stellepos))
            if spielfeld[2][stellepos] == 0:
                possiblemoves.append((2, stellepos))
        if ringpos == 2:  # Inner ring
            if spielfeld[1][stellepos] == 0:
                possiblemoves.append((1, stellepos))
    if len(possiblemoves) == 0:
        return False
    return possiblemoves


def checkmuhle(ringPos, stellePos, spielfeld, mancolor):
    if stellePos % 2 == 0:  # Men on the edge
        if spielfeld[ringPos][(stellePos + 1) % 8] == mancolor and spielfeld[ringPos][
            (stellePos + 2) % 8] == mancolor:
            return True
        if spielfeld[ringPos][(stellePos - 1) % 8] == mancolor and spielfeld[ringPos][
            (stellePos - 2) % 8] == mancolor:
            return True
    else:  # Men in the centre lines
        if spielfeld[(ringPos + 1) % 3][stellePos] == mancolor and spielfeld[(ringPos + 2) % 3][
            stellePos] == mancolor:
            return True
        if spielfeld[ringPos][(stellePos + 1) % 8] == mancolor and spielfeld[ringPos][
            (stellePos - 1) % 8] == mancolor:
            return True
    return False


def update_board_muhlen(self, board, board_muhlen_old):
    board_muhlen_new = copy.deepcopy(board_muhlen_old)
    for ring in range(3):
        for stelle in range(8):
            if self.checkmuhle(ring, stelle, board, board[ring][stelle]):
                board_muhlen_new[ring][stelle] = 1
            else:
                board_muhlen_new[ring][stelle] = 0
    return board_muhlen_new


def toremove(board, enemy):
    enemies = []
    scores = []
    for ring in range(3):
        for stelle in range(8):
            # For each enemy man who is not in a mill
            if board[ring][stelle] == enemy and not self.checkmuhle(ring, stelle, board, enemy):
                # Generate "evil" score for the enemy man
                evil_score = 0

                # If two men are in one line and can make a mill next move
                if stelle % 2 == 0:  # Edge case
                    if board[ring][((stelle + 1) % 8)] == enemy:
                        evil_score += 1
                    if board[ring][(stelle - 1) % 8] == enemy:
                        evil_score += 1
                    # Really bad situation, man has to be removed because two mills are possible
                    if board[ring][(stelle - 1) % 8] == enemy and board[ring][((stelle + 1) % 8)] == enemy:
                        evil_score += 100

                elif stelle % 2 != 0:  # Center case
                    if board[(ring + 1) % 3][stelle] == enemy:
                        evil_score += 1
                    if board[(ring + 2) % 3][stelle] == enemy:
                        evil_score += 1
                    if board[ring][(stelle + 1) % 8] == enemy:
                        evil_score += 1
                    if board[ring][(stelle - 1) % 8] == enemy:
                        evil_score += 1
                    # Really bad situation, same as above when two mills are possible
                    if board[(ring + 1) % 3][stelle] == enemy and (
                            board[ring][(stelle + 1) % 8] == enemy or board[ring][(stelle - 1) % 8] == enemy):
                        evil_score += 100
                    if board[(ring + 2) % 3][stelle] == enemy and (
                            board[ring][(stelle + 1) % 8] == enemy or board[ring][(stelle - 1) % 8] == enemy):
                        evil_score += 100

                scores.append(evil_score)
                enemies.append((ring, stelle))
    if len(scores) == 0:
        # Uh oh, there is only mills left
        # We can just remove men out of mills now
        for ring in range(3):
            for stelle in range(8):
                # For each enemy man
                if board[ring][stelle] == enemy:
                    scores.append(1)
                    enemies.append((ring, stelle))
                    max_score = scores[0]
    else:
        max_score = max(scores)

    return enemies[scores.index(max_score)]


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

hand_remaining = {1:9, 2:9}  # Remaining men to place on the board
board_remaining = {1:9, 2:9}  # Remaining men from each player
player_colors = {1:"White", 2:"Black"}  # Converting integer to string representation of player
board = [[0 for j in range(8)] for i in range(3)]   # Initialise board at zero-state
turn = False # White begins
turn_to_player = {False:1, True:2}
done = False
to = (0, 0)
_from = (0, 0)
remove = (0, 0)

# Arbitrary color choice
player_human = 1
player_ai = 2

while not done:
    # AI's turn
    if turn:
        if hand_remaining[player_ai] > 0:   # Game phase 1, placing
            hand_remaining[player_ai] -= 1
            # Call AI
            ai.move = ai.make_move()    # generate move
            if board[ai.move[0]][ai.move[1]] == 0:  # If the man can be placed on the empty spot
                to = ai.move
                drivers.place(ai.move)
            else:   # If the move is invalid make a random valid move
                possible_moves = []
                for ring in range(3):
                    for pos in range(8):
                        if board[ring][pos] == 0:
                            possible_moves.append((ring, pos))  # Add possible move to list
                to = random.choice(possible_moves)
                drivers.place(to)    # Select random move and execute with drivers

        else:   # Game phase 2, moving
            # Call AI
            ai_move_to, ai_move_from = ai.make_move()
            if (ai_move_to not in possiblemoves(ai_move_from[0], ai_move_from[1], board)) and not (board_remaining[player_ai] == 3):    # Illegal move
                print("Uh, oh. AI made a mistake!")
            else:
                board[ai_move_to[0]][ai_move_to[1]] = player_ai
                board[ai_move_from[0]][ai_move_from[1]] = 0


        # Check for mills
        if checkmuhle(ai_move_to[0],ai_move_to[1], board, player_ai):
            drivers.remove(toremove(board, player_human))
            board_remaining[player_human] -= 1

    # Human's turn
    else:
        if hand_remaining[player_human] > 0:   # Game phase 1, placing
            hand_remaining[player_human] -= 1
            drivers.await_changes()
            move_human = drivers.get_move()
            if board[move_human[0]][move_human[1]] == 0:
                board[move_human[0]][move_human[1]] = player_human
        else:   # Game phase 2, moving
            drivers.await_changes()
            move_human = drivers.get_move()
            if len(move_human) != 2:    # Has to include a position to and from
                print("Invalid move, silly human!")
            else:
                # Check move for legality
                if board[move_human[0][0]][move_human[0][1]] != 0 or board[move_human[1][0]][move_human[1][1]] != player_human:  # Never legal
                    print("Illegal move, human!")
                elif (not board[move_human[0][0]][move_human[0][1]] in possiblemoves(move_human[1][0], move_human[1][1], board)) and board_remaining[player_human] > 3: # If player cant jump
                    print("Illegal move, human!")
                else:   # Legal move
                    board[move_human[0][0]][move_human[0][1]] = player_human
                    board[move_human[1][0]][move_human[1][1]] = 0

        # Check for mills
        if checkmuhle(move_human[0][0], move_human[0][1], board, player_human):
            drivers.remove(toremove(board, player_ai))
            board_remaining[player_ai] -= 1
    #
    # Check victory conditions
    #

    # Victory by no men left
    if board_remaining[1] < 3:    # If Black wins
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




