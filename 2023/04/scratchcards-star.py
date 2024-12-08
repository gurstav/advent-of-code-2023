
import re

'''
    Plan
    1. Read file into list of lines
    2. Create a Card object for each line in lines to (ordered) list cards
        a. Parse input
            a. Split on ':' 
                Left part into 'card_details' = 'Card <card number>'
                Right part into 'play_numbers' = '<winning numbers> | <scratch numbers>'
            b. Assign Card attributes
                a. Split card_details on ' ' and add right part as 'number' to Card attribute
                b. Split play_numbers on '|'
                    Don't forget to strip from spaces
                    a. split left part on ' ' and set to the 'winning_numbers' attribute (as set)
                    b. split right part on ' ' and set to 'scratch_numbers' attribute (as set)
    3. Create a check to see how many matching winning and scratch numbers there are
        Count cardinality of scratch_numbers.intersection(winning_numbers)
    4. Calculate sum
        The first match makes the card worth one point and each match after the first doubles the point value of that card.
        For example:

        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
        In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers you have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers you have, four of them (48, 83, 17, and 86) are winning numbers! That means card 1 is worth 8 points (1 for the first match, then doubled three times for each of the three matches after the first).

        Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
        Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
        Card 4 has one winning number (84), so it is worth 1 point.
        Card 5 has no winning numbers, so it is worth no points.
        Card 6 has no winning numbers, so it is worth no points.
        So, in this example, the Elf's pile of scratchcards is worth 13 points.

'''

TEST_CASES = ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53", "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", "Card 3: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", "Card 4: 41 48 83 86 18 | 83 86  6 31 18  9 48 53"]
INPUT_FILE = 'scratchcards-input' 

class Card():

    def __init__(self, raw_line):
        self.raw_line = raw_line
        self.number, self.winning_numbers, self.scratch_numbers = self._parse_input(raw_line)

    def _split_raw_line(self, raw_line):
        return raw_line.split(':')
    
    def _get_raw_card_details(self, split_raw_line):
        return split_raw_line[0].strip()
    
    def _get_raw_play_numbers(self, split_raw_line):
        return split_raw_line[1].strip()
    
    def _get_start_index_of_digit(self, clean_raw_card_details):
        m = re.search(r"\d", clean_raw_card_details)
        return m.start()

    def _get_card_number(self, raw_card_details):
        clean_raw_card_details = raw_card_details.strip()
        digit_start_index = self._get_start_index_of_digit(clean_raw_card_details)
        
        return int(clean_raw_card_details[digit_start_index:].strip())
    
    def _clean_raw_numbers(self, raw_numbers):
        clean = set()
        for n in raw_numbers:
            clean_entry = n.strip()
            if clean_entry: clean.add(int(clean_entry))
        
        return clean
            
    def _get_winning_numbers(self, raw_play_numbers):
        raw_winning_numbers = raw_play_numbers.split('|')[0]
        winning_numbers = raw_winning_numbers.split(' ')
        return self._clean_raw_numbers(winning_numbers)
    
    def _get_scratch_numbers(self, raw_play_numbers):
        raw_scratch_numbers = raw_play_numbers.split('|')[1]
        scratch_numbers = raw_scratch_numbers.split(' ')
        return self._clean_raw_numbers(scratch_numbers)

    def _parse_input(self, raw_line):
        '''
        Parse input
            a. Split on ':' 
                Left part into 'raw_card_details' = 'Card <card number>'
                Right part into 'raw_play_numbers' = '<winning numbers> | <scratch numbers>'
            b. Assign Card attributes
                Don't forget to strip from spaces
                a. Split raw_card_details on ' ' and add right part as 'number' to Card attribute
                b. Split raw_play_numbers on '|'
                    a. split left part on ' ' and set to the 'winning_numbers' attribute (as set)
                    b. split right part on ' ' and set to 'scratch_numbers' attribute (as set)
        '''
        split_raw_line = self._split_raw_line(raw_line)
        raw_card_details = self._get_raw_card_details(split_raw_line)
        raw_play_numbers = self._get_raw_play_numbers(split_raw_line)
        card_number = self._get_card_number(raw_card_details)
        winning_numbers = self._get_winning_numbers(raw_play_numbers)
        scratch_numbers = self._get_scratch_numbers(raw_play_numbers)

        return card_number, winning_numbers, scratch_numbers
    
    def _get_cardinality_of(self, intersection):
        return len(intersection)

    def _get_winning_and_scratch_number_intersection(self):
        return self.winning_numbers.intersection(self.scratch_numbers)

    def get_number_of_matches(self):
        ''' Count cardinality of scratch_numbers.intersection(winning_numbers) '''
        intersection = self._get_winning_and_scratch_number_intersection()
        return self._get_cardinality_of(intersection)
    
    def get_points(self):
        number_of_matches = self.get_number_of_matches()
        if number_of_matches == 0: 
            return 0
        else:
            return 2**(number_of_matches-1)
        
    def register_successors(self, cards):
        number_of_matches = self.get_number_of_matches()
        next_card_index = self.number # Number 1 in index 0, so successor in index 1 = self.number
        last_card_index = self.number + number_of_matches
        self.successors = cards[next_card_index:last_card_index]

    def register_number_of_cards_won(self):
        ''' While there are successors, recursively look through the successors of each successor and count the number of cards won '''
        number_of_cards_won, successors = 0, [self]
        while successors:
            current_card = successors.pop()
            successors.extend(current_card.successors)
            number_of_cards_won += 1

        self.number_of_cards_won = number_of_cards_won


def read_file(path=INPUT_FILE):
    lines = []
    raw_lines = []
    with open(path) as f:
        raw_lines = f.readlines()
    for raw_line in raw_lines:
        line = raw_line.replace('\n', '').strip()
        lines.append(line)

    return lines

def get_cards(raw_lines):
    return [Card(raw_line) for raw_line in raw_lines]

def calculate_sum(cards):
    sum = 0
    for card in cards:
        sum += card.get_points()

    return sum

def register_successors(cards):
    for card in cards:
        card.register_successors(cards)

def register_number_of_cards_won(cards):
    for card in cards:
        card.register_number_of_cards_won()

def get_sum(cards):
    sum = 0
    for card in cards:
        sum += card.number_of_cards_won

    return sum

if __name__ == '__main__':
    #lines = TEST_CASES
    lines = read_file()
    cards = get_cards(lines)
    register_successors(cards)
    register_number_of_cards_won(cards)
    sum = get_sum(cards)
    print(sum) # Correct answer 5095824
