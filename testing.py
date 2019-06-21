import gameutil

board = [
    [0, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0]
]

board_muhlen = [
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0]
]

for i in range(3):
    for j in range(8):
        if gameutil.checkmuhle(i, j, board, board_muhlen, 2):
            print("muhle!")