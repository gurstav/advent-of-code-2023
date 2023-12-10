INPUT_FILE = 'haunted-wasteland-input'
TEST_INPUT = 'test-input'


class Map:
    
    def __init__(self, start_node_label='AAA'):
        self.nodes = {}
        self.start_node_label = start_node_label

    def add_nodes(self, map_nodes):
        for node in map_nodes:
            self.nodes.update({node.label: node})

    def find_node_using_directions(self, directions, node_to_find='ZZZ'):
        iter = 0
        new_node_label = self.start_node_label
        reversed_directions = list(reversed(directions))
        directions_left = reversed_directions.copy()
        not_found = True
        while(not_found):
            if not directions_left: 
                directions_left.extend(reversed_directions)
            direction = directions_left.pop()
            node_in_direction = getattr(self.nodes[new_node_label], direction)
            new_node_label = self.nodes[node_in_direction].label
            iter += 1
            print(direction, iter, "going to", new_node_label)
            if new_node_label == node_to_find:
                print(node_to_find, "was found in", iter)
                not_found = False

class Node():

    def __init__(self, label, left, right):
        self.label = label 
        self.L = left
        self.R = right



def read_file(path=INPUT_FILE):
    with open(path) as f:
        lines = f.readlines()
    return lines

def get_directions(lines):
    lines.reverse()
    return [char for char in lines.pop().replace('\n','').strip()]

def get_map_nodes(lines):
    map_nodes = [] 
    while(lines):
        line = lines.pop().replace('\n','')
        if line.strip() != '' and line !='\n':
            split_line = line.split(' = ')
            label, directions = split_line[0], split_line[1]
            (left, right) = tuple(directions.replace('(','').replace(')','').split(', '))
            map_nodes.append(Node(label, left, right))

    return map_nodes

def main():
    lines = read_file(INPUT_FILE)
    directions = get_directions(lines)
    map_nodes = get_map_nodes(lines)
    map = Map()
    map.add_nodes(map_nodes)
    map.find_node_using_directions(directions)

if __name__ == '__main__':
    main()

