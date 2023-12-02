import collections
import math

'''
Determine which games would have been possible if the bag had been loaded 
with only 12 red cubes, 13 green cubes, and 14 blue cubes. 

What is the sum of the IDs of those games?

'''

INPUT_FILE = 'cube-conundrum-input' 
GIVEN_COLORS = {'red': 12, 'green': 13, 'blue': 14}

class Game():

    def __init__(self, line):
        self.line = line
        self.id, self.colors = self._parse_line()

    def _get_id(self):
        ''' Parses string "Game n: k red, l green, b blue '''
        game_entry = self.line.split(':')[0] # Gets "Game id"
        return int(game_entry.split(' ')[1]) # Gets id
    
    class MaxColorConfiguration():
        ''' 
        Since a game is only considering to be possible given the maximum number of shown cubes at once, extract the maximum set of colors from a configuration 
        For example if (r,g,b) configurations are (1, 2, 4), (5, 1, 3), the maximum color configuration is (5,2,4).
        '''

        EXPECTED_COLORS = ['red', 'green', 'blue']

        def __init__(self, round_configurations):
            self.round_configurations = round_configurations
            self.rounds = self._parse_round_configurations()
            self.colors = self._get_max_color_configuration()
            
        def _parse_round_configurations(self):
            ''' Returns for example [[' 1 green', ' 2 red', ' 6 blue'], [' 4 red', ' 1 green', ' 3 blue'], [' 7 blue', ' 5 green'], [' 6 blue', ' 2 red', ' 1 green']]'''
            rounds = []
            for round in self.round_configurations:
                rounds.append(round.split(','))
            return rounds
        
        def _get_max_color_configuration(self):
            max_count = {}
            for color in self.EXPECTED_COLORS:
                max_count[color] = 0

            for round in self.rounds:
                for entry in round:
                    clean_entry = entry.lstrip().rstrip()
                    [color_count, color] = clean_entry.split(' ') # Get e.g. ["1", "green"]
                    color_count = int(color_count)
                    if max_count[color] < color_count: max_count[color] = color_count

            return max_count

    def _get_colors(self):
        ''' Parses string "Game n: k red, l green, b blue '''
        round = self.line.split(':')[1]
        round_configurations = round.split(';')

        return self.MaxColorConfiguration(round_configurations).colors

    def _parse_line(self):
        ''' Return id and a map of colors by parsing a line in the input '''

        return self._get_id(), self._get_colors()
    
    def _is_valid_count(self, given_count, game_count):
        ''' Checks if the number of multiples of a given color is >=1 in the game color, if yes, then the game is possible '''
        return math.floor(given_count/game_count) >= 1

    def is_possible(self, given_colors=GIVEN_COLORS):

        valid_counts = []
        for (game_color, game_count) in self.colors.items():
            given_count = given_colors[game_color]
            is_valid_count = self._is_valid_count(given_count, game_count)
            valid_counts.append(is_valid_count)
            
        print(f" Game {self.id} has max set of colors {self.colors}.")
        print(f" \t\t tested against {given_colors}")
        return all(valid_counts)


def read_file(path):
    with open(path) as f:
        lines = f.readlines()
    return iter(lines)

def parse_game_configs():
    pass

def get_games():
    lines = read_file(INPUT_FILE)
    games = []
    for line in lines:
        games.append(Game(line))

    return games

def get_sum(games):
    sum = 0
    for game in games:
        if(game.is_possible()): 
            sum += game.id
    print(f"The sum of possible games is {sum}")

def main():
    games = get_games()
    get_sum(games)
    pass

if __name__ == '__main__':
    main()