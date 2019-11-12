import serial

def convert_board(vector_board):
    matrix_board = [[0 for k in range(8)] for l in range(3)]
    for i in range(3):
        for j in range(8):
            matrix_board[i][j] = vector_board[(i*8)+j]
    return matrix_board


def human_move(matrix_board_old, matrix_board_new, board, player_ai):
    to, from_, remove = False
    for i in range(3):
        for j in range(8):
            if matrix_board_old[i][j] == 0 and matrix_board_new[i][j] != 0:
                to = (i, j)
            if matrix_board_old[i][j] != 0 and matrix_board_new[i][j] == 0:
                from_ = (i, j)
            if board[i][j] == player_ai and matrix_board_old[i][j] == player_ai and matrix_board_new[i][j] == 0:
                remove = (i, j)
    return to, from_, remove


def await_move():
    done = False
    old_vec = readboard()
    while not done:
        vec = readboard()
        if not vec == old_vec:
            time.sleep(2.0)
            old_vec = vec
            vec = readboard()
            if vec == old_vec:
                return True




