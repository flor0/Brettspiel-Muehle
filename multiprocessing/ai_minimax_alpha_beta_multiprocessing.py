import copy, gameutil, multiprocessing, ctypes, time
from multiprocessing import freeze_support



class Morris:
    def __init__(self, board, board_muhlen, real_player, remaining_set):
        self.board = board
        self.board_muhlen = board_muhlen
        self.player = real_player
        self.opponent = 1 if self.player == 2 else 2
        self.remaining_set = remaining_set
        self.max_depth = 4
        t = time.time()
        self.out = self.make_score(board, board_muhlen, real_player, -1000000000000000,
                                                             100000000000000)

        print("AI time: %s sec" % str(time.time() - t))
    ###
    # First function being called, remembers moves to return them
    ###
    def make_score(self, board, board_muhlen, player, alpha, beta):
        manager = multiprocessing.Manager()
        n = 0
        procs = []
        evaluations = manager.dict()
        moves = manager.dict()
        poss = manager.dict()
        maxEval = alpha
        best_move = False
        print("debug")

        # If phase 1
        if self.remaining_set > 0:
            for ring in range(3):
                for stelle in range(8):
                    if board[ring][stelle] == 0:
                        move = (ring, stelle)
                        moves[n] = move
                        board_continue = copy.deepcopy(board)
                        board_continue[ring][stelle] = self.player

                        proc = multiprocessing.Process(target=self.minimax, args=(board_continue, copy.deepcopy(board_muhlen), 1 if player == 2 else 2
                                                  , maxEval, beta, self.remaining_set, self.max_depth, evaluations, n,))
                        procs.append(proc)
                        proc.start()
                        n += 1
            for proc in procs:
                proc.join()
                print("joined")
            print(evaluations)
            for evaluation in range(n):
                if evaluations[evaluation] > maxEval:
                    maxEval = evaluations[evaluation]
                    best_move = moves[evaluation]

            return best_move[0], best_move[1]
        # If phase 2
        else:
            for ring in range(3):
                for stelle in range(8):
                    if board[ring][stelle] == self.player:
                        possiblemoves = self.possiblemoves(ring, stelle, board)
                        if possiblemoves:
                            for move in possiblemoves:
                                moves[n] = move
                                poss[n] = (ring, stelle)
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
                                proc = multiprocessing.Process(target=self.minimax, args=(board_, muhlen_, 1 if player == 2 else 2
                                                          , maxEval, beta, self.remaining_set, self.max_depth, evaluations, n,))
                                procs.append(proc)
                                proc.start()
                                n += 1

            for proc in procs:
                proc.join()
                print("joined")
            print(evaluations)
            print("hahaha")
            for evaluation in range(len(evaluations)):
                if evaluations[evaluation] > maxEval:
                    maxEval = evaluations[evaluation]
                    best_move = moves[evaluation]
                    best_move = moves[evaluation][0], moves[evaluation][1], poss[evaluation][0], poss[evaluation][1]

            return best_move[0], best_move[1], best_move[2], best_move[3]


    ###
    # Minimax function is simpler and only remembers and returns scores of the decision tree without the moves
    ###
    def minimax(self, board, board_muhlen, player, alpha, beta, remaining_set, depth, upper_eval, upper_key):
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
                            score_opponent += 110
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

                            if gameutil.checkmuhle(ring, stelle, board_, muhlen_, player):
                                for ring_ in range(3):
                                    for stelle_ in range(8):
                                        # TODO: Consider all possible men being removed
                                        # Take the first enemy man and remove it
                                        if board_[ring_][stelle_] == (1 if player == 2 else 2) and muhlen_[ring_][stelle_] == 0:
                                            board_[ring_][stelle_] = 0
                                            # break stelle
                                            break
                                    else:
                                        # continue if stelle wasnt broken
                                        continue
                                    # break ring if stelle was broken
                                    break

                            evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, best_score, beta, remaining_set - 1, depth-1, upper_eval, upper_key)
                            if evaluation > best_score:
                                best_score = evaluation
                                if best_score >= beta:
                                    break
                    else:
                        continue
                    break
                if depth == self.max_depth:
                    upper_eval[upper_key] = best_score
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
                                # TODO: kinda whack
                                score_addition = 0
                                if self.checkmuhle(move[0], move[1], board_, player):
                                    # New mill generated
                                    score_addition += 20
                                    if self.checkmuhle(ring, stelle, board, player):
                                        # Zwickmuehle
                                        score_addition += 60

                                    # Finally, remove one random enemy man
                                    for ring_ in range(3):
                                        for stelle_ in range(8):
                                            if board_[ring_][stelle_] == (1 if player == 2 else 2) and muhlen_[ring_][stelle_] == 0:
                                                board_[ring_][stelle_] = 0
                                                break
                                        else:
                                            continue
                                        break

                                evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, best_score, beta,
                                                          remaining_set, depth - 1, upper_eval, upper_key)
                                evaluation += score_addition
                                if evaluation > best_score:
                                    best_score = evaluation
                                    if best_score >= beta:
                                        break
                        else:
                            continue
                        break
                if depth == self.max_depth:
                    upper_eval[upper_key] = best_score
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
                                for ring_ in range(3):
                                    for stelle_ in range(8):
                                        if board_[ring_][stelle_] == (1 if player == 2 else 2) and muhlen_[ring_][stelle_] == 0:
                                            board_[ring_][stelle_] = 0
                                            break
                                    else:
                                        continue
                                    break

                            evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, alpha, best_score, remaining_set - 1, depth - 1, upper_eval, upper_key)
                            if evaluation < best_score:
                                best_score = evaluation
                                if best_score <= alpha:
                                    break
                    else:
                        continue
                    break
                if depth == self.max_depth:
                    upper_eval[upper_key] = best_score
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
                                # TODO: kinda whack
                                score_addition = 0
                                if self.checkmuhle(move[0], move[1], board_, player):
                                    # New mill generated
                                    score_addition += 20
                                    if self.checkmuhle(ring, stelle, board, player):
                                        # Zwickmuehle
                                        score_addition += 60

                                    # Finally, remove one enemy man
                                    for ring_ in range(3):
                                        for stelle_ in range(8):
                                            if board_[ring_][stelle_] == (1 if player == 2 else 2) and muhlen_[ring_][stelle_] == 0:
                                                board_[ring_][stelle_] = 0
                                                break
                                        else:
                                            continue
                                        break

                                evaluation = self.minimax(board_, muhlen_, 1 if player == 2 else 2, alpha, best_score,
                                                          remaining_set, depth - 1, upper_eval, upper_key)
                                evaluation += score_addition
                                if evaluation < best_score:
                                    best_score = evaluation
                                    if best_score <= alpha:
                                        break
                        else:
                            continue
                        break
                if depth == self.max_depth:
                    upper_eval[upper_key] = best_score
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


if __name__ == "__main__":
    freeze_support()
    input_file = open("ai_in.txt", "r")
    input_file_data = input_file.readlines()
    print(eval(input_file_data[3]))
    morris = Morris(eval(input_file_data[0]), eval(input_file_data[1]), eval(input_file_data[2]),
                    eval(input_file_data[3]))
    print("hahahaha, writing out!")
    file_out = open("ai_out.txt", "w")
    file_out.write("("+str(morris.out[0])+", "+str(morris.out[1])+")"+"\n")
    try:
        if morris.out[2] and morris.out[3]:
            file_out.write("("+str(morris.out[2])+", "+str(morris.out[3])+")")
    except:
        pass
    file_out.close()