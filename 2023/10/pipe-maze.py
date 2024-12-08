''' 
    Convert each sign to a vector [north, east, south, west]
    '|' = [1,0,1,0]
    '-' = [0,1,0,1]
    'L' = [1,1,0,0]
    'J' = [1,0,0,1]
    etc.

    Checking one Pipe with its right element
    L- = [0,1,0,1]*[1,1,0,0]=[0,1,0,0] (output is valid vector east)
    This means right output is valid

'''

INPUT_FILE = 'pipe-maze-input'

class Map:

    NORTH = [1,0,0,0]
    EAST = [0,1,0,0]
    SOUTH = [0,0,1,0]
    WEST = [0,0,0,1]
    DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

    def __init__(self, lines):
        self.pipes = self._read_input(lines)
        self.start_coordinate = self._get_start_coordinate()

    def _read_input(self, lines):
        pipes = {}
        for y, line in enumerate(lines):
            for x, character in enumerate(line):
                pipes.update({(x+1,y+1): Pipe((x+1,y+1), character)})
        
        return pipes

    def _get_start_coordinate(self):
        for pipe in self.pipes.values():
            if pipe.character == 'S': return pipe.coordinate
        raise RuntimeError("Unable to find start coordinate.")
    
    def walk(self):
        number_of_steps = []
        for direction in self.DIRECTIONS:
            pipe = self.pipes[self.start_coordinate]
            is_endpoint = False
            is_starting_character = False
            steps = 0
            while(not is_starting_character and not is_endpoint):
                print(pipe.character, pipe.coordinate, "walking in direction", direction)
                direction, pipe, is_endpoint = self.take_step(pipe, direction)
                is_starting_character = pipe.character == 'S'
                steps += 1
            number_of_steps.append(steps)

        return number_of_steps
    
    def _get_new_pipe(self, new_coordinate):
        return self.pipes[new_coordinate]

    def take_step(self, pipe, input_direction):
        pipe.get_output_direction(input_direction)
        pipe.get_new_coordinate(input_direction)
        new_pipe = self._get_new_pipe(pipe.new_coordinate)

        return pipe.output_direction, new_pipe, pipe.is_endpoint()


class Pipe: 

    NORTH = [1,0,0,0]
    EAST = [0,1,0,0]
    SOUTH = [0,0,1,0]
    WEST = [0,0,0,1]

    def __init__(self, coordinate, character):
        self.character = character
        self.coordinate = coordinate
        self.transformation_vector = self._get_transformation_vector()
    
    def _get_transformation_vector(self):
        ''' [north, east, south, west] 
        Defined as inverted input and output direction.
        '''
        match self.character:
            case '|': return [1,0,1,0]
            case '-': return [0,1,0,1]
            case 'L': return [0,1,1,0] # maps south (input) to east (output)
            case 'J': return [0,0,1,1] # maps south (input) to west (output)
            case '7': return [1,0,0,1] # maps north (input) to west (output)
            case 'F': return [0,1,1,0] # maps north (input) to east (output)
            case '.': return [0,0,0,0]
            case 'S': return [1,1,1,1]

    def invert_direction(self, direction):
        match direction:
            case self.NORTH:
                return self.SOUTH
            case self.EAST:
                return self.WEST
            case self.SOUTH:
                return self.NORTH
            case self.WEST:
                return self.EAST

    def get_output_direction(self, input_direction):
        ''' Example
            - Input direction is south [0,0,1,0] which means coming from north
            - Vector is [1,0,1,0]
            => Output vector is [1*0,0*0,1*1,0*0]=[0,0,1,0] which means output direction is also south
        '''
        # Relative to the new pipe, the input direction is the inverted value of the previous output direction 
        self.output_direction = [a*b for a,b in zip(input_direction, self.transformation_vector)]
        print("output_direction is ", self.output_direction)

    def get_new_coordinate(self, direction):
        x, y = self.coordinate[0], self.coordinate[1]
        match direction:
            case self.NORTH: 
                self.new_coordinate = (x, y-1)
            case self.EAST: 
                self.new_coordinate = (x+1, y)
            case self.SOUTH: 
                self.new_coordinate = (x, y+1)
            case self.WEST: 
                self.new_coordinate = (x-1, y)

    def is_endpoint(self):
        print("Is endpoint is", self.output_direction == [0,0,0,0])
        return self.output_direction == [0,0,0,0]
    

def _read_file(path):
    with open(path) as f:
        lines = f.readlines()
    return lines

def main():
    lines = _read_file(INPUT_FILE)
    map = Map(lines)
    map.walk()

    

if __name__ == '__main__':
    main()