INPUT_FILE = 'input-not-quite-lisp'

map = {'(': 1, ')': -1}

def read_file(path):
    with open(path) as f:
        lines = f.read()
    return lines

def main():
    file = read_file(INPUT_FILE)
    parenthesis = list(file)
    sum = 0
    for index, entry in enumerate(parenthesis):
        sum += map[entry]
        position = index+1
        if (sum == -1):
            print("Reaches the basement (floor -1) for the first time at position", position)
            break

if __name__ == '__main__':
    main()