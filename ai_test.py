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
        self.score, self.ring, self.stelle = self.minimax(self.board, self.board_muhlen, self.player, self.remaining, -10000000000000, 100000000000000)

    def minimax(self, board, board_muhlen, player, move, alpha, beta, depth=4):

        opponent = 1 if player == 2 else 2

        if depth <= 0:  # Return the static evaluation
            # Generate static evaluation
            """
            Evaluation depends on the state of the game
            1st state:  Mills are valued high but preventing the enemy from having mills is more important
                        Adjacent free spaces are a priority, so you have more options to move and are not trapped by the enemy
            2nd state:  Mills are a priority but so is not getting trapped
                        Having a man is now valued
            3rd state:  Preventing mills is most important                        
            """
            score_player = 0
            score_opponent = 0
            for i in range(3):
                for j in range(8):
                    if board[i][j] == self.player:
                        #score_player += 0.00005
                        pass
                    elif board[i][j] == self.opponent:
                        #score_opponent += 0.00005
                        pass
                    if gameutil.checkmuhle(i, j, board, board_muhlen, self.player) and \
                            board[i][j] == self.player:
                        score_player += 10

                    elif gameutil.checkmuhle(i, j, board, board_muhlen, self.opponent) and \
                            board[i][j] == self.opponent:
                        score_opponent += 15
                    score_player += self.number_possible_moves(board, self.player)
                    score_opponent += self.number_possible_moves(board, self.opponent)
            score = score_player - score_opponent

            static_evaluation = (score, move[0], move[1])

            # End generate static evaluation

            return static_evaluation

        # If maximizing Player
        if player == self.player:
            maxEval = (alpha, 69, 69)
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
                                evaluation = self.minimax(board_new, child_muhlen, opponent, (ring, stelle), maxEval[0], beta, depth-1)
                                if evaluation[0] > maxEval[0]:
                                    maxEval = evaluation
                                    if maxEval[0] >= beta:
                                        break
                        evaluation = self.minimax(child, child_muhlen, opponent, (ring, stelle), maxEval[0], beta, depth - 1)
                        if evaluation[0] > maxEval[0]:
                            maxEval = evaluation
                            if maxEval[0] >= beta:
                                break
                if maxEval[0] >= beta:
                    break
            return maxEval

        # If minimizing Player
        else:
            minEval = (beta, 69, 69)
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
                        evaluation = self.minimax(child, child_muhlen, opponent, (ring, stelle), alpha, minEval[0], depth-1)
                        if evaluation[0] < minEval[0]:
                            minEval = evaluation
                            if minEval[0] <= alpha:
                                break
                if minEval[0] <= alpha:
                    break
            return minEval

    # Functions for the AI
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