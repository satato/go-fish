import card
import random

class Deck():
    types = ["Hearts", "Spades", "Diamonds", "Clubs"]
    values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    # initializes the 52 cards that make up a deck,
    # and stores them in a list as this Deck instance's 'cards' attribute
    def __init__(self):
        self.cards = []
        # initializes the 52 cards that make up the deck (one of every value + type combination)
        for v in self.values:
            for t in self.types:
                self.cards.append(card.Card(t, v))

    # shuffles the current deck of cards
    def shuffle(self):
        random.shuffle(self.cards)

    # prints out the names (in the order they are in the deck, from bottom to top) of each card in the deck
    def print_cards(self):
        for c in self.cards:
            print(c.name)

    # draws a card from the current deck, and updates it accordingly
    def draw(self):
        # checks that there are cards to draw
        if len(self.cards) > 0:
            # takes the last card off the list and returns it
            return self.cards.pop()
