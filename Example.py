# card-games example usage

from Deck import Deck

# instantiate deck
my_deck = Deck()

# get a random card and display it
# the card is removed from the Deck object
my_card = my_deck.deal()
print( my_card )

# return all cards to the deck and 'shuffle'
my_deck.shuffle()


