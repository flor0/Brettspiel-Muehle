import copy
import gameutil
import numpy as np



class Morris:

    def __init__(self, spielbrett, spielbrett_muhlen, spieler, remaining):
        self.player = spieler
        self.remaining = remaining
        self.opponent = 1 if self.player == 2 else 2
        self.board = spielbrett
        self.board_muhlen = spielbrett_muhlen
        self.score, self.ring, self.stelle = self.minimax(self.board, self.board_muhlen, self.player, self.remaining)

    def minimax(self, board, board_muhlen, player, remaining, remaining_to_set=18, depth=3):

        if depth <= 0:
            return 0, None, None


        # Initialisations
        remaining_new = remaining
        opponent = 1 if player == 2 else 2
        nodes = []  # A node is: (score, ring, stelle)
        board_new = copy.deepcopy(board)
        score = 0
        boards_to_evaluate = []
        boards_muhlen_to_evaluate = []
        moves_to_evaluate = []

        # Placing men
        if remaining_to_set > 0:
            for ring in range(3):
                for stelle in range(8):
                    print(board[ring][stelle])
                    if board[ring][stelle] == 0:
                        # Placing man
                        board_new = copy.deepcopy(board)
                        board_new[ring][stelle] = player
                        moves_to_evaluate.append((ring, stelle))
                        # End placing man

                        # Mühle
                        board_muhlen_new = copy.deepcopy(board_muhlen)

                        if gameutil.checkmuhle(ring, stelle, board_new, board_muhlen_new, player):
                            board_muhlen_new[ring][stelle] = 1
                            score += 5  # Could be part of evaluate
                            for i in range(3):
                                for j in range(8):
                                    if board_new[i][j] == opponent and gameutil.hasnotonlymills(opponent, board_new, board_muhlen):
                                        if board_muhlen_new[i][j] == 0:
                                            board_temp = copy.deepcopy(board_new)
                                            board_temp[i][j] = 0
                                            boards_to_evaluate.append(board_temp)
                                            boards_muhlen_to_evaluate.append(board_muhlen_new)
                                            remaining_new[opponent] -= 1

                                    elif board_new[i][j] == opponent:
                                        board_temp = copy.deepcopy(board_new)
                                        board_temp[i][j] = 0
                                        boards_to_evaluate.append(board_temp)
                                        boards_muhlen_to_evaluate.append(board_muhlen_new)
                                        remaining_new[opponent] -= 1
                        # End Mühle

                        else:
                            boards_to_evaluate.append(board_new)
                            boards_muhlen_to_evaluate.append(board_muhlen)


        # Evaluate

        # Anz Spielsteine
        for i in range(3):
            for j in range(8):
                if board[i][j] == player:
                    score += 3
        # End Anz SPielsteine

        # Rekursion
        data = []
        for i in range(len(boards_to_evaluate)):
            data.append(self.minimax(boards_to_evaluate[i], boards_muhlen_to_evaluate[i], opponent, remaining_new, remaining_to_set-1, depth-1))

        # End Rekursion
        # Max Zug
        recursion_scores = []
        recursion_zuge = []
        for i in range(len(data)):
            recursion_scores.append(data[i][0])
            recursion_zuge.append((data[i][1], data[i][2]))
        try:
            max_score = max(recursion_scores) if player == self.player else min(recursion_scores)
            max_score_index = recursion_scores.index(max_score)
            print(recursion_zuge[max_score_index][0])
            return (score, moves_to_evaluate[max_score_index][0], moves_to_evaluate[max_score_index][1])
        except:
            return (score, 69, 69)
        # End max zug

        # End evaluate





spielbrett = [[1, 1, 0, 2, 0, 0, 0, 0],
              [0, 1, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]
spielbrett_muhlen = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
remaining = {1: 9, 2: 9}
muhler = Morris(spielbrett, spielbrett_muhlen, 2, remaining)
print(muhler.score, muhler.ring, muhler.stelle)