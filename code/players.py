# imports
import card, deck, numpy, random
from datetime import date

"""
-----------------------------------------------------------------------------------
-- Description: The CP class represents a computer player for the 'Go Fish' game. -
---- Each computer player (CP) has its own probabilities for remembering guessed  -
---- cards earlier in the game. The HP class represents a human player (the user) -
---- for the 'Go Fish' game, of which there can be several. Both classes inherit  -
---- from the Player class, which provides the base functionality that is common  -
---- between both human and computer players.                                     -
-- Author: Amber Melton -----------------------------------------------------------
-- Create Date: July 16, 2023 -----------------------------------------------------
-----------------------------------------------------------------------------------
"""

# defines a go-fish player, and the base functionality associated with one.
class Player():
    
    # creates a new player instance
    def __init__(self):
        self.hand = []
        self.sets = []

    # getter for the computer player's current hand
    def get_hand(self):
        return self.hand
    
    # gets the names of cards in the computer players current hand
    def get_hand_names(self):
        result = []
        for c in self.hand:
            result.append(c.name)

        return result

    # gets the values of cards in the computer players current hand
    def get_hand_values(self):
        result = []
        for c in self.hand:
            result.append(c.value)

        return result

    # getter for the computer player's current sets
    def get_sets(self):
        return self.sets
        result = []
        for s in self.sets:
            result.append(s.name)

        return result

    # checks how many cards the computer player has in-hand that have the same value as the given card
    # returns a list of the cards that match
    def card_count(self, card_to_check: card.Card):
        cards = []

        for c in self.hand:
            if c.value == card_to_check.value:
                cards.append(c)

        return cards
    
    # checks how many cards the computer player has in-hand that have the given value
    # returns a list of the cards that match
    def card_count(self, value_to_check: str):
        cards = []

        for c in self.hand:
            if c.value == value_to_check:
                cards.append(c)

        return cards
    
    # adds the given card to the computer player's hand
    def add_to_hand(self, card_to_add: card.Card):
        self.hand.append(card_to_add)
        # checks for set (if has a set, adds to sets (and removes from hand))
        self.check_for_set(card_to_add.value)

    # removes any cards from the computer player's hand that match the given card's value
    def remove_from_hand(self, card_to_take: card.Card):
        index = 0
        remove_from = []

        for c in self.hand:
            if c.value == card_to_take.value:
                remove_from.append(index)
            index += 1
        
        remove_from.reverse()
        for i in remove_from:
            self.hand.pop(i)

    # removes any cards from the computer player's hand that match the given cards value
    def remove_from_hand(self, value_to_take: str):
        index = 0
        remove_from = []

        for c in self.hand:
            if c.value == value_to_take:
                remove_from.append(index)
            index += 1
        
        remove_from.reverse()
        for i in remove_from:
            self.hand.pop(i)

    # resets the computer player's hand, sets, etc.
    def reset(self):
        self.hand = []
        self.sets = []

    # checks whether a set exists for the given value, and forms one accordingly if so.
    def check_for_set(self, card_value):
        count = 0
        indexes = []

        for i in range(0, len(self.hand)):
            if self.hand[i].value == card_value:
                count += 1
                indexes.append(i)
        
        # if a set exists, add it to sets and remove from hand (otherwise does nothing)
        if count == 4:
            # add value to sets
            self.sets.append(card_value)
            # remove cards from hand
            indexes.reverse()
            for i in indexes:
                self.hand.pop(i)
            return True # returns true if a set was formed
        return False # returns false if no set was formed

# defines a "human player" and tracks the human players that exist
class HP(Player):
    
    players = []
    player_names = []

    # creates a new human player (HP) instance, which stores the player's current stats, hand, etc.
    def __init__(self, name):
        if self.player_names.__contains__(name):
            raise Exception("There is already a player by this name.")
        else:
            self.player_names.append(name)
            self.players.append(self)

        super().__init__()

        self.name = name
        self.wins = 0
        self.losses = 0
        self.create_date = date.today()

    # changes the current player's name, so long as the new name isn't one of an existing player
    def change_name(self, new_name):
        if self.player_names.__contains__(new_name):
            raise Exception("There is already a player by this name.")

        self.name = new_name

    # resets the player's hand, sets, etc.
    def game_reset(self):
        self.hand = []
        self.sets = []
    
    # resets the player's stats entirely
    def reset(self):
        self.wins = 0
        self.losses = 0
        self.hand = []
        self.sets = []

# defines a "computer player" and adds functionality for generating guesses, etc.
class CP(Player):

    # creates a new CP (computer player) object with the given base probability and degradation factor.
    #   - base probability = the likelihood that the CP will remember the last HP (human player) guess/ask.
    #   - degredation factor = the factor by which the probability of "remembering" decreases for every card guessed.
    def __init__(self, base_prob, degradation_factor):
        super().__init__()
        self.remembrance_factors = [base_prob]
        self.log = []
        self.guess_log = {}

        for i in range(1, 10):
            self.remembrance_factors.append(self.remembrance_factors[i - 1]/degradation_factor)

    # randomly selects a card from the current hand
    def select_from_hand(self):
        # determines size of hand
        size = len(self.hand)
        # randomly pick a card from the hand
        index = random.randrange(0, size)
        # returns the selected card
        return self.hand[index].value

    # attempts to make a guess for go-fish
    def make_guess(self):
        # first checks whether any cards in the current hand exist in the log of player guesses
        log_matches = []
        for c in self.hand:
            if self.log.__contains__(c.value):
                log_matches.append(c.value)
        
        # if it does, tries to remember the first one
        remembers = 0

        while(len(log_matches) > 0 and remembers == 0):
            value = log_matches[0]
            # finds the remembrance factor for the guess
            factor = self.remembrance_factors[self.log.index(value)]

            # attempt to "remember"
            remembers = numpy.random.choice(2,1, p = [(1-factor), factor]) # 0 = failed to remember. 1 = remembered.
            if remembers == 1:
                # if remembered, check if we've already asked for and gotten it
                # check if we've previously asked for it
                if self.guess_log.keys.__contains__(value):
                    # check if we remember it
                    remembers = numpy.random.choice(2,1, p = [(1-factor), factor]) # 0 = failed to remember. 1 = remembered.
                    if remembers == 1: # if we remember it, did we get it or not?
                        # if we already got it, go for something else
                        if self.guess_log[value]:
                            # remove from log_matches (and continue looping)
                            log_matches.pop(0)
                        else: # if we didn't get it, go ahead and ask
                            return value
                    else: # we don't remember that we've guessed it, so we just ask!
                        return value
                
                else: # we haven't previously guessed it, so go ahead!
                    return value

            else: # if didn't remember, remove from log_matches (and check other matches if there are any; via current loop)
                log_matches.pop(0)

        #if exited loop without guessing, make a random guess from hand
        return self.select_from_hand()
    
    # logs the given card value as a guess by the player
    def log_player_guess(self, card_value):
        self.log.insert(0, card_value)
        # if there are now more than 10 items in the log, remove the last one
        if len(self.log) > 10:
            self.log.pop()

    # logs the given card value and result of a guess asked by the computer player
    def log_computer_guess(self, card_value, received):
        self.guess_log[card_value] = received
        # if there are now more than 10 keys in the dictionary, remove the first (oldest) one
        if len(self.guess_log.keys()) > 10:
            # identify the first key 
            first = None
            for k in self.guess_log.keys():
                first = k
                break

            # now remove it
            self.guess_log.pop(first)

    # resets the computer player's hand, sets, etc.
    def reset(self):
        self.hand = []
        self.sets = []
        self.log = []
        self.guess_log = {}