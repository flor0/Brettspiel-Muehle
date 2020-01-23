import copy, gameutil, time

class Morris:
    def __init__(self, board, board_muhlen, real_player, remaining_set):
        self.board = board
        self.board_muhlen = board_muhlen
        self.player = real_player
        self.opponent = 1 if self.player == 2 else 2
        self.remaining_set = remaining_set
        self.max_depth = 3  # Important, determines the depth of the algorithm
        t = time.time()
        self.out = self.make_score(board, board_muhlen, real_player, -1000000000000000,
                                                             100000000000000)
        print("AI time: %s sec" % str(time.time() - t))
    ###
    # First function being called, only remembers moves to return them
    ###
    def make_score(self, board, board_muhlen, player, alpha, beta):
        maxEval = alpha
        best_move = False
        # If phase 1
        if self.remaining_set > 0:
            for ring in range(3):
                for stelle in range(8):
                    if board[ring][stelle] == 0:
                        move = (ring, stelle)
                        board_continue = copy.deepcopy(board)
                        board_continue[ring][stelle] = self.player

                        score_add = 0
                        if self.checkmuhle(move[0], move[1], board_continue, self.player):
                            score_add += 100

                        evaluation = self.minimax(board_continue, copy.deepcopy(board_muhlen), 1 if player == 2 else 2
                                                  , maxEval, beta, self.remaining_set, self.max_depth)
                        evaluation += score_add

                        if evaluation > maxEval:
                            maxEval = evaluation
                            best_move = move
                            if maxEval >= beta:
                                break
                else:
                    continue
                break
            return best_move[0], best_move[1]
        # If phase 2
        else:
            # Figure out how many pieces on board by ai
            mypieces = 0
            for i in range(3):
                for j in range(8):
                    if board[i][j] == self.player:
                        mypieces += 1

            if mypieces > 3:
                for ring in range(3):
                    for stelle in range(8):
                        if board[ring][stelle] == self.player:
                            possiblemoves = self.possiblemoves(ring, stelle, board)
                            if possiblemoves:
                                for move in possiblemoves:
                                    board_ = copy.deepcopy(board)
                                    muhlen_ = copy.deepcopy(board_muhlen)
                                    board_[ring][stelle] = 0
                                    try:
                                        board_[move[0]][move[1]] = self.player
                                    except:
                                        print("ERROR"+str(move))
                                    score_add = 0
                                    if self.checkmuhle(move[0], move[1], board_, self.player):
                                        score_add += 100
                                    evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, maxEval, beta, self.remaining_set, self.max_depth)
                                    evaluation += score_add

                                    if evaluation > maxEval:
                                        maxEval = evaluation
                                        best_move = move[0], move[1], ring, stelle
                                        if maxEval >= beta:
                                            break
                    else:
                        continue
                    break
                return best_move[0], best_move[1], best_move[2], best_move[3]

            # If jumping
            else:
                for ring in range(3):
                    for stelle in range(8):
                        if board[ring][stelle] == self.player:
                            possiblemoves = []
                            possiblemoves_bool = False
                            for i in range(3):
                                for j in range(8):
                                    if board[i][j] == 0:
                                        possiblemoves_bool = True
                                        possiblemoves.append((i, j))
                            if possiblemoves_bool:
                                for move in possiblemoves:
                                    board_ = copy.deepcopy(board)
                                    muhlen_ = copy.deepcopy(board_muhlen)
                                    board_[ring][stelle] = 0
                                    try:
                                        board_[move[0]][move[1]] = self.player
                                    except:
                                        print("ERROR" + str(move))
                                    score_add = 0
                                    if self.checkmuhle(move[0], move[1], board_, self.player):
                                        score_add += 100
                                    evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, maxEval, beta,
                                                              self.remaining_set, self.max_depth)
                                    evaluation += score_add

                                    if evaluation > maxEval:
                                        maxEval = evaluation
                                        best_move = move[0], move[1], ring, stelle
                                        if maxEval >= beta:
                                            break
                    else:
                        continue
                    break
                return best_move[0], best_move[1], best_move[2], best_move[3]

    ###
    # Minimax function is simpler and only remembers and returns scores of the decision tree without the moves
    ###
    def minimax(self, board, board_muhlen, player, alpha, beta, remaining_set, depth):
        if depth <= 1:
            # Static evaluation for gamemode 1
            if remaining_set >= 1:
                score_player = 0
                score_opponent = 0
                for i in range(3):
                    for j in range(8):
                        if board[i][j] == self.player:
                            score_player += 1
                            pass
                        elif board[i][j] == self.opponent:
                            score_opponent += 1
                        if gameutil.checkmuhle(i, j, board, board_muhlen, self.player) and \
                                board[i][j] == self.player:
                            score_player += 100

                        elif gameutil.checkmuhle(i, j, board, board_muhlen, self.opponent) and \
                                board[i][j] == self.opponent:
                            score_opponent += 1000
                        score_player += self.number_possible_moves(board, self.player)
                        score_opponent += self.number_possible_moves(board, self.opponent)
                score = score_player - score_opponent
                return score

            # Static evaluation for gamemode 2
            else:
                score_player = 0
                score_opponent = 0
                for i in range(3):
                    for j in range(8):
                        if board[i][j] == self.player:
                            score_player += 1
                            if not self.possiblemoves(i, j, board):
                                score_opponent += 5
                        elif board[i][j] == self.opponent:
                            score_opponent += 1
                            if not self.possiblemoves(i, j, board):
                                score_player += 5

                        if gameutil.checkmuhle(i, j, board, board_muhlen, self.player) and \
                                board[i][j] == self.player:
                            score_player += 10
                        elif gameutil.checkmuhle(i, j, board, board_muhlen, self.opponent) and \
                                board[i][j] == self.opponent:
                            score_opponent += 100
                return score_player - score_opponent
                        # Making a mill also generates points but is checked in the minimax function, not here

        # MAX
        if player == self.player:
            best_score = alpha
            # Phase 1
            if remaining_set:
                for ring in range(3):
                    for stelle in range(8):
                        if board[ring][stelle] == 0:
                            board_ = copy.deepcopy(board)
                            board_[ring][stelle] = player
                            muhlen_ = copy.deepcopy(board_muhlen)

                            if self.checkmuhle(ring, stelle, board_, player):
                                to_remove = self.toremove(board_, 1 if player == 2 else 2)
                                if board_[to_remove[0]][to_remove[1]] == (1 if player == 2 else 2) and not muhlen_[to_remove[0]][to_remove[1]] == 0:
                                    board_[to_remove[0]][to_remove[1]] = 0
                                    muhlen_ = self.update_board_muhlen(board_, muhlen_)

                            evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, best_score, beta, remaining_set - 1, depth-1)
                            if evaluation > best_score:
                                best_score = evaluation
                                if best_score >= beta:
                                    break
                    else:
                        continue
                    break
                return best_score
            else:
                # Phase 2
                mymen = 0
                theirmen = 0
                for i in range(3):
                    for j in range(8):
                        if board[i][j] == player:
                            mymen += 1
                        elif board[i][j] == 1 if player == 2 else 2:
                            theirmen += 1

                for ring in range(3):
                    for stelle in range(8):
                        if board[ring][stelle] == player:
                            possiblemoves = self.possiblemoves(ring, stelle, board)
                            if not possiblemoves:
                                continue
                            for move in possiblemoves:
                                board_ = copy.deepcopy(board)
                                muhlen_ = copy.deepcopy(board_muhlen)
                                board_[ring][stelle] = 0
                                try:
                                    board_[move[0]][move[1]] = player
                                except:
                                    print("ERROR"+str(move))
                                # check if new mill has been generated / zwickmuehle
                                score_addition = 0
                                if self.checkmuhle(move[0], move[1], board_, player):
                                    score_addition += 100
                                    # New mill generated
                                    if self.checkmuhle(ring, stelle, board, player):
                                        # Zwickmuehle
                                        score_addition += 500

                                    # Finally, remove one random enemy man
                                    to_remove = self.toremove(board_, 1 if player == 2 else 2)
                                    if board_[to_remove[0]][to_remove[1]] == (1 if player == 2 else 2) and muhlen_[to_remove[0]][to_remove[1]] == 0:
                                        board_[to_remove[0]][to_remove[1]] = 0
                                        muhlen_ = self.update_board_muhlen(board_, muhlen_)

                                evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, best_score, beta,
                                                          remaining_set, depth - 1)
                                evaluation += score_addition
                                if evaluation > best_score:
                                    best_score = evaluation
                                    if best_score >= beta:
                                        break
                        else:
                            continue
                        break
                return best_score


        # MIN
        else:
            best_score = beta
            if remaining_set:
                # Phase 1
                for ring in range(3):
                    for stelle in range(8):
                        if board[ring][stelle] == 0:
                            board_ = copy.deepcopy(board)
                            board_[ring][stelle] = player
                            muhlen_ = copy.deepcopy(board_muhlen)

                            if self.checkmuhle(ring, stelle, board_, player):
                                to_remove = self.toremove(board_, 1 if player == 2 else 2)
                                if board_[to_remove[0]][to_remove[1]] == (1 if player == 2 else 2) and muhlen_[to_remove[0]][to_remove[1]] == 0:
                                    board_[to_remove[0]][to_remove[1]] = 0
                                    muhlen_ = self.update_board_muhlen(board_, muhlen_)

                            evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, alpha, best_score, remaining_set - 1, depth - 1)
                            if evaluation < best_score:
                                best_score = evaluation
                                if best_score <= alpha:
                                    break
                    else:
                        continue
                    break
                return best_score
            else:
                # Phase 2
                mymen = 0
                theirmen = 0
                for i in range(3):
                    for j in range(8):
                        if board[i][j] == player:
                            mymen += 1
                        elif board[i][j] == 1 if player == 2 else 2:
                            theirmen += 1

                for ring in range(3):
                    for stelle in range(8):
                        if board[ring][stelle] == player:
                            possiblemoves = self.possiblemoves(ring, stelle, board)
                            if not possiblemoves:
                                continue
                            for move in possiblemoves:
                                board_ = copy.deepcopy(board)
                                muhlen_ = copy.deepcopy(board_muhlen)
                                board_[ring][stelle] = 0
                                try:
                                    board_[move[0]][move[1]] = player
                                except:
                                    print("ERROR"+str(move))
                                # check if new mill has been generated / zwickmuehle
                                score_addition = 0
                                if self.checkmuhle(move[0], move[1], board_, player):
                                    # New mill generated
                                    score_addition += 100
                                    if self.checkmuhle(ring, stelle, board, player):
                                        # Zwickmuehle
                                        score_addition += 500

                                    to_remove = self.toremove(board_, 1 if player == 2 else 2)
                                    if board_[to_remove[0]][to_remove[1]] == (1 if player == 2 else 2) and not \
                                    muhlen_[to_remove[0]][to_remove[1]] == 0:
                                        board_[to_remove[0]][to_remove[1]] = 0
                                        muhlen_ = self.update_board_muhlen(board_, muhlen_)

                                evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, alpha, best_score,
                                                          remaining_set, depth - 1)
                                evaluation += score_addition
                                if evaluation < best_score:
                                    best_score = evaluation
                                    if best_score <= alpha:
                                        break
                        else:
                            continue
                        break
                return best_score


    ###
    # Additional Functions for the AI
    ###

    def number_possible_moves(self, board, player):
        n = 0
        for i in range(3):
            for j in range(8):
                if board[i][j] == player:
                    # Left/Right you can go anytime, anywhere
                    if board[i][(j + 1) % 8] == 0:
                        n += 1
                    if board[i][(j - 1) % 8] == 0:
                        n += 1
                    # Up/Down you can only go in center positions
                    if j % 2 != 0:
                        if i == 0 and board[i + 1][j] == 0:
                            n += 1
                        if i == 1 and board[i + 1][j] == 0:
                            n += 1
                        if i == 1 and board[i - 1][j] == 0:
                            n += 1
                        if i == 2 and board[i - 1][j] == 0:
                            n += 1
        return n

    def possiblemoves(self, ringpos, stellepos, spielfeld):
        possiblemoves = []
        if stellepos % 2 == 0:  # Men on the edges
            if spielfeld[ringpos][(stellepos+1) % 8] == 0:  # Sideways
                possiblemoves.append((ringpos, (stellepos+1) % 8))
            if spielfeld[ringpos][(stellepos-1) % 8] == 0:
                possiblemoves.append((ringpos, (stellepos-1) % 8))
        else:  # Men on the center fields
            if spielfeld[ringpos][(stellepos+1) % 8] == 0:
                possiblemoves.append((ringpos, (stellepos+1) % 8))
            if spielfeld[ringpos][(stellepos-1) % 8] == 0:  # Sideways
                possiblemoves.append((ringpos, (stellepos-1) % 8))
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

    def checkmuhle(self, ringPos, stellePos, spielfeld, mancolor):
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


    def clearmuhlen(self, board, board_muhlen):
        tobecleared = []
        for ring in range(3):
            for stelle in range(8):
                if (not self.checkmuhle(ring, stelle, board, board[ring][stelle])) and (board_muhlen[ring][stelle] != 0):
                    tobecleared.append((ring, stelle))
        if len(tobecleared) == 0:
            return False
        else:
            return tobecleared


    def update_board_muhlen(self, board, board_muhlen_old):
        board_muhlen_new = copy.deepcopy(board_muhlen_old)
        for ring in range(3):
            for stelle in range(8):
                if self.checkmuhle(ring, stelle, board, board[ring][stelle]):
                    board_muhlen_new[ring][stelle] = 1
                else:
                    board_muhlen_new[ring][stelle] = 0
        return board_muhlen_new


    # Determines which man is most beneficial to be removed
    def toremove(self, board, enemy):
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
                        if board[(ring + 1) % 3][stelle] == enemy and (board[ring][(stelle + 1) % 8] == enemy or board[ring][(stelle - 1) % 8] == enemy):
                            evil_score += 100
                        if board[(ring + 2) % 3][stelle] == enemy and (board[ring][(stelle + 1) % 8] == enemy or board[ring][(stelle - 1) % 8] == enemy):
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
