import copy, gameutil

class Morris:
    def __init__(self, board, board_muhlen, real_player, remaining_set):
        self.board = board
        self.board_muhlen = board_muhlen
        self.player = real_player
        self.opponent = 1 if self.player == 2 else 2
        self.remaining_set = remaining_set
        self.score, self.ring, self.stelle = self.make_score(board, board_muhlen, real_player, -1000000000000000,
                                                             100000000000000)
    ###
    # First function being called, remembers moves to return them
    ###
    def make_score(self, board, board_muhlen, player, alpha, beta):
        maxEval = alpha
        best_move = False
        for ring in range(3):
            for stelle in range(8):
                if board[ring][stelle] == 0:
                    move = (ring, stelle)
                    board_continue = copy.deepcopy(board)
                    board_continue[ring][stelle] = self.player
                    evaluation = self.minimax(board_continue, copy.deepcopy(board_muhlen), 1 if player == 2 else 2
                                              , alpha, beta, self.remaining_set, 3)
                    # TODO: Evaluation is always 0 !?
                    print(move, evaluation)
                    if evaluation > maxEval:
                        maxEval = evaluation
                        best_move = move
        return maxEval, best_move[0], best_move[1]


    ###
    # Minimax function is simpler and only remembers and returns scores of the decision tree without the moves
    ###
    def minimax(self, board, board_muhlen, player, alpha, beta, remaining_set, depth):
        if depth <= 1:
            score_player = 0
            score_opponent = 0
            for i in range(3):
                for j in range(8):
                    if board[i][j] == self.player:
                        score_player += 1
                        pass
                    elif board[i][j] == self.opponent:
                        score_opponent += 1
                        pass
                    if gameutil.checkmuhle(i, j, board, board_muhlen, self.player) and \
                            board[i][j] == self.player:
                        score_player += 100

                    elif gameutil.checkmuhle(i, j, board, board_muhlen, self.opponent) and \
                            board[i][j] == self.opponent:
                        score_opponent += 110
                    score_player += self.number_possible_moves(board, self.player)
                    score_opponent += self.number_possible_moves(board, self.opponent)
            score = score_player - score_opponent
            # print(score)
            # End generate static evaluation
            return score

        # MAX
        if player == self.player:
            best_score = -10000000000000000000
            # Phase 1
            if remaining_set:
                for ring in range(3):
                    for stelle in range(8):
                        if board[ring][stelle] == 0:
                            board_ = copy.deepcopy(board)
                            board_[ring][stelle] = player
                            muhlen_ = copy.deepcopy(board_muhlen)

                            if gameutil.checkmuhle(ring, stelle, board_, muhlen_, player):
                                for ring_ in range(3):
                                    for stelle_ in range(8):
                                        if board_[ring_][stelle_] == (1 if player == 2 else 2) and muhlen_[ring_][stelle_] == 0:
                                            board_[ring_][stelle_] = 0
                                            break
                                    else:
                                        continue
                                    break

                            evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, alpha, beta, remaining_set - 1, depth-1)
                            if evaluation > best_score:
                                best_score = evaluation
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
                            for move in possiblemoves:
                                board_ = copy.deepcopy(board)
                                muhlen_ = copy.deepcopy(board_muhlen)
                                board_[ring][stelle] = 0
                                board[move[0]][move[1]] = player
                                evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, alpha, beta, remaining_set, depth-1)
                                if evaluation > best_score:
                                    best_score = evaluation
                return best_score


        # MIN
        else:
            best_score = 10000000000000000000
            if remaining_set:
                # Phase 1
                for ring in range(3):
                    for stelle in range(8):
                        if board[ring][stelle] == 0:
                            board_ = copy.deepcopy(board)
                            board_[ring][stelle] = player
                            muhlen_ = copy.deepcopy(board_muhlen)

                            if gameutil.checkmuhle(ring, stelle, board_, muhlen_, player):
                                for ring_ in range(3):
                                    for stelle_ in range(8):
                                        if board_[ring_][stelle_] == (1 if player == 2 else 2) and muhlen_[ring_][stelle_] == 0:
                                            board_[ring_][stelle_] = 0
                                            break
                                    else:
                                        continue
                                    break

                            evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, alpha, beta, remaining_set - 1, depth - 1)
                            if evaluation < best_score:
                                best_score = evaluation
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
                            for move in possiblemoves:
                                board_ = copy.deepcopy(board)
                                muhlen_ = copy.deepcopy(board_muhlen)
                                board_[ring][stelle] = 0
                                board[move[0]][move[1]] = player
                                evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, alpha, beta,
                                                          remaining_set, depth - 1)
                                if evaluation < best_score:
                                    best_score = evaluation
                return best_score

    # Not working, new version found above ^
    def minimax_(self, board, board_muhlen, player, alpha, beta, depth):
        # Static evaluation
        if depth < 1:
            score_player = 0
            score_opponent = 0
            for i in range(3):
                for j in range(8):
                    if board[i][j] == self.player:
                        # score_player += 1
                        pass
                    elif board[i][j] == self.opponent:
                        # score_opponent += 1
                        pass
                    if gameutil.checkmuhle(i, j, board, board_muhlen, self.player) and \
                            board[i][j] == self.player:
                        score_player += 100

                    elif gameutil.checkmuhle(i, j, board, board_muhlen, self.opponent) and \
                            board[i][j] == self.opponent:
                        score_opponent += 110
                    # score_player += self.number_possible_moves(board, self.player)
                    # score_opponent += self.number_possible_moves(board, self.opponent)
            score = score_player - score_opponent
            static_evaluation = score
            # print(score)
            # End generate static evaluation
            return static_evaluation

        # Make all possible moves
        maxEval = alpha
        minEval = beta

        for ring in range(3):
            for stelle in range(8):
                if board[ring][stelle] == 0:
                    board_new = copy.deepcopy(board)
                    board_new[ring][stelle] = player
                    board_new_muhlen = copy.deepcopy(board_muhlen)
                    if self.player == player:
                        # Max player
                        evaluation = self.minimax(board_new, board_new_muhlen, 1 if player == 2 else 2, maxEval, beta, depth-1)
                        if evaluation > maxEval:
                            maxEval = evaluation
                            if maxEval >= beta:
                                print("MAX", maxEval, depth)
                                return maxEval
                    else:
                        # Min player
                        evaluation = self.minimax(board_new, board_new_muhlen, 1 if player == 2 else 2, alpha, minEval, depth-1)
                        if evaluation < minEval:
                            minEval = evaluation
                            if minEval <= alpha:
                                print("MIN", minEval, depth)
                                return minEval
        if self.player == player:
            print("MAX", maxEval, depth)
            return maxEval
        else:
            print("MIN", minEval, depth)
            return minEval
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
                possiblemoves.append((ringpos, stellepos+1 % 8))
            if spielfeld[ringpos][(stellepos-1) % 8] == 0:  # Sideways
                possiblemoves.append((ringpos, stellepos-1 % 8))
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
