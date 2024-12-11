from typing import List
from copy import deepcopy
import itertools

WIRE_CHARACTERS = {'|', '-'}
INPUT_CHARACTERS = ('A', 'B')
GATE_CHARACTER = 'G'
OUTPUT_CHARACTER = 'X'

def get_board(opname: str) -> str:
    # Read board from file

    with open(f"./circuits/{opname}.txt") as f:
        return f.read()

def gridify_board(board: str) -> List[List[str]]:
    # Return 2D char array representation of board

    return list(list(line) for line in board.split('\n'))

def nand(a,b):
    if a == None or b == None:
        return None
    return not (a and b)

def evaluate_function(board: str, *inputs: bool) -> bool:
    # Given a board string, evaluate the boolean function with the
    # given inputs
    board_arr = gridify_board(board)
    # determine idx of input(s), A/B
    trans = list(map(list, itertools.zip_longest(*board_arr, fillvalue=' ')))

    # get board info
    y_dim = len(trans)
    x_dim = len(trans[0])

    # boolean array for tracking
    bool_grid = [[None] * x_dim for _ in range(y_dim)]

    # this section is for identifying where inputs are
    if len(inputs) == 2:
        possible_inputs = {'A', 'B'}
    else:
        possible_inputs = {'A'}
    remaining_inputs = list(possible_inputs)
    input_mapping = {}
    for i, row in enumerate(trans):
        row_set = set(row)
        for input in possible_inputs:
            if input in row_set:
                input_mapping[input] = (i, row.index(input))
                remaining_inputs.remove(input)
        if len(remaining_inputs) == 0:
            break

    # this section initializes those inputs into boolean array
    for i, inp in enumerate(input_mapping.keys()):
        idx = input_mapping[inp]
        bool_grid[idx[0]][idx[1]] = inputs[i]

    # iterate repeatedly throw circuit, propagating values one at a time through array
    while True:
        for i, row in enumerate(trans):
            for j, val in enumerate(row):
                if bool_grid[i][j] is None:
                    if val in WIRE_CHARACTERS:
                        if val == '-':
                            bool_grid[i][j] = bool_grid[i-1][j]
                        else: # val == '|'
                            if (trans[i-1][j] == '-'):
                                if (bool_grid[i-1][j] is not None):
                                    bool_grid[i][j] = bool_grid[i-1][j]
                            else:
                                if (j == 0):
                                    if bool_grid[i][j+1] is not None:
                                        bool_grid[i][j] = bool_grid[i][j+1]
                                elif (j == x_dim-1):
                                    if bool_grid[i][j-1] is not None:
                                        bool_grid[i][j] = bool_grid[i][j-1]
                                else:
                                    if bool_grid[i][j+1] != None:
                                        bool_grid[i][j] = bool_grid[i][j+1]
                                    elif bool_grid[i][j-1] != None:
                                        bool_grid[i][j] = bool_grid[i][j-1]
                    if val == GATE_CHARACTER:
                        bool_grid[i][j] = nand(bool_grid[i][j-1], bool_grid[i][j+1])
                    if (val == OUTPUT_CHARACTER) and (bool_grid[i-1][j] != None):
                        return bool_grid[i-1][j]