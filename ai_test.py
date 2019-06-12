import copy
import gameutil
import random


class Morris:

    def __init__(self, spielbrett, spielbrett_muhlen, spieler, remaining):
        self.player = spieler
        self.remaining = remaining
        self.opponent = 1 if self.player == 2 else 2
        self.board = spielbrett
        self.board_muhlen = spielbrett_muhlen
        self.score, self.ring, self.stelle = self.minimax(self.board, self.board_muhlen, self.player, self.remaining)

    def minimax(self, board, board_muhlen, player, move, depth=3):

        opponent = 1 if player == 2 else 2

        if depth <= 0:  # Return the static evaluation
            # Generate static evaluation
            # Each piece gives 3 points, each mill gives one point, each possible move gives 0.1 points
            score_player = 0
            score_opponent = 0
            for i in range(3):
                for j in range(8):
                    if board[i][j] == self.player:
                        score_player += 3
                    elif board[i][j] == self.opponent:
                        score_opponent += 3
                    if gameutil.checkmuhle(i, j, board, board_muhlen, self.player) and \
                            board[i][j] == self.player:
                        score_player += 2.5
                        print("MUHLE")
                    elif gameutil.checkmuhle(i, j, board, board_muhlen, self.opponent) and \
                            board[i][j] == self.opponent:
                        score_opponent += 2.5
            score = score_player - score_opponent

            static_evaluation = (score, move[0], move[1])

            # End generate static evaluation

            return static_evaluation

        # If maximizing Player
        if player == self.player:
            maxEval = (-100000000000000000000000000000000000, 69, 69)
            # For each child in position:
            for ring in range(3):
                for stelle in range(8):
                    if board[ring][stelle] == 0:
                        child = copy.deepcopy(board)
                        child[ring][stelle] = player
                        child_muhlen = copy.deepcopy(board_muhlen)
                        if gameutil.checkmuhle(ring, stelle, child, child_muhlen, player):  # Just to generate mills
                            # Remove one man
                            toremoves = []
                            for i in range(3):
                                for j in range(8):
                                    if board[i][j] == opponent:
                                        toremoves.append((i, j))
                            for toremove in toremoves:
                                board_new = copy.deepcopy(board)
                                board_new[toremove[0]][toremove[1]] = 0
                                evaluation = self.minimax(board_new, child_muhlen, opponent, (ring, stelle), depth-1)
                                if evaluation[0] > maxEval[0]:
                                    maxEval = evaluation
                        evaluation = self.minimax(child, child_muhlen, opponent, (ring, stelle), depth - 1)
                        if evaluation[0] > maxEval[0]:
                            maxEval = evaluation
            return maxEval

        # If minimizing Player
        else:
            minEval = (100000000000000000000000000000000000, 69, 69)
            # For each child in position:
            for ring in range(3):
                for stelle in range(8):
                    if board[ring][stelle] == 0:
                        child = copy.deepcopy(board)
                        child[ring][stelle] = player
                        child_muhlen = copy.deepcopy(board_muhlen)
                        if gameutil.checkmuhle(ring, stelle, child, child_muhlen, player):  # Just to generate mills
                            # Remove one man
                            toremoves = []
                            for i in range(3):
                                for j in range(8):
                                    if board[i][j] == opponent:
                                        toremoves.append((i, j))
                            toremove = random.choice(toremoves)
                            board[toremove[0]][toremove[1]] = 0
                        evaluation = self.minimax(child, child_muhlen, opponent, (ring, stelle), depth-1)
                        if evaluation[0] < minEval[0]:
                            minEval = evaluation
            return minEval


'''
spielbrett = [[1, 1, 0, 2, 0, 0, 0, 0],
              [0, 1, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]
spielbrett_muhlen = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
remaining = {1: 9, 2: 9}
muhler = Morris(spielbrett, spielbrett_muhlen, 2, remaining)
print(muhler.score, muhler.ring, muhler.stelle)
'''