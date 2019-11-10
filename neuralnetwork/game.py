import gameutil, copy, random, neural_ai

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


def toremove(board, enemy):
    enemies = []
    scores = []
    for ring in range(3):
        for stelle in range(8):
            # For each enemy man who is not in a mill
            if board[ring][stelle] == enemy and not checkmuhle(ring, stelle, board, enemy):
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


def canmove(ringpos, stellepos, spielfeld):
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


def canmoveatall(player, spielfeld):
    for ring in range(len(board)):
        for position in range(len(board[ring])):
            if spielfeld[ring][position] == player:
                if canmove(ring, position, spielfeld):
                    return True
    return False

def generate_move(board, player, hand_remaining_human, hand_remaining_ai, board_remaining_human, board_remaining_ai):
    """
    Returns 3 objects, tuples of shape (a, b) or None. They have the shape TO, FROM, REMOVE
    """

    # If phase 1
    if hand_remaining_ai > 0:

        # Generate move using Ai
        ai_move = neural_ai.makemove(board, hand_remaining_human, hand_remaining_ai, board_remaining_human, board_remaining_ai)
        if type(ai_move) == list:
            to = ai_move[0]
        else:
            to = ai_move

        # Check if move is legal, else generate a random legal move
        if not board[to[0]][to[1]] == 0:
            # If its illegal/place already occupied
            # Generate random move
            empty_positions = []
            for ring in range(3):
                for pos in range(8):
                    if board[ring][pos] == 0:
                        empty_positions.append((ring, pos))
            to = random.choice(empty_positions)

        # Finally, return the move
        return to


    # If phase 2
    else:
        # Generate move using Ai
        ai_move = neural_ai.makemove(board, hand_remaining_human, hand_remaining_ai, board_remaining_human, board_remaining_ai)
        if type(ai_move) == list:
            to = ai_move[0]
            from_ = ai_move[1]

        else:
            # Ai has already messed up, output has invalid format

            # Generate random move
            rand_tos = []
            rand_froms = []
            for ring in range(3):
                for pos in range(8):
                    if board[ring][pos] == player:
                        rand_froms.append((ring, pos))
                    if board[ring][pos] == 0:
                        rand_tos.append((ring, pos))
            rand_from = random.choice(rand_froms)
            # If Ai has only 3 men left, he can jump to any position
            rand_tos = possiblemoves(rand_from[0], rand_from[1], board) if board_remaining_ai > 3 else rand_tos
            rand_to = random.choice(rand_tos)

            to = rand_to
            from_ = rand_from

            # Return the random move
            return to, from_

        # Check for legality

        # If Phase2
        # Check legality of from and legality of to and from -> to:
        if board[from_[0]][from_[1]] == player and to in possiblemoves(from_[0], from_[1], board):
            # If all is legal, return
            return to, from_

        # If phase 3 / jumping is allowed
        elif board_remaining_ai < 4:
            if board[from_[0]][from_[1]] == player and board[to[0]][to[1]] == 0:
                # If all is legal, return
                return to, from_

        else:
            # If illegal, random move
            # Generate random move
            rand_tos = []
            rand_froms = []
            for ring in range(3):
                for pos in range(8):
                    if board[ring][pos] == player:
                        rand_froms.append((ring, pos))
                    if board[ring][pos] == 0:
                        rand_tos.append((ring, pos))
            rand_from = random.choice(rand_froms)
            # If Ai has only 3 men left, he can jump to any position
            rand_tos = possiblemoves(rand_from[0], rand_from[1], board) if board_remaining_ai > 3 else rand_tos
            rand_to = random.choice(rand_tos)

            to = rand_to
            from_ = rand_from

            # Return the random move
            return to, from_


def move_is_legal(board, move, player, remaining_ai_board, remaining_ai_hand):
    """
    Input format: Phase1: (A, B) or Phase2: [(A, B), (C, D)]
    """
    # Separate the two game phases

    # Move is in TO format
    if type(move) == tuple and len(move) == 2:
        to = move
        """
        When placing:
        1: You need pieces in your hand to place
        2: The field on the board has to be empty
        """
        if remaining_ai_hand < 1 or board[to[0]][to[1]] != 0:
            return False
        return True

    # Move is in [TO, FROM] format
    if type(move) == list and len(move) == 2 and len(move[0]) == 2 and len(move[1]) == 2:
        to = move[0]
        from_ = move[1]
        """
        Rules apply:
        1: You must not have pieces in your hand to move a piece
        2: TO has to be empty
        3: FROM has to be one of your pieces
        4: If you have more than 3 pieces on the board, TO has to be a neighbour of FROM else it can be any free field 
        """
        if remaining_ai_hand > 0 or board[to[0]][to[1]] != 0 or board[from_[0]][from_[1]] != player:
            return False
        # If you can't jump
        if remaining_ai_board > 3:
            # FROM and TO have to be neighbours or in other words: TO is in possiblemoves of FROM in board
            if not to in possiblemoves(from_[0], from_[1], board):
                return False
        return True

    # Move has invalid format
    print("Move has invalid format")
    return False


#
# Initialize game variables
#

hand_remaining = {1:9, 2:9}  # Remaining men to place on the board
board_remaining = {1:9, 2:9}  # Remaining men from each player
player_colors = {1:"White", 2:"Black"}  # Converting integer to string representation of player
board = [[0 for j in range(8)] for i in range(3)]   # Initialise board at zero-state
turn = True # Black begins
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
            ai_move = generate_move(board, player_ai, hand_remaining[player_human], hand_remaining[player_ai], board_remaining[player_human], board_remaining[player_ai])    # generate move
            if move_is_legal(board, ai_move, player_ai, board_remaining[player_ai], hand_remaining[player_ai]): # Check is move is legal
                #drivers.place(to)    # Select random move and execute with drivers

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




