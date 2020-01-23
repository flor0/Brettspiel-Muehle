if __name__ == "__main__":
    import gameutil, copy, random, neural_ai, ai_minimax_alpha_beta, drivers, time
    #
    # Define game functions
    #
    def generate_board_muhlen(board):
        muhlen = [[0 for k in range(8)] for f in range(3)]
        for i in range(3):
            for j in range(8):
                if checkmuhle(i, j, board, board[i][j]):
                    muhlen[i][j] = 1
        return muhlen


    def possiblemoves(ringpos, stellepos, spielfeld):
        possiblemoves = []
        if stellepos % 2 == 0:  # Men on the edges
            if spielfeld[ringpos][(stellepos + 1) % 8] == 0:  # Sideways
                possiblemoves.append((ringpos, (stellepos + 1) % 8))
            if spielfeld[ringpos][(stellepos - 1) % 8] == 0:
                possiblemoves.append((ringpos, (stellepos - 1) % 8))
        else:  # Men on the center fields
            if spielfeld[ringpos][(stellepos + 1) % 8] == 0:
                possiblemoves.append((ringpos, (stellepos + 1) % 8))
            if spielfeld[ringpos][(stellepos - 1) % 8] == 0:  # Sideways
                possiblemoves.append((ringpos, (stellepos - 1) % 8))
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
            # Uh, oh! There is only mills left
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
        for ring in range(3):
            for position in range(8):
                if spielfeld[ring][position] == player:
                    if canmove(ring, position, spielfeld):
                        return True
        return False


    def muehle_blocker(board, enemy):
        evil_scores = []
        empty_positions = []
        for ring in range(3):
            for pos in range(8):
                if board[ring][pos] == 0:
                    evil_score = 0
                    empty_positions.append((ring, pos))
                    # Edge case
                    if pos % 2 == 0:
                        if board[ring][(pos + 1) % 8] == enemy and board[ring][(pos + 2) % 8] == enemy:
                            evil_score += 1
                        if board[ring][(pos - 1) % 8] == enemy and board[ring][(pos - 2) % 8] == enemy:
                            evil_score += 1
                    # Middle case
                    else:
                        if board[(ring + 1) % 3][pos] == enemy and board[(ring + 2) % 3][pos] == enemy:
                            evil_score += 1
                        if board[ring][(pos + 1) % 8] == enemy and board[ring][(pos - 1) % 8] == enemy:
                            evil_score += 1
                    evil_scores.append(evil_score)
        # Return the most evil position
        if len(evil_scores) > 0:
            if not max(evil_scores) > 0:
                return False
            max_evil_index = evil_scores.index(max(evil_scores))
            max_evil_move = empty_positions[max_evil_index]
            return max_evil_move
        # If you cant place anywhere, return False
        else:
            return False

    def generate_move(board, player, hand_remaining_human, hand_remaining_ai, board_remaining_human, board_remaining_ai):
        """
        Returns 3 objects, tuples of shape (A, B) or None. They have the shape TO, FROM, REMOVE
        """

        # If phase 1
        if hand_remaining_ai > 0:

            # Hardcoded Muehle-Blocker
            blocker_move = muehle_blocker(board, 1 if player == 2 else 2)
            if not blocker_move:
                # Generate move using Ai
                try:
                    ai_move = neural_ai.makemove(board, hand_remaining_human, hand_remaining_ai, board_remaining_human, board_remaining_ai)
                    if type(ai_move) == list:
                        to = ai_move[0]
                    else:
                        to = ai_move
                except:
                    to = ai_minimax_alpha_beta.Morris(board, generate_board_muhlen(board), player_ai, hand_remaining[player_ai]+hand_remaining[player_human]).out

                if not board[to[0]][to[1]] == 0:
                    # If its illegal/place already occupied
                    # Generate move using minimax
                    to = ai_minimax_alpha_beta.Morris(board, generate_board_muhlen(board), player_ai, hand_remaining[player_ai]+hand_remaining[player_human]).out
                    if not board[to[0]][to[1]] == 0:
                        # Generate random move
                        empty_positions = []
                        for ring in range(3):
                            for pos in range(8):
                                if board[ring][pos] == 0:
                                    empty_positions.append((ring, pos))
                        to = random.choice(empty_positions)
            else:
                to = blocker_move

            # Finally, return the move
            return to


        # If phase 2
        else:
            # Generate move using Ai
            try:
                ai_move = neural_ai.makemove(board, hand_remaining_human, hand_remaining_ai, board_remaining_human, board_remaining_ai)
                if type(ai_move) == list:
                    to = ai_move[0]
                    from_ = ai_move[1]
            except:
                mymove = ai_minimax_alpha_beta.Morris(board, generate_board_muhlen(board), player_ai,
                                                  hand_remaining[player_ai] + hand_remaining[player_human]).out
                print(mymove)
                to = (mymove[0], mymove[1])
                from_ = (mymove[2], mymove[3])


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


            # If phase 3 / jumping is allowed
            if board_remaining_ai < 4:
                if board[from_[0]][from_[1]] == player and board[to[0]][to[1]] == 0:
                    # If all is legal, return
                    return to, from_

            # If Phase2
            # Check legality of from and legality of to and from -> to:
            elif board[from_[0]][from_[1]] == player and to in possiblemoves(from_[0], from_[1], board):
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

    #hand_remaining = {1: 9, 2: 9}  # Remaining men to place on the board
    hand_remaining = {1: 9, 2: 9}
    #board_remaining = {1: 9, 2: 9}  # Remaining men from each player
    board_remaining = {1: 9, 2: 9}  # Remaining men from each player

    player_colors = {1: "White", 2: "Black"}  # Converting integer to string representation of player
    board = [[0 for j in range(8)] for i in range(3)]   # Initialise board at zero-state
    # random situation
    """
    board[0][0] = 1
    board[0][1] = 1
    board[0][5] = 1
    board[0][7] = 1
    board[1][2] = 1
    board[0][3] = 1
    board[1][0] = 2
    board[1][6] = 2
    board[1][7] = 2
    board[2][7] = 2
    """

    turn = True  # Black begins
    turn_to_player = {False: 1, True: 2}
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
            drivers.update_display(0)
            if hand_remaining[player_ai] > 0:   # Game phase 1, placing
                print(board)
                print("AI placing")
                # Call AI
                #ai_move_to = ai_minimax_alpha_beta.Morris(board, generate_board_muhlen(board), player_ai, hand_remaining[player_ai]+hand_remaining[player_human]).out
                ai_move_to = generate_move(board, player_ai, hand_remaining[player_human], hand_remaining[player_ai], board_remaining[player_human], board_remaining[player_ai])    # generate move
                print("AI move generated")
                print("TO: {}".format(ai_move_to))
                if move_is_legal(board, ai_move_to, player_ai, board_remaining[player_ai], hand_remaining[player_ai]):  # Check is move is legal
                    drivers.move_to(ai_move_to)
                    board[ai_move_to[0]][ai_move_to[1]] = player_ai
                    hand_remaining[player_ai] -= 1
                else:
                    print("Ai to illegal move! {}".format(ai_move_to))

            else:   # Game phase 2, moving
                print("AI moving")
                # Call AI
                ai_move = generate_move(board, player_ai, hand_remaining[player_human], hand_remaining[player_ai], board_remaining[player_human], board_remaining[player_ai])
                print("hahaha {}".format(ai_move))
                ai_move_to = ai_move[0]
                ai_move_from = ai_move[1]
                go_move = [ai_move_to, ai_move_from]
                print("lol {}".format(go_move))
                if not move_is_legal(board, go_move, player_ai, board_remaining[player_ai], hand_remaining[player_ai]):   # Illegal move
                    print("Uh, oh. AI from to made a mistake! {}, {}".format(ai_move_to, ai_move_from))
                else:
                    print("Valid move from : {}, {}".format(ai_move_to, ai_move_from))
                    board[ai_move_to[0]][ai_move_to[1]] = player_ai
                    board[ai_move_from[0]][ai_move_from[1]] = 0
                    drivers.move_from_to([ai_move_to, ai_move_from])

            # Check for mills
            if checkmuhle(ai_move_to[0],ai_move_to[1], board, player_ai):
                print("Mühle by Ai!")
                rem = toremove(board, player_human)
                print("AI removing {}".format(rem))
                drivers.remove(rem)
                board[rem[0]][rem[1]] = 0
                board_remaining[player_human] -= 1

        # Human's turn
        else:
            drivers.update_display(2)
            if hand_remaining[player_human] > 0:   # Game phase 1, placing
                waiting = True
                while waiting:
                    print("DEBUG1...")
                    matrix_board_old = drivers.convert_board(drivers.readline_as_array(drivers.sensor_arduino))
                    print("matrix old {}".format(matrix_board_old))
                    drivers.await_move()
                    matrix_board_new = drivers.convert_board(drivers.readline_as_array(drivers.sensor_arduino))
                    print("matrix new {}".format(matrix_board_new))
                    print("board      {}".format(board))
                    print("player_ai {}".format(player_ai))
                    move_human = drivers.human_move(matrix_board_old, matrix_board_new, board, player_ai)
                    print("Human move {}".format(move_human))
                    print("DEBUG1 END")
                    if move_is_legal(board, move_human, player_human, board_remaining[player_human], hand_remaining[player_human]):
                        board[move_human[0]][move_human[1]] = player_human
                        hand_remaining[player_human] -= 1
                        waiting = False
                        # Check for mills 1
                        if checkmuhle(move_human[0], move_human[1], board, player_human):
                            drivers.update_display(1)
                            waiting = True
                            while waiting:
                                matrix_board_old = drivers.convert_board(
                                    drivers.readline_as_array(drivers.sensor_arduino))
                                drivers.await_move()
                                matrix_board_new = drivers.convert_board(
                                    drivers.readline_as_array(drivers.sensor_arduino))
                                remove_human = drivers.human_move(matrix_board_old, matrix_board_new, board, player_ai)
                                print("Human remove {}".format(remove_human))
                                if remove_human is not None and remove_human:

                                    if board[remove_human[0]][remove_human[1]] == player_ai:
                                        board[remove_human[0]][remove_human[1]] = 0 #whyyyy :((((
                                        board_remaining[player_ai] -= 1
                                        waiting = False
                                else:
                                    print("False remove, silly human!3")
                                    drivers.update_display(5)
                    else:
                        print("Move illegal, silly human!1")
                        drivers.update_display(5)



            else:   # Game phase 2, moving
                waiting = True
                while waiting:
                    print("DEBUG2...")
                    matrix_board_old = drivers.convert_board(drivers.readline_as_array(drivers.sensor_arduino))
                    print("matrix old {}".format(matrix_board_old))
                    drivers.await_move()
                    matrix_board_new = drivers.convert_board(drivers.readline_as_array(drivers.sensor_arduino))
                    print("matrix new {}".format(matrix_board_new))
                    print("board      {}".format(board))
                    print("player_ai {}".format(player_ai))
                    move_human = drivers.human_move(matrix_board_old, matrix_board_new, board, player_ai)
                    print("Human move {}".format(move_human))
                    print("DEBUG2 END")
                    if move_is_legal(board, move_human, player_human, board_remaining[player_human], hand_remaining[player_human]):
                        board[move_human[0][0]][move_human[0][1]] = player_human
                        board[move_human[1][0]][move_human[1][1]] = 0
                        waiting = False
                        # Check for mills 2
                        if checkmuhle(move_human[0][0], move_human[0][1], board, player_human):
                            drivers.update_display(1)
                            waiting = True
                            while waiting:
                                matrix_board_old = drivers.convert_board(
                                    drivers.readline_as_array(drivers.sensor_arduino))
                                drivers.await_move()
                                matrix_board_new = drivers.convert_board(
                                    drivers.readline_as_array(drivers.sensor_arduino))
                                if matrix_board_old and matrix_board_new and board and player_ai:
                                    remove_human = drivers.human_move(matrix_board_old, matrix_board_new, board, player_ai) #best fix ever
                                    print("Human remove {}".format(remove_human))
                                else:
                                    print("FATAL FATAL ERRORRR!!!! NOT GOOD #1")
                                if remove_human is not None and remove_human:
                                    if board[remove_human[0]][remove_human[1]] == player_ai:
                                        board[remove_human[0]][remove_human[1]] = 0 #y u so stupid
                                        board_remaining[player_ai] -= 1
                                        waiting = False
                                    else:
                                        print("False remove, silly human!3")
                                        drivers.update_display(5)

                                else:
                                    print("FATAL FATAL ERRORRR!!!! NOT GOOD #2")
                    else:
                        print("Illegal move, silly human!2")
                        drivers.update_display(5)



        turn = not turn

        #
        # Check victory conditions
        #

        # Victory by no men left
        if board_remaining[player_human] + hand_remaining[player_human] < 3:    # If Black wins
            print(board_remaining)
            print("remaining 1")
            print("Ai won!")
            done = True
            drivers.update_display(3)
            time.sleep(30)
        elif board_remaining[player_ai] + hand_remaining[player_ai] < 3:  # If White wins
            print(board_remaining)
            print("remaining 2")
            print("Human won!")
            done = True
            drivers.update_display(4)
            time.sleep(30)

        # Victory by unable to move s
        if hand_remaining[player_human] < 1 and board_remaining[player_human] > 3:
            if not canmoveatall(player_human, board):  # If White can't move, Black wins
                print(board)
                print("Cantmoveatall1")
                print("Human won!")
                done = True
                drivers.update_display(4)
                time.sleep(30)

        if hand_remaining[player_ai] < 1 and board_remaining[player_ai] > 3:
            if not canmoveatall(player_ai, board):  # If Black can't move, White wins
                print(board)
                print("cantmoveatall2")
                print("AI won!")
                done = True
                drivers.update_display(3)
                time.sleep(30)
