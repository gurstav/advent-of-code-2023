INPUT_FILE = 'input'

''' Sum first and last digit(s) of each line in input file 

    Assume no negative numbers.
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

def get_first_digit(line):
    ''' Search from left to right '''
    for index in range(len(line)):
        found_digit = find_digit(line, index)
        if found_digit is not None: return found_digit

def get_last_digit(line):
    ''' Search from right to left '''
    for index in range(len(line)):
        idx = index+1
        found_digit = find_digit(line, -idx)
        if found_digit is not None: return found_digit

def get_count(lines):
    sum = 0
    for line in lines:
        sum += int(get_first_digit(line) + get_last_digit(line))
    print(sum)
    

def main():
    lines = read_file(INPUT_FILE)
    get_count(lines)

if __name__ == '__main__':
    main()