import re
import csv

# Patterns
re_open_tag = r'\s*<(?P<name>[^/][a-z]+)(?P<attrs>[^>]*)>\s*'
re_close_tag = r'\s*</(?P<name>[a-z]+)\s*>\s*'


match = re.match(re_open_tag,'<config something="yeah" no>')
if match:
    print(match)
    print(match.groupdict())


def file_splitter(filename):
    '''
    Load the .ccsv file and split it into the csv part and the tags

    Inputs:
        - filename (str or Path): the file to be loaded

    Outputs:
        - csv_lines (list): a list where each entry corresponds to a line and is a list of strings
        - tags (dict): a mapping from tag name (str) to properties (dict)
    '''
    csv_lines = []
    tags = {}

    # First read csv content at the top of the file
    with open(filename, 'r') as rfile:

        for line in csv.reader(rfile):
            # skip blank lines
            if not len(line):
                continue
            # Check if first "cell" actually has a tag
            open_tag_match = re.match(re_open_tag,line[0])
            if open_tag_match:
                break
            else:
                csv_lines.append(line)

        # If finished reading the file and no tags found, return
        if not bool(open_tag_match):
            return csv_lines, tags

        # Otherwise, tags are present. Start splitting out the tags
        current_tag = open_tag_match.groupdict()['name']
        current_tag_contents = ''

        # Now use rfile (csv reader has moved the pointer to the right point in the file)
        for line in rfile.readlines():

            # If we have an open tag in hand
            if current_tag:

                # Check if this tag is getting closed
                close_tag_match = re.match(re_close_tag, line)
                if close_tag_match:
                    if close_tag_match.groupdict()['name'] == current_tag:
                        print(f'found closing tag for <{current_tag}>')
                    else:
                        raise ValueError(f'Incorrect closing tag found for <{current_tag}> tag')

                    # Store the contents and clear the temporary variables
                    tags[current_tag] = current_tag_contents
                    current_tag_contents = ''
                    current_tag = None
                    open_tag_found = False
                    continue

                # If tag not closd in this line, append the contents
                else:
                    current_tag_contents += line.strip()

            # Otherwise we are looking for a new open tag
            else:
                open_tag_match = re.match(re_open_tag,line)
                if open_tag_match:
                    current_tag = open_tag_match.groupdict()['name']
                    current_tag_contents = ''
                    continue

    return csv_lines, tags


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

