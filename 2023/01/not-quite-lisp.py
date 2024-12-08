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
    for entry in parenthesis:
        sum += map[entry]
        
    print(sum)

if __name__ == '__main__':
    main()