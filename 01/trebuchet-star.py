INPUT_FILE = 'input'
LETTER_DIGITS = {"zero","one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}
LETTER_DIGIT_TO_NUMBER = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

''' 
    Sum first and last digit(s) of each line in input file 

    Assume no negative numbers. Consider written numbers.
'''

def read_file(path):
    with open(path) as f:
        lines = f.readlines()
    return iter(lines)

def find_digit(line, index):
    character = line[index]
    if character.isdigit():
        return character
    else:
        return None

def get_first_number_digit(line):
    ''' Search from left to right '''
    for index in range(len(line)):
        found_digit = find_digit(line, index)
        if found_digit is not None: return found_digit, index

def get_last_number_digit(line, line_length):
    ''' Search from right to left '''
    for index in range(len(line)):
        idx = index+1
        found_digit = find_digit(line, -idx)
        if found_digit is not None: return found_digit, -idx % line_length

def get_first_letter_digit(letter_digit_indicies):
    ''' 
    Input [(<substring>, <start_index>), ...] 
    Returns <first substring>, <first start_index>
    '''
    try:
        first_letter_digit = letter_digit_indicies[0][0]
        number = str(LETTER_DIGIT_TO_NUMBER[first_letter_digit])
        first_start_index = letter_digit_indicies[0][1]
    
        return number, first_start_index
    except IndexError:
        return None, None

def get_last_letter_digit(letter_digits_indicies, line_length):
    ''' 
    Input [(<substring>, <start_index>), ...] 
    Returns <last substring>, <last start_index>
    '''
    try:
        last_letter_digit = letter_digits_indicies[-1][0]
        number = str(LETTER_DIGIT_TO_NUMBER[last_letter_digit])
        last_start_index = letter_digits_indicies[-1][1] % line_length
    
        return number, last_start_index
    except IndexError:
        return None, None

def get_letter_digits(line, line_length):
    ''' Finds all letter digits in order and appends to list (ordered) together with its start index. 
    Returns (<"first digit">, <first_digit_index>), (<"last digit">, <last_digit_index>)
    '''
    all_substring_indicies = [(line[i: j], i) for i in range(len(line)) for j in range(i + 1, len(line) + 1)]
    letter_digit_indicies = []
    for substring_index in all_substring_indicies:
        substring, start_index = substring_index[0], substring_index[1]
        if substring in LETTER_DIGITS: letter_digit_indicies.append((substring, start_index))

    return get_first_letter_digit(letter_digit_indicies), get_last_letter_digit(letter_digit_indicies, line_length)

def get_first(first_number_digit, first_letter_digit):
    ''' Compare indicies of the first letter and number and pick the first '''

    if first_letter_digit[0] is None:
        return first_number_digit[0]
    elif first_number_digit[1] < first_letter_digit[1]: 
        return first_number_digit[0]
    else:
        return first_letter_digit[0]
    
def get_last(last_number_digit, last_letter_digit):
    ''' Compare indicies of the last letter and number and pick the last '''

    if last_letter_digit[0] is None:
        return last_number_digit[0]
    elif last_number_digit[1] > last_letter_digit[1]:
        return last_number_digit[0]
    else:
        return last_letter_digit[0]

def get_sum(lines):
    sum = 0
    for line in lines:
        line_length = len(line)
        first_number_digit = get_first_number_digit(line)
        last_number_digit = get_last_number_digit(line, line_length)
        first_letter_digit, last_letter_digit = get_letter_digits(line, line_length)
        
        sum += int(get_first(first_number_digit, first_letter_digit) + get_last(last_number_digit, last_letter_digit))

    return sum
    
def main():
    lines = read_file(INPUT_FILE)
    sum = get_sum(lines)
    print(sum)

if __name__ == '__main__':
    main()