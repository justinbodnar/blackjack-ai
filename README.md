# card-games
 A collection of Python classes and scripts for using card games in Monte Carlo simulations and Machine Learning.

# Deck.py
Deck.py is a class for a deck of cards. An instance of this class holds an array of 52 strings representing cards. Card strings consist of the face value and a suit seperated by a hyphen. Face values { A, 2, ... Q, K } are represented as { 1, 2, ... 12, 13 }. Suits are { 's', 'd', 'c', 'h' }. Some examples of valid card strings are '1-s' for the ace of spades, '4-c' for the four of clubs, and '12-h' for the queen of hearts.

Usage:

from Deck import Deck
deck = Deck()

Functions
	
deck.shuffle() # returns the array to 52 randomly organized card strings.

deck.deal() # removes a card string from the Deck object, and returns it

deck.checkDeck() # prints the current content of the deck


# blackjack.py
blackjack.py is an implementation of the classic card game using the Deck class, and played from the terminal.

Usage:

$ python blackjack.py


