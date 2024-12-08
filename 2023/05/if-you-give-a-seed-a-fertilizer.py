import re

INPUT_FILE = 'if-you-give-a-seed-a-fertilizer-input' 
INPUT_TEST = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''.split('\n')


class Seed:
    def __init__(self, number):
        self.number = int(number)

class Map:

    def __init__(self, content, category):
            self.source, self.target = self._parse_category(category)
            self.source_destination_ranges = self._parse_content(content, category)
        
    def _parse_category(self, category):
        [source, target] = category.split('-to-')

        return source, target

    def _parse_category_content(self, category_content):
        ''' self.destination_range_start, self.source_range_start, self.range_length '''
        [destination_range_start, source_range_start, range_length] = category_content.split(' ')
        
        return int(destination_range_start), int(source_range_start), int(range_length)

    def _parse_content(self, content, category):
        source_destination_ranges = []
        category_contents = content[category]
        for category_content in category_contents:
            range = {}
            destination_range_start, source_range_start, range_length = self._parse_category_content(category_content)
            destination_range_end = destination_range_start + range_length
            source_range_end = source_range_start + range_length
            range["destination_range_start"] = destination_range_start
            range["destination_range_end"] = destination_range_end
            range["source_range_start"] = source_range_start
            range["source_range_end"] = source_range_end
            range["length"] = range_length
            
            source_destination_ranges.append(range)
            
        return source_destination_ranges
    
    def _is_in_source_range(self, source, range):
        assert type(source) == int
        if source >= range["source_range_start"] and source <= range["source_range_end"]:
            return True

    def _get_destination_value(self, source, range):
        ''' Get difference from source range start and get the target value as the same delta from the target value start '''
        delta = source - range["source_range_start"]

        return int(range["destination_range_start"] + delta)

    def apply(self, source):
        ''' If source in any range, return destination value, else return the source number '''
        for range in self.source_destination_ranges:
            if self._is_in_source_range(source, range):
                return self._get_destination_value(source, range)
            
        return source
        
            
class SeedToSoil(Map):

    def __init__(self, content, category='seed-to-soil'):
        super().__init__(content, category)
        
class SoilToFertilizer(Map):

    def __init__(self, content, category='soil-to-fertilizer'):
        super().__init__(content, category)

class FertilizerToWater(Map):

    def __init__(self, content, category='fertilizer-to-water'):
        super().__init__(content, category)

class WaterToLight(Map):

    def __init__(self, content, category='water-to-light'):
        super().__init__(content, category)

class LightToTemperature(Map):

    def __init__(self, content, category='light-to-temperature'):
        super().__init__(content, category)

class TemperatureToHumidity(Map):

    def __init__(self, content, category='temperature-to-humidity'):
        super().__init__(content, category)

class HumidityToLocation(Map):

    def __init__(self, content, category='humidity-to-location'):
        super().__init__(content, category)


def get_match_pattern(header):
    return r':(.*)' if header == 'seeds:' else r'^\d+(?:\s+\d+){2}$'

def read_file(path=INPUT_FILE):
    lines = []
    with open(path) as f:
        lines = f.readlines()
    return lines
    
def get_content(lines):
    categories = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light", "light-to-temperature", "temperature-to-humidity", "humidity-to-location"]
    categories.reverse()
    headers = ["seed-to-soil map:", "soil-to-fertilizer map:", "fertilizer-to-water map:", "water-to-light map:", "light-to-temperature map:", "temperature-to-humidity map:", "humidity-to-location map:"]
    headers.reverse()
    lines.reverse()
    set_of_headers = set(headers)
    content = {}

    # Get seeds
    line = lines.pop()
    match = re.match(r'seeds:(.*)', line)
    content["seeds"] = match.group(0).replace("seeds: ", "").split(' ')

    # Get rest of content    
    while (lines):
        line = lines.pop()
        if line.strip() in set_of_headers:
            category = categories.pop()
            content[category] = []
            line = lines.pop()
        match = re.match(r'^\d+(?:\s+\d+){2}$', line)
        if match: 
            content[category].append(match.group(0))

    return content

def get_location(seed):

    # Get mappers
    seed_to_soil = SeedToSoil(content)
    soil_to_fertilizer = SoilToFertilizer(content)
    fertilizer_to_water = FertilizerToWater(content)
    water_to_light = WaterToLight(content)
    light_to_temperature = LightToTemperature(content)
    temperature_to_humidity = TemperatureToHumidity(content)
    humidity_to_location = HumidityToLocation(content)

    # Apply mappers in a chain
    soil = seed_to_soil.apply(seed.number)
    fertilizer = soil_to_fertilizer.apply(soil)
    water = fertilizer_to_water.apply(fertilizer)
    light = water_to_light.apply(water)
    temperature = light_to_temperature.apply(light)
    humidity = temperature_to_humidity.apply(temperature)
    location = humidity_to_location.apply(humidity)

    return location
    

def get_locations(seeds):
    locations = set()
    for seed in seeds:
        locations.add(get_location(seed))
    
    return locations

def get_lowest_location_number(locations):
    return min(locations)

if __name__ == '__main__':
    #lines = INPUT_TEST
    lines = read_file()
    content = get_content(lines)
    seeds = [Seed(number) for number in content["seeds"]]
    locations = get_locations(seeds)
    lowest_location_number = get_lowest_location_number(locations)
    print(lowest_location_number)
    

    
    

    