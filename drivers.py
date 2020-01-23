import serial, time
import serial.tools.list_ports

graveyard_positions = ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"]  # Positions here
global graveyard_full_index
graveyard_full_index = 0
global graveyard_empty_index
graveyard_empty_index = 0

initial = "XX"
coords = [["00","30","60","63","66","36","06","03"], ["11","31","51","53","55","35","15","13"], ["22", "32", "42", "43", "44","34","24","23"]]


def open_sensor_arduino():
    ser = serial.Serial("/dev/ttyUSB0", 1000000, timeout=.1)
    time.sleep(1.55)
    ser.flushInput()
    return ser

def open_motor_arduino_wait():
    ser = serial.Serial("/dev/ttyUSB2", 1000000, timeout=None)
    time.sleep(1.55)
    ser.flushInput()
    return ser


def open_display_arduino():
    ser = serial.Serial("/dev/ttyUSB1", 1000000, timeout=.1)
    time.sleep(1.55)
    ser.flushInput()
    return ser


def open_motor_arduino():
    ser = serial.Serial("/dev/ttyUSB2", 1000000, timeout=.1)
    time.sleep(1.55)
    ser.flushInput()
    return ser


def readline_as_array(ser):
    ser.write("0".encode("utf-8"))
    time.sleep(0.1)
    rawserial = ser.readline()
    stringdata = rawserial.decode("utf-8")
    stringarray = eval(stringdata)
    new_array = [0 for i in range(24)]
    for i in range(24):
        if stringarray[i] == 0:
            new_array[i] = 1
    return new_array


def convert_board(vector_board):
    matrix_board = [[0 for k in range(8)] for l in range(3)]
    for i in range(3):
        for j in range(8):
            matrix_board[i][j] = vector_board[(i*8)+j]
    return matrix_board


def human_move(matrix_board_old, matrix_board_new, board, player_ai):
    to, from_, remove = False, False, False
    for i in range(3):
        for j in range(8):
            if matrix_board_old[i][j] == 0 and matrix_board_new[i][j] != 0:
                to = (i, j)
            if matrix_board_old[i][j] != 0 and matrix_board_new[i][j] == 0:
                from_ = (i, j)
            if board[i][j] == player_ai and matrix_board_old[i][j] == player_ai and matrix_board_new[i][j] == 0:
                remove = (i, j)
    if to and from_ and not remove:
        print("Human move drivers 1 : {}".format([to, from_]))
        return [to, from_]
    if to and from_ and remove:
        print("Human move drivers 2 : {}".format([to, from_, remove]))
        return [to, from_, remove]
    if to:
        print("Human move drivers 3 {}".format(to))
        return to
    if not to and from_ and not remove:
        return from_
    else:
        print("{}{}{}{}{}{}{}".format(to, from_, remove, matrix_board_old, matrix_board_new,board,player_ai))


def await_move():
    done = False
    old_vec = readline_as_array(sensor_arduino)
    while not done:
        vec = readline_as_array(sensor_arduino)
        if not vec == old_vec:
            time.sleep(2.0)
            old_vec = vec
            vec = readline_as_array(sensor_arduino)
            if vec == old_vec:
                return True


def move_to(move):
    global graveyard_full_index
    graveyard_positions = ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"]
    goto(graveyard_positions[graveyard_full_index])
    graveyard_full_index = (graveyard_full_index + 1) % 9
    grab()
    print("haha {}".format(move))
    goto(coords[move[0]][move[1]])
    release()
    return_to_init()

def move_from_to(move):
    to = move[0]
    from_ = move[1]
    goto(coords[from_[0]][from_[1]])
    grab()
    goto(coords[to[0]][to[1]])
    release()
    return_to_init()

def remove(move):
    global graveyard_empty_index
    goto(coords[move[0]][move[1]])
    grab()
    goto(graveyard_positions[graveyard_empty_index])
    graveyard_empty_index = (graveyard_empty_index+1) % 9
    release()
    return_to_init()


def grab():
    time.sleep(1)
    motor_arduino.write("VD".encode("utf-8"))   # lower magnet
    time.sleep(0.5)
    motor_arduino.write("MO".encode("utf-8"))   # Activate magnet
    time.sleep(0.5)
    motor_arduino.write("VU".encode("utf-8"))   # raise magnet
    time.sleep(1)


def release():
    time.sleep(1)
    motor_arduino.write("VD".encode("utf-8"))   # Lower magnet
    time.sleep(0.5)
    motor_arduino.write("MF".encode("utf-8"))   #deactivate magnet
    time.sleep(0.5)
    motor_arduino.write("VU".encode("utf-8"))   # raise magnet
    time.sleep(1)


def goto(move):
    print("going to init...")
    motor_arduino_wait.flushInput()
    motor_arduino.write("XX".encode("utf-8"))
    data = motor_arduino_wait.read()
    print("went to init")

    print("going to position...")
    motor_arduino_wait.flushInput()
    motor_arduino.write(move.encode("utf-8"))
    data = motor_arduino_wait.read()
    print("went to position")


def return_to_init():
    print("returning to init...")
    motor_arduino_wait.flushInput()
    motor_arduino.write("XX".encode("utf-8"))
    data = motor_arduino_wait.read()
    print("returned to init")


def update_display(number):
    display_arduino.write(str(number).encode("utf-8"))


display_arduino = open_display_arduino()
sensor_arduino = open_sensor_arduino()
motor_arduino = open_motor_arduino()

motor_arduino_wait = open_motor_arduino_wait()

return_to_init()
