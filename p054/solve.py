import enum

class Rank(enum.Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

CARD_VALUES = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
ROYAL_FLUSH = CARD_VALUES[-5:]

def value_to_index(card_value):
    return CARD_VALUES.index(card_value)

class Hand:
    def __init__(self, cards):
        """
        Setup hand
        
        :param cards: List of cards, e.g. ["5H", "5C", "6S", "7S", "KD"]
        """
        self.cards = cards
        self.suits = [card[1] for card in cards]
        self.values = [card[0] for card in cards]
        self.indices = self._card_indices()
    
    def analyze(self):
        """
        Analyze hand

        Returns a dictionary:
        - suits: Dictionary of suits with a count of how many times each occurred
        - values: Dictionary of values with a count of how many times each occurred
        """
        analysis = {
            "suits": {},
            "values": {},
        }
        
        for suit in self.suits:
            analysis["suits"][suit] = analysis["suits"].get(suit, 0) + 1
        for value in self.values:
            analysis["values"][value] = analysis["values"].get(value, 0) + 1

        return analysis

    def is_consecutive(self):
        """ Return whether hand contains consecutive values """
        for i, next_i in zip(self.indices[:4], self.indices[1:]):
            if i + 1 != next_i:
                return False
        return True
    
    def rank(self):
        """
        Rank hand
        
        Returns a tuple:
        - Rank enum - e.g., Rank.STRAIGHT_FLUSH
        - Individual card values in the order required to compare ties:
          First, card values from the rank (e.g., the value for the Queen, in a pair of Queens),
          followed by the card values not used for the rank
        """
        analysis = self.analyze()
        num_suits = len(analysis["suits"])
        value_counts = list(analysis["values"].values())
        reversed_indices = self.indices[::-1]

        if num_suits == 1 and set(self.values) == set(ROYAL_FLUSH):
            return (Rank.ROYAL_FLUSH,)
        if num_suits == 1 and self.is_consecutive():
            return Rank.STRAIGHT_FLUSH, self.indices[-1]
        for card_value, count in analysis["values"].items():
            if count == 4:
                return (Rank.FOUR_OF_A_KIND, value_to_index(card_value), *reversed_indices)
        if 3 in value_counts and 2 in value_counts:
            return Rank.FULL_HOUSE, self.indices[-1], self.indices[-4]
        if num_suits == 1:
            return Rank.FLUSH, self.indices[-1]
        if self.is_consecutive():  # Hm, I think this is not working
            return Rank.STRAIGHT, self.indices[-1]
        for card_value, count in analysis["values"].items():
            if count == 3:
                return (Rank.THREE_OF_A_KIND, value_to_index(card_value), *reversed_indices)
        if value_counts.count(2) == 2:
            indices = []
            for card_value, count in analysis["values"].items():
                if count == 2:
                    indices.append(value_to_index(card_value))
            indices = list(sorted(indices))
            return (Rank.TWO_PAIRS, *indices, *reversed_indices)
        for card_value, count in analysis["values"].items():
            if count == 2:
                return (Rank.ONE_PAIR, value_to_index(card_value), *reversed_indices)
        return (Rank.HIGH_CARD, *reversed_indices)

    def _card_indices(self):
        """ Return indices of each card based on CARD_VALUES """
        indices = [value_to_index(value) for value in self.values]
        return list(sorted(indices))


def winner(player1_hand, player2_hand):
    """
    Determine winner
    """
    rank1 = player1_hand.rank()
    rank2 = player2_hand.rank()
    print(f"{rank1[0]} vs {rank2[0]}")
    if rank1[0].value > rank2[0].value:
        return 1
    if rank2[0].value > rank1[0].value:
        return 2
    for i in range(1, len(rank1)):
        if rank1[i] > rank2[i]:
            return 1
        if rank2[i] > rank1[i]:
            return 2

    assert "Tie - this should not happen"


if __name__ == "__main__":
    with open("poker.txt") as f:
        player_1_count = 0
        for line in f:
            cards = line[:-1].split(" ")
            print(f"Player 1: {cards[:5]}")
            print(f"Player 2: {cards[5:]}")
            player = winner(Hand(cards[:5]), Hand(cards[5:]))
            if player == 1:
                player_1_count += 1
            print(f"Player {player}")
        print(f"Player 1: {player_1_count}")
