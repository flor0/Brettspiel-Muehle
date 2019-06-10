import copy
import gameutil
import numpy as np



class Morris:

    def __init__(self, spielbrett, spieler):
        self.player = spieler
        self.opponent = 1 if self.player == 2 else 2
        self.board = spielbrett

    def minimax(self, board, board_muhlen, player, remaining, remaining_to_set=18, depth=3):

        # Initialisations
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
                    if board[ring][stelle] == 0:

                        # Placing man
                        board_new = copy.deepcopy(board)
                        board_new[ring][stelle] = player
                        moves_to_evaluate.append((ring, stelle))
                        # End placing man

                        # Mühle
                        if gameutil.checkmuhle(ring, stelle, board_new):
                            board_muhlen_new = copy.deepcopy(board_muhlen)
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

                                    elif board_new[i][j] == opponent:
                                        board_temp = copy.deepcopy(board_new)
                                        board_temp[i][j] = 0
                                        boards_to_evaluate.append(board_temp)
                                        boards_muhlen_to_evaluate.append(board_muhlen_new)
                        # End Mühle

                        else:
                            boards_to_evaluate.append(board_new)
                            boards_muhlen_to_evaluate.append(board_muhlen)


    # Evaluate

    # Anz Spielsteine
    for i in range(3):
        for j in range(8):
            if brett

    # End evaluate



