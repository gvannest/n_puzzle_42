import sys
from objects import Taquin
from termcolor import colored

def error_handling(e):
    print(colored(e, 'red'))
    sys.exit(0)

def compute_inversion(flat_grid):
    from math import sqrt
    grid_size = int(sqrt(len(flat_grid)))
    inv = 0
    for idx, x in enumerate(flat_grid):
        last_inv = inv
        i = idx + 1
        if x == 0: 
            #blank_on_odd = (grid_size - idx // grid_size + 1) % 2
            blank_on_odd =  not (idx // grid_size) % 2
            continue
        while i < len(flat_grid):
            if x > flat_grid[i] and flat_grid[i] != 0:
                inv += 1
            i += 1
    return inv, blank_on_odd

def is_solvable(flat_grid, grid_size):
    inv = 0
    inv , blank_on_odd = compute_inversion(flat_grid)
    if grid_size % 2 :
        return inv % 2
    else:
        if blank_on_odd == True and (inv % 2) == 2:
            return True
        elif blank_on_odd == False and (inv % 2) == 0:
            return True
    return False

def check_integrity(t):
    if len(t.numbers) != len(set(t.numbers)):
        error_handling("[ERROR]: Duplicate values")
    if set(t.numbers) != set(range(t.size**2)):
        error_handling("[ERROR]: Weird number suite")
    #t.g = [t.numbers[i:i+t.size] for i in range(0, len(t.numbers), t.size)]
    if not is_solvable(t.numbers, t.size):
        error_handling("[ERROR]: Can't be done")
    return t.numbers
