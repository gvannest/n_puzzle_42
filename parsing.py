import os, re
from integrity import *
from objects import Taquin


def read_file(filename):
    if os.path.isfile(filename):
        try :
            with open(filename, 'r') as f:
                return parse_file(f)    
        except Exception as e:
            error_handling(e)
    else:
        error_handling("[ERROR]: File does not exist. L2T")

def process_file(filename):
    """
    send the raw data in parse file, and return a Taquin object with the size 
    """
    #numbers = parse_file(read_file(filename))
    taquin = read_file(filename)
    return check_integrity(taquin)


# parse lines up to get size of the taquin. Then retrieve the lines.. ? 
def get_size(line):
    match = re.match(r"^(\d+\s*)(?!.+^#)(#.*)?$", line) or None
    size = 0
    if match and len(line) == len(match.group(0)):
        size = int(re.match(r'^(\d+)', line).group(0))
    else: 
        error_handling("[PARSING ERROR]: Looks like a size problem -->{0}<--".format(line))
    return size

def get_line(size, line):
    num = []
    match = re.match(r'^((\d+)\s*)+\s*(?!.+^#)(#.*)?$', line or None)
    if match and len(line) == len(match.group(0)):
        """
        retrieve all numbers
        """
        buff = ''
        for idx, char in enumerate(line):
            if char == ' ':
                continue
            elif char == '#':
                break
            elif char.isdigit():
                buff += char
                if idx + 1 == len(line) or not line[idx + 1].isdigit():
                    num.append(int(buff))
                    buff = ''
    if len(num) != size:
        error_handling("[PARSING ERROR]: Parsing error in line -->{0}<--".format(line))
    return num

def parse_file(f):
    """
    data is the content of the whole file to read. 
    first we retrive the size of the grid
    We need to retrieve first the size of the grid, then for each line in grid : 
            - strip trailing space
            - check if first char is a '#'. If it isnt a digit -> exit
            - if it is a number, we parse the line to retrieve all the numbers separated by white_spaces
        case : 
            - no given size
            - give size = 0
    """
    t = Taquin()
    data = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        elif line[0] == '#':
            continue
        elif t.size == 0:
            t.size = get_size(line)
        elif line != '':
            t.numbers.extend(get_line(t.size, line))
    if t.size == 0 or len(t.numbers) != t.size**2:
        error_handling("[PARSING ERROR]: Parsing error")
    return t
