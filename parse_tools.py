import re
import csv
import yaml
from io import StringIO

def file_splitter(filename):
    ''' 
    Split the file into csv and config
    
    Returns:
        csv_lines (list): list of strings where each string is a line of csv
        config (dict): the parsed config from the yaml
    
    '''
    reading_yaml_header = False
    yaml_line_count = 0
    
    csv_lines = []
    yaml_lines = []
    with open(filename, 'r') as rfile:
        for i, line in enumerate(csv.reader(rfile)):
            if i == 0 and line[0].startswith('---'):
                reading_yaml_header = True
                continue
                
            if reading_yaml_header:
                if line[0].startswith('---'):
                    reading_yaml_header = False
                    continue
                    
                else:
                    yaml_line_count += 1
            else:
                if len(line):
                    csv_lines.append(line)
    if yaml_line_count:
        with open(filename, 'r') as rfile:
            for i, line in enumerate(rfile):
                if i == 0:
                    continue 
                elif i > yaml_line_count: 
                    break
                else:
                    yaml_lines.append(line.rstrip())
        
    config = yaml.safe_load(StringIO("\n".join(yaml_lines)))
    return csv_lines, config


def cell_parser(cell_string):
    '''
    A simple cell parser that can split a cell string into composite parts

    Inputs:
        - cell_string (str): the contents of the cell before computation e.g. "= cost * quantity
    Output:
        - parts (list): an ordered list of numbers, column names and operators e.g. ["cost","*","quantity", "+", "3"]
    '''

    # Map operator chars to lambda functions
    operators = {
        '*': lambda x,y:x*y,
        '+': lambda x,y:x+y,
        '-': lambda x,y:x-y,
        '/': lambda x,y:x/y
    }

    parts = []
    current_col, current_num = "", ""
    reading_num, reading_col = False, False

    # Move cell by cell
    for char in cell_string:

        # If we are currently reading a number
        if reading_num:
            if char.isdigit() or char=='.':
                current_num += char
                continue
            # Otherwise, end of number
            else:
                parts.append(current_num)
                current_num = ''
                reading_num=False

        # If currently reading a column name
        if reading_col:
            if char.isalpha() or char=='_':
                current_col += char
                continue
            # Otherwise we have ended this collumn name
            else:
                parts.append(current_col)
                current_col = ''
                reading_col=False

        if char.isalpha() or char=='_':
            current_col += char
            reading_col=True

        elif char in operators:
            parts.append(char)

        elif char.isdigit() or char=='.':
            current_num += char
            reading_num=True

    # Closing out
    if reading_num:
        parts.append(current_num)

    elif reading_col:
        parts.append(current_col)

    return parts


def compute_lines(lines):
    '''
    A basic computation engine, can only handle within line multiplication for now
    
    Inputs:
        - lines (list): csv lines, a list of lists of strings that haven't yet been computed
    Output:
        (list): a list of lists of the same shape, but with computations filled in

    '''

    # Heading dictionary, maps column name to index
    hdict = dict( (y,x) for x,y in enumerate(lines[0]))

    new_lines = []
    for line in lines:

        new_line = []
        changed = False
        for cell in line:
            if cell.startswith('='):
                parsed = cell_parser(cell.lstrip('= '))
                mult_ind = parsed.index('*')
                if mult_ind:
                    val1 = float(line[hdict[parsed[mult_ind-1]]])
                    val2 = float(line[hdict[parsed[mult_ind+1]]])
                    val = val1 * val2
                    changed=True
                    new_line.append(val)
            else:
                new_line.append(cell)

        new_lines.append(new_line)

        print(f"{line}  -{'*' if changed else '-'}-> {new_line}")
    return new_lines

