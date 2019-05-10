import argparse, pytest, sys 
from parsing import process_file
from termcolor import cprint, colored
from npuzzle_solver import main as solve
import random
from integrity import is_solvable

def generator(size):
    while True:
        grid = [x for x in range(size**2)]
        random.shuffle(grid)
        if is_solvable(grid, size):
            break
    return grid

def main():
    parser = argparse.ArgumentParser(description="N-puzzle Solver")
    parser.add_argument('-f', '--filename',
                        type=str,
                        help="Put a '.txt' file containing a puzzle to solve")
    parser.add_argument('-g', '--generator',
                        type=int,
                        help="if the '--generator' flag is present, it must be followed by an int and optionnaly by the flag '-u' if you want a unsolvable puzzle")
    parser.add_argument('-m', '--method',
                        type=str,
                        choices=['manhattan', 'linear_conflict', 'misplaced_tiles'],
                        help="Method to be used for heuristic determination.",
                        default='misplaced_tiles')
    parser.add_argument('-a', '--algo',
                        type=str,
                        choices=['astar', 'gbfs', 'uniformed_cost', 'ida_star'],
                        help="Algorithm used to solve the n-puzzle.",
                        default='uniformed_cost')
    parser.add_argument('-v', '--visu',
                        help="Show the results as an interactive game",
                        action='store_true')

    parser.add_argument('-d', '--detail',
                        help="Detailed output",
                        action='store_true')


    args = parser.parse_args()
    if not args.filename and not args.generator:
        cprint("ERROR. filename or generator needed. use -h for help", 'red')
        sys.exit()
    if args.filename:
        grid = process_file(args.filename)
        cprint("File processed successfully", 'green')
    elif args.generator:
        grid = generator(args.generator)
        cprint("Grid generated", 'green')

    cprint("Trying to solve...   %s" % grid, 'green')
    solve(grid, args) 

if __name__ == '__main__':
    main()
