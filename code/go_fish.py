# imports
import PySimpleGUI as sgui
import random, numpy
import card, deck, players

"""
------------------------------------------------------------------------------
-- Description: This is the main file associated with the 'Go Fish' program, -
---- which is a Python rendition of the incomplete 'Go Fish' project in Java -
---- (see: https://github.com/satato/go-fish/commits) from 2019.             -
-                                                                            -
-- Author: Amber Melton ------------------------------------------------------
-- Create Date: July 16, 2023 ------------------------------------------------
------------------------------------------------------------------------------
"""

# variables & constants
cards_per_player = 7
computer_responses = ["Aw!", "Rats, okay!", "Well shoot", "I really thought you had one", "Dang!", "Dang."]
# global variables
global game_deck
global human_player
global computer_player
global turn

# generates an appropriate base probability for the computer player, based on the provided difficulty
# difficulties are: 0 (easy), 1 (normal), and 2 (extra hard)
def generate_base_prob(difficulty):
    if difficulty == 0: # easy difficulty starts with a base prob between 50 and 80
        return 100
    elif difficulty == 1: # normal difficulty starts with a base prob between 90 and 100
        return 100
    else: # hard difficulty starts with a base prob of 100 
        return 100
    
# generates an appropriate degradation for the computer player, based on the provided difficulty
# difficulties are: 0 (easy), 1 (normal), and 2 (extra hard)
def generate_degradation_factor(difficulty):
    if difficulty == 0: # easy difficulty has a degredation factor 2 and 2.5 
        return 2
    elif difficulty == 1: # normal difficulty has a degredation factor of 2 
        return 2
    else: # hard difficulty has a degredation factor between 1.2 and 1.75
        return 2

# begins running the program (launching window, preparing visuals, etc.)
def run():

    print("==============================")
    print("beginning new game")
    print("==============================")

    new_game()

    """
    # prepare window
    sgui.theme('Blue Mono')
    layout = [  [sgui.Text('This window not yet implemented')],
                [sgui.Text('Textbox: '), sgui.InputText()],
                [sgui.Button('Ok'), sgui.Button('Cancel')] ]

    # launch the window
    window = sgui.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sgui.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel, exits the loop
            break
        print('You entered ', values[0])

    window.close() # closes the window (once the while loop is exited)
    """

# begins a new game of 'Go Fish' (clears past game and resets everything)
def new_game():
    global game_deck
    global human_player
    global computer_player
    global turn

    # initialize a new deck of cards
    game_deck = deck.Deck()
    # shuffle the new deck
    game_deck.shuffle()

    # create new players
    computer_player = players.CP(generate_base_prob(1), generate_degradation_factor(1))
    if len(players.HP.players) == 0:
        human_player = players.HP("Default Player")
    else:
        human_player = players.HP.players[0]

    player = 0
    # deal cards
    for i in range(0,(cards_per_player * 2)):
        deal = game_deck.draw()
        if player == 0:
            human_player.add_to_hand(deal)
            player = 1
        else:
            computer_player.add_to_hand(deal)
            player = 0
    
    # determine who goes first (0 = HP, 1 = CP)
    turn = random.randrange(0,1)
    # while cards remain in the deck, keep taking turns
    while len(game_deck.cards) > 0 and len(human_player.get_hand) > 0 and len(computer_player.get_hand) > 0:
        take_turn()

    # game is over!
    end_game()
    
# prints out the end message(s) for the game and calculates the winner
def end_game():
    print("Game over!")
    # calculate winner
    if len(human_player.get_sets) > len(computer_player.get_sets):
        print("You won!")
    elif len(human_player.get_sets) > len(computer_player.get_sets):
        print("Your opponent won :(")
    else:
        print("You and your opponent tied, each having " + len(human_player.get_sets) + " sets!")

# displays the user's hand and any sets that they or the computer have
def display_hand_and_sets():
    # displays the human player's hand & sets
    print("Your hand: " + ", ".join(human_player.get_hand_names()))
    print("Your sets: " + ", ".join(human_player.get_sets()))
    print("Your opponent's sets: " + ", ".join(computer_player.get_sets()))

# has either player make their turn
def take_turn():
    global turn
    display_hand_and_sets()

    if turn == 0: # if it is the human player's turn, prompt them to take it
        turn = 1
        check_hand_for_cards(human_player)
        # prompt user to go fishing
        print("-------------------------")
        print("Your turn!")
        response = input("You: Do you have any...")
        hand = human_player.get_hand_values()
        # checks whether the user has the card they asked for
        if hand.__contains__(response) or hand.__contains__(response[0:len(response) - 1]):
            if response[-1] == "s":
                response = response[0:len(response) - 1]

            # checks whether computer has any
            cards = computer_player.card_count(response)
            if len(cards) != 0:
                # the computer has the card(s), removes them
                computer_player.remove_from_hand(response)
                # and add them to the user's hand
                for c in cards:
                    human_player.add_to_hand(c)
                # turn over!
                check_hand_for_cards(computer_player)
            else:
                # computer says 'Go fish!'
                print("Opponent: Go Fish!")
                print("-------------------------")
                # user draws a card
                human_player.add_to_hand(game_deck.draw())
        else:
            print("You don't have that card! Forfeiting your turn...")
    else: # if it is the computer player's turn, prompt them to take it
        turn = 0
        check_hand_for_cards(computer_player)
        # make computer go fishing
        guess = computer_player.make_guess()
        # present computer's guess to user
        question = "Opponent: Do you have any " + guess + "s? (Y/N)"
        response = input(question)
        # check whether user has the card in question
        cards = human_player.card_count(guess)
        if len(cards) != 0:
            # if user said no, call them a liar.
            if response != "Y" and response != "y":
                print("Opponent: Liar! You have " + str(len(cards)) + "!")
            # either way, take the cards
            human_player.remove_from_hand(guess)
            # and add them to the computer's hand
            for c in cards:
                computer_player.add_to_hand(c)
            # turn over!
            check_hand_for_cards(human_player)
        else:
            # user says 'Go fish!'
            print("You: Go Fish!")
            print("Opponent: " + random.choice(computer_responses))
            print("-------------------------")
            # computer draws a card
            computer_player.add_to_hand(game_deck.draw())
        
# checks the given player's hand for cards, and makes them draw if they have none
def check_hand_for_cards(player: players.Player):
    if len(player.get_hand()) == 0: # if the player has no cards, draws one (otherwise does nothing)
            player.add_to_hand(game_deck.draw())
    
# program starts via run
run()