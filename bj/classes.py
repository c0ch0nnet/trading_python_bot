import random


class Card:
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    SPADES = "Spades"
    CLUBS = "Clubs"

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.points = Card.set_points(value)

    @staticmethod
    def set_points(value):
        return Deck.points[value]

    def __str__(self):  # решить через словарь
        icons = {
            "Hearts": '\u2665',
            "Diamonds": '\u2666',
            "Spades": '\u2660',
            "Clubs": '\u2663'
        }
        return f"{self.value}{icons[self.suit]}"

    def __repr__(self):
        return self.__str__()

    def equal_suit(self, other_card):
        return self.suit == other_card.suit

    def __gt__(self, other_card):
        if Deck.values.index(self.value) == Deck.values.index(other_card.value):
            return Deck.suits.index(self.suit) > Deck.suits.index(other_card.suit)
        else:
            return Deck.values.index(self.value) > Deck.values.index(other_card.value)

    def __lt__(self, other_card):
        if Deck.values.index(self.value) == Deck.values.index(other_card.value):
            return Deck.suits.index(self.suit) < Deck.suits.index(other_card.suit)
        else:
            return Deck.values.index(self.value) < Deck.values.index(other_card.value)


class Deck:

    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
    points = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

    def __init__(self):
        self.cards = []
        self.last_card_index = -1
        for suit in Deck.suits:
            for value in Deck.values:
                card = Card(value, suit)
                self.cards.append(card)

    def __str__(self):
        s = f'deck[{len(self.cards)}]'
        for card in self.cards:
            s = s + str(card) + ','
        return s

    def __iter__(self):
        self.last_card_index = -1
        return self

    def __next__(self):
        self.last_card_index += 1
        if self.last_card_index >= len(self.cards):
            raise StopIteration
        return self.cards[self.last_card_index]

    def draw(self, x):
        cards = []
        for _ in range(x):
            cards.append(self.cards.pop(0))
        return cards

    def shuffle(self):
        return random.shuffle(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def __mul__(self, num):
        while num > 1:
            deck = Deck()
            self.cards += deck.cards
            num -= 1
        return self


if __name__ == "__main__":
    deck = Deck()
    print(deck)
    deck = deck * 3
    print(deck)


