
import operator

INPUT_FILE = 'camel-cards-input'
TEST_INPUT = 'test-input'

class Hand:

    POSSIBLE_CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    
    def __init__(self, cards, bid):
        assert len(cards) == 5
        assert type(cards) == list
        self.cards = cards
        self.card_rank = self._get_card_rank()
        self.count_per_card = self._get_count_per_card()
        self.card_count = self._get_card_count()
        self.type = self._get_type()
        self.rank = self._get_hand_rank()
        self.strength = self._get_hand_strength()
        self.bid = int(bid)
        self.order = self.rank, self.strength

    def _get_card_count(self):
        card_count = []
        for key in self.count_per_card.keys():
            card_count.append(self.count_per_card[key])
        
        return card_count

    def _get_card_rank(self):
        card_rank = {}
        for rank, card in enumerate(reversed(self.POSSIBLE_CARDS)):
            card_rank.update({card: rank})

        return card_rank

    def _is_five_of_a_kind(self):
        return self.card_count.count(5) == 1

    def _is_four_of_a_kind(self):
        return self.card_count.count(4) == 1

    def _is_full_house(self):
        return self.card_count.count(2) == 1 and self.card_count.count(3) == 1

    def _is_three_of_a_kind(self):
        return self.card_count.count(3) == 1

    def _is_two_pairs(self):
        return self.card_count.count(2) == 2

    def _is_pair(self):
        return self.card_count.count(2) == 1

    def _is_high_card(self):
        ''' If the length of the set of cards is as long as the total number of cards it is only containing uniques '''
        return self.card_count.count(1) == 5

    def _get_type(self):
        if self._is_five_of_a_kind():
            return 'Five of a kind'
        elif self._is_four_of_a_kind():
            return 'Four of a kind'
        elif self._is_full_house():
            return 'Full house'
        elif self._is_three_of_a_kind():
            return 'Three of a kind'
        elif self._is_two_pairs():
            return 'Two pairs'
        elif self._is_pair():
            return 'Pair'
        elif self._is_high_card():
            return 'High card'

    def _get_count_per_card(self):
        count_per_card = {}
        for card in self.POSSIBLE_CARDS:
            count = self.cards.count(card)
            if count != 0: count_per_card.update({card: count})
        
        return count_per_card
    
    def has_stronger_hand_than(self, other_hand):
        ''' A stronger hand has a higher card (in order) '''
        for this_hand_card, other_hand_card in zip(self.cards, other_hand.cards):
            this_hand_card_rank = self.card_rank[this_hand_card]
            other_hand_card_rank = self.card_rank[other_hand_card]
            if this_hand_card_rank == other_hand_card_rank:
                continue
            elif this_hand_card_rank > other_hand_card_rank:
                return True
            elif this_hand_card_rank < other_hand_card_rank:
                return False

    def _get_hand_rank(self):
        if self._is_five_of_a_kind():
            return 6
        elif self._is_four_of_a_kind():
            return 5
        elif self._is_full_house():
            return 4
        elif self._is_three_of_a_kind():
            return 3
        elif self._is_two_pairs():
            return 2
        elif self._is_pair():
            return 1
        elif self._is_high_card():
            return 0
        
    def _get_hand_strength(self):
        ranks = [int(self.card_rank[card]) for card in self.cards]
        return tuple(ranks)

    def has_higher_rank_than(self, other_hand):
        if self.rank > other_hand.rank:
            return True
        elif self.rank == other_hand.rank:
            return False
        elif self.rank < other_hand.rank:
            return False

    def is_better_hand_than(self, other_hand):
        ''' Better is defined as having higher rank or higher strength '''
        if self.rank > other_hand.rank:
            return True
        elif self.rank == other_hand.rank and self.has_stronger_hand_than(other_hand):
                return True
        elif self.rank < other_hand.rank:
            return False

def _read_file(path):
    with open(path) as f:
        lines = f.readlines()
    return lines

def _parse(lines):
    contents = []
    for line in lines:
        cards = []
        [hand, bid] = line.replace('\n', '').strip().split(' ')
        for card in hand:
            cards.append(card)
        content = {
            'cards': cards, 
            'bid' : bid
            }
        contents.append(content)

    return contents

def get_hands(contents):
    hands = []
    for content in contents:
        hands.append(Hand(content["cards"], content["bid"]))

    return hands

def get_sorted_hands(hands):
    keyfun= operator.attrgetter("order")
    return sorted(hands, key=keyfun)

def get_total_winnings(sorted_hands):
    total_winnings = 0
    for rank, hand in enumerate(sorted_hands):
        factor = rank+1
        total_winnings += factor * hand.bid

    return total_winnings

def main():
    lines = _read_file(INPUT_FILE)
    contents = _parse(lines)
    hands = get_hands(contents)
    sorted_hands = get_sorted_hands(hands)
    total_winnings = get_total_winnings(sorted_hands)

    print(total_winnings) # correct answer 250232501

if __name__ == '__main__':
    main()