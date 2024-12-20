INPUT_FILE = 'mirage-maintenance-input'
TEST_INPUT = 'test-input'

class Value():

    ''' Star solution should be the same but with a mirrored extrapolation triangle.
     
    This solution
     - reverses the lists when creating the extrapolation triangle
     - switching the sign of row value to used to build triangle

    '''

    def __init__(self, history):
        self.history = history
        self.difference_steps = self._get_difference_steps()
        self.reversed_difference_steps = self._get_reversed_difference_steps()
        self.extrapolation_triangle = self._get_extrapolation_triangle()
        self.extrapolation_value = self._get_extrapolation_value()

    def get_difference(self, values):
        difference = []
        for value, next_value in zip(values, values[1:]):
            difference.append(next_value-value)

        return difference
    
    def _get_reversed_difference_steps(self):
        rds = []
        for step in self.difference_steps:
            step.reverse()
            rds.append(step)
            
        return rds

    def _get_difference_steps(self):
        difference_steps = []
        difference_step = self.history
        difference_steps.append(difference_step)
        has_not_only_zeroes = set(difference_step)!={0}
        while (has_not_only_zeroes):
            difference_step = self.get_difference(difference_step)
            difference_steps.append(difference_step)
            has_not_only_zeroes = set(difference_step)!={0}

        return list(reversed(difference_steps))
    
    def _get_extrapolation_triangle(self):
        triangle = []
        print(self.history, "has reversed difference steps", self.reversed_difference_steps)
        for this_line, next_line in zip(self.reversed_difference_steps, self.reversed_difference_steps[1:]):
            this_line.append(this_line[-1]) # Append last value on this line to this line
            next_line.append(next_line[-1]-this_line[-1]) # Star: Append NEGATIVE current last value on next line and last value on this line to the next line
            triangle.append(next_line)
        
        print(" this gives a triangle", triangle)
        return triangle
        
    def _get_extrapolation_value(self):
        return self.extrapolation_triangle[-1][-1]


def read_file(path=INPUT_FILE):
    with open(path) as f:
        lines = f.readlines()
    return lines

def get_values(lines):
    values = []
    for lines in lines:
        raw_values = lines.strip().split(' ')
        int_values = [int(value) for value in raw_values]
        values.append(Value(int_values))

    return values
        
def get_sum(values):
    sum = 0
    for value in values:
        sum += value.extrapolation_value

    return sum

def main():
    lines = read_file(INPUT_FILE)
    values = get_values(lines)
    sum = get_sum(values)
    print(sum) # Correct 1112

if __name__ == '__main__':
    main()