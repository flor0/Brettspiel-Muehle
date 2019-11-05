from __future__ import absolute_import, division, print_function, unicode_literals
import functools, datahandler

import numpy as np
import tensorflow as tf

def moveconverter(a):
    converts = {
    'a7':(0, 0),
    'd7':(0, 1),
    'g7':(0, 2),
    'g4':(0, 3),
    'g1':(0, 4),
    'd1':(0, 5),
    'a1':(0, 6),
    'a4':(0, 7),
    'b6':(1, 0),
    'd6':(1, 1),
    'f6':(1, 2),
    'f4':(1, 3),
    'f2':(1, 4),
    'd2':(1, 5),
    'b2':(1, 6),
    'b4':(1, 7),
    'c5':(2, 0),
    'd5':(2, 1),
    'e5':(2, 2),
    'e4':(2, 3),
    'e3':(2, 4),
    'd3':(2, 5),
    'c3':(2, 6),
    'c4':(2, 7)
    }
    return converts[a]

def tupletostring(a):
    return "{}{}".format(a[0], a[1])


datafile = open("DATASET.expanded.txt", "r")
datafile_lines = datafile.readlines()

board_states = [line[:24] for line in datafile_lines]
remaining_hand_me = [int(line[24]) for line in datafile_lines]
remaining_hand_enemy = [int(line[25]) for line in datafile_lines]
remaining_board_me = [int(line[26]) for line in datafile_lines]
remaining_board_enemy = [int(line[27]) for line in datafile_lines]
answers = [line[29:] for line in datafile_lines]

mydataset = open("mydata.txt", "w")
mydataset.write("b00,b01,b02,b03,b04,b05,b06,b07,b10,b11,b12,b13,b14,b15,b16,b17,b20,b21,b22,b23,b24,b25,b26,b27,hand_me,hand_enemy,board_me,board_enemy,solution\n")
for i in range(len(datafile_lines)):
    if i % 10000 == 0:
        print(str(i)+"/"+str(len(datafile_lines)))
    if len(answers[i]) > 3:
        temp_array = []
        temp_array.append(moveconverter(answers[i][:2]))
        temp_array.append(moveconverter(answers[i][2:4]))
        solution = datahandler.get_int(temp_array)
    else:
        solution = datahandler.get_int(moveconverter(answers[i][:2]))

    mydataset.write(board_states[i].replace("M", "1,").replace("E", "2,").replace("O", "0,")+str(remaining_hand_me[i])+","+str(remaining_hand_enemy[i])+","+str(remaining_board_me[i])+","+str(remaining_board_enemy[i])+","+str(solution)+"\n")
mydataset.close()




