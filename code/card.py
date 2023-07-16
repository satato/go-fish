class Card():
    types = ["Hearts", "Spades", "Diamonds", "Clubs"]
    values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    # creates a new card object with the given type and value
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.name = value + " of " + type