import math
import re

INPUT_FILE = 'wait-for-it-input' 
RACE_TIMES, RECORD_DISTANCES = [40817772], [219101213651089]

class Race():

    def __init__(self, time, record_distance):
        assert type(time) == int
        assert type(record_distance) == int
        self.time = time
        self.record_distance = record_distance
        self.possible_hold_times = set(range(1, time))

class ToyBoat(Race):

    def __init__(self, time, record_distance, initial_speed=0):
        assert type(time) == int
        assert type(record_distance) == int
        super().__init__(time, record_distance)
        self.initial_speed = initial_speed

    def _get_time_left_in_race(self, hold_time):
        return self.time - hold_time

    def _get_speed(self, hold_time):
        return hold_time
    
    def _calculate_distance(self, speed, time_left_in_race):
        return speed * time_left_in_race

    def _get_distance_travelled(self, hold_time):
        time_left_in_race = self._get_time_left_in_race(hold_time)
        speed = self._get_speed(hold_time)
        distance = self._calculate_distance(speed, time_left_in_race)
        
        return distance

    def _get_results(self):
        results = []
        for hold_time in iter(self.possible_hold_times):
            result = {}
            result["hold_time"] = hold_time
            result["distance_travelled"] = self._get_distance_travelled(hold_time)
            results.append(result)
        
        return results

    def _breaks_record(self, result):
        return result["distance_travelled"] > self.record_distance

    def get_number_of_broken_records(self):
        results = self._get_results()
        nr_broken_records = 0
        for result in results:
            if self._breaks_record(result): nr_broken_records += 1
        
        return nr_broken_records

def read_file(path=INPUT_FILE):
    lines = []
    with open(path) as f:
        lines = f.readlines()
    return lines

def parse_input(lines):
    ''' return list race_times and list record_distances '''
    race_times = []
    record_distances = []
    for line in lines:
        if "Time:" in line:
            raw_line = line.replace("Time:", "").strip()
            match = re.match(r'^\d+(?:\s+\d+){3}$', raw_line)
            race_times = [int(value) for value in match.group(0).split('     ')]
        if "Distance:" in line:
            raw_line = line.replace("Distance:", "").strip()
            match = re.match(r'^\d+(?:\s+\d+){3}$', raw_line)
            record_distances = [int(value) for value in match.group(0).split('   ')]
    
    return race_times, record_distances

def get_races(race_times, record_distances):
    races = [Race(race_time, record_distance) for race_time, record_distance in zip(race_times, record_distances)]

    return races

def get_number_of_broken_records_per_boat(races):
    number_of_broken_records_per_boat = []
    for race in races:
        number_of_broken_records_per_boat.append(ToyBoat(race.time, race.record_distance).get_number_of_broken_records())

    return number_of_broken_records_per_boat

def get_product(number_of_broken_records_per_boat):
    return math.prod(number_of_broken_records_per_boat)

if __name__ == '__main__':
    #lines = INPUT_TEST
    #lines = read_file()
    race_times, record_distances = RACE_TIMES, RECORD_DISTANCES
    races = get_races(race_times, record_distances)
    number_of_broken_records_per_boat = get_number_of_broken_records_per_boat(races)
    product = get_product(number_of_broken_records_per_boat)
    print(product) # 28101347 correct
    