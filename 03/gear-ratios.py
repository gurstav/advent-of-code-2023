'''
# Get input
# Read input into a n x m matrix A
# Get indicies of entries on each row (x,y). This will be a set of indicies (l_start, k) to  (l_end, k)
#   Get allowed symbols
#   Get numbers
#
# Check adjecency
    Row above A[l_start-1, k-1] to A[l_end, k-1]
    Same row A[l_start-1, k] to A[l_end+1, k]
    Row below A[l_start-1, k+1] to A[l_end, k+1]
'''
import re


''' TEST CASES (from internet somewhere) 
Should render
    Part 1: 925 (OK!)
    Part 2: 6756

Test cases covered:
    Number with no surrounding symbol
    Number with symbol before and after on same line
    Number with symbol vertically above and below
    Number with diagonal symbol in all 4 possible diagonals
    Possible gear with 1, 2, 3 and 4 surrounding numbers
    Gear with different numbers
    Gear with same numbers
    Non gear with 2 unique surrounding numbers
    Number at beginning/end of line
    Number at beginning/end of grid
    Numbers need to have a symbol adjacent to be a valid part, not another number
    Single digit numbers at the end of a row can be valid parts
    An odd Javascript parsing error (co /u/anopse )
'''
TEST_CASES = [
"12.......*..",
"+.........34",
".......-12..",
"..78........",
"..*....60...",
"78.........9",
".5.....23..$",
"8...90*12...",
"............",
"2.2......12.",
".*.........*",
"1.1..503+.56"
]


INPUT_FILE = 'gear-ratios-input' 
NON_ALLOWED_SYMBOLS = {}
DELIMITERS = {"."}

def read_file(path=INPUT_FILE):
    with open(path) as f:
        lines = f.readlines()
    return lines

def get_sum():
    pass

def get_matrix(lines):
    matrix = []
    for x, line in enumerate(lines):
        matrix.append([])
        for y, character in enumerate(line):
            if character != '\n': matrix[x].append(character)

    return matrix

def find_distinct_numbers(line):
    return set(re.findall(r'\d+', line))

class Number():

    def __init__(self, value, start_index, end_index, row_nr):
        self.value = int(value)
        self.start_index = start_index
        self.end_index = end_index
        self.row_nr = row_nr

def find_indicies_of_number(value, line, distinct_numbers_on_line):
    ''' TODO NEED TO FIX MULTIPLE OF SAME NUMBERS ON SAME LINE '''
    # TODO ''' should return zip start_index, end_index'''
    start_indicies = [match.start() for match in re.finditer(f'\\b{value}\\b', line)] # '\\b . \\b' sets exact regexp boundary    
    end_indicies = [i+len(value)-1 for i in start_indicies]

    return zip(start_indicies, end_indicies)

def get_numbers(lines):
    numbers = []
    for row_nr, line in enumerate(lines):
        distinct_numbers_on_line = find_distinct_numbers(line)
        for value in iter(distinct_numbers_on_line):
            indicies_of_number = find_indicies_of_number(value, line, distinct_numbers_on_line)
            for start_index, end_index in indicies_of_number:
                numbers.append(Number(value, start_index, end_index, row_nr))

    return numbers

def is_symbol(character):
    if not character.isdigit() and character not in NON_ALLOWED_SYMBOLS and character not in DELIMITERS:
        return True
    else:
        return False

def has_adjacent_symbol_above(number, matrix): 
    row_above_nr = number.row_nr-1
    if (row_above_nr < 0): # Guard top row
        return False
    row_above = matrix[row_above_nr]
    row_length = len(row_above)
    from_index = number.start_index-1 if number.start_index-1 >= 0 else 0 # Guard left edge
    to_index = number.end_index+2 if number.end_index+2 <= row_length else row_length # Guard right edge
    adjacent_characters = row_above[from_index:to_index]
    # DEBUG: print(f"{number.value} on {number.start_index}:{number.end_index} has adjacent_characters {adjacent_characters} on row above")
    has_symbol = []
    for character in adjacent_characters:
        has_symbol.append(is_symbol(character))
    
    return any(has_symbol)
    
def has_adjacent_symbol_on_same_row(number, matrix): 
    same_row = matrix[number.row_nr]
    row_length = len(same_row)
    has_symbol = []

    index_before = number.start_index-1
    if (index_before >= 0):
        character_before = same_row[index_before]
        # DEBUG: print(f"{character_before} before {number.value}")
        has_symbol.append(is_symbol(character_before))
    else:
        has_symbol.append(False)

    index_after = number.end_index+1
    if (index_after < row_length):
        character_after = same_row[index_after]
        # DEBUG: print(f"{character_after} after {number.value} (on indicies {number.start_index}:{number.end_index})")
        has_symbol.append(is_symbol(character_after))
    else:
        has_symbol.append(False)

    return any(has_symbol)

def has_adjacent_symbol_below(number, matrix): 
    matrix_rows = len(matrix)
    if (number.row_nr+1 >= matrix_rows): # Guard bottom row
        return False
    row_below = matrix[number.row_nr+1]
    row_length = len(row_below)
    from_index = number.start_index-1 if number.start_index-1 >= 0 else 0 # Guard left edge
    to_index = number.end_index+2 if number.end_index+2 <= row_length else row_length # Guard right edge
    adjacent_characters = row_below[from_index:to_index]

    has_symbol = []
    for character in adjacent_characters:
        has_symbol.append(is_symbol(character))

    return any(has_symbol)

def check_has_adjacent_symbol(numbers, matrix):
    for number in numbers:
        number.has_adjacent_symbol_above = has_adjacent_symbol_above(number, matrix)
        number.has_adjacent_symbol_on_same_row = has_adjacent_symbol_on_same_row(number, matrix)
        number.has_adjacent_symbol_below = has_adjacent_symbol_below(number, matrix)

        number.has_adjacent_symbol = any([number.has_adjacent_symbol_above, number.has_adjacent_symbol_on_same_row, number.has_adjacent_symbol_below])

if __name__ == '__main__':
    # DEBUG: lines = TEST_CASES
    lines = read_file()
    
    numbers = get_numbers(lines)
    matrix = get_matrix(lines)
    check_has_adjacent_symbol(numbers, matrix)
    sum = 0
    for number in numbers:
        # DEBUG: print(f"{number.value} {number.has_adjacent_symbol} (above: {number.has_adjacent_symbol_above}, same: {number.has_adjacent_symbol_on_same_row}, below: {number.has_adjacent_symbol_below}) ")
        if number.has_adjacent_symbol: 
            sum += number.value
            
    print("Sum is ", sum) # 538046 correct