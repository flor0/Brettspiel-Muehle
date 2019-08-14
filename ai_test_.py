import copy, gameutil, random

class Morris:
    def __init__(self, board, board_muhlen, real_player):
        self.board = board
        self.board_muhlen = board_muhlen
        self.player = real_player
        self.opponent = 1 if self.player == 2 else 2
        self.score, self.ring, self.stelle = self.make_score(board, board_muhlen, real_player)

    def make_score(self, board, board_muhlen, player, alpha=1000000000000000, beta=-1000000000000000000, depth=4):
        maxEval = beta
        best_move = False
        for ring in range(3):
            for stelle in range(8):
                if board[ring][stelle] == 0:
                    move = (ring, stelle)
                    evaluation = self.minimax(copy.deepcopy(board), copy.deepcopy(board_muhlen), 1 if player == 2 else 2
                                              , move, alpha, beta, depth=3)
                    if evaluation > maxEval:
                        maxEval = evaluation
                        best_move = move
        return maxEval, best_move[0], best_move[1]

    def minimax(self, board, board_muhlen, player, move, alpha=100000000000000, beta=-1000000000000000000, depth=4):
        # Static evaluation
        if depth < 1:
            score_player = 0
            score_opponent = 0
            for i in range(3):
                for j in range(8):
                    if board[i][j] == self.player:
                        # score_player += 0.00005
                        pass
                    elif board[i][j] == self.opponent:
                        # score_opponent += 0.00005
                        pass
                    if gameutil.checkmuhle(i, j, board, board_muhlen, self.player) and \
                            board[i][j] == self.player:
                        score_player += 101

                    elif gameutil.checkmuhle(i, j, board, board_muhlen, self.opponent) and \
                            board[i][j] == self.opponent:
                        score_opponent += 100
                    score_player += self.number_possible_moves(board, self.player)
                    score_opponent += self.number_possible_moves(board, self.opponent)
            score = score_player - score_opponent

            static_evaluation = score

            # End generate static evaluation

            return static_evaluation

        # Make all possible moves
        maxEval = beta
        minEval = alpha

        for ring in range(3):
            for stelle in range(8):
                if board[ring][stelle] == 0:
                    board_new = copy.deepcopy(board)
                    board_new[ring][stelle] = player
                    board_new_muhlen = copy.deepcopy(board_muhlen)
                    move = (ring, stelle)
                    if self.player == player:
                        evaluation = self.minimax(board_new, board_new_muhlen, 1 if player == 2 else 2, move, alpha=maxEval, beta=beta, depth=depth-1)
                        if evaluation > maxEval:
                            maxEval = evaluation
                            return maxEval
                    else:
                        evaluation = self.minimax(board_new, board_new_muhlen, 1 if player == 2 else 2, move, alpha=alpha, beta=minEval, depth=depth-1)
                        if evaluation < minEval:
                            minEval = evaluation
                            return minEval
        if self.player == player:
            return maxEval
        else:
            return minEval

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
