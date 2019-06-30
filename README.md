# card-games
A collection of Python classes and scripts for using card games in Monte Carlo simulations and Machine Learning.

# blackjack.py
Blackjack.py is an implementation of the classic card game using the Deck class, and played from the terminal. This script is used to generate data about hands of blackjack via Monte Carlo simulations. This is done by generating random hands and storing representations of the hands, tagged with the eventual outcome of the decision.

# representing a hand of blackjack

For the purpose of training a nuerel network to play blackjack, we want to represent a hand in a way that tells us whether we should 'hit' or 'stay.' Luckily we only need to know the value of the hand, so we represent each scenario as a single integer, ie. a hand of ( 2-s, 10-h ) will be 12. We then tag the data as either 'h' or 's' for 'hit' or 'stay.'

How we determine whether the hand warrants a 'h' or 's' is a matter of opinion. The current iteration will simply append in the following manner:

<pre>
if user hits and busts:
	tag = 's'
elif user hits and doesn't bust:
	tag = 'h'
elif user stays and wins hand:
	tag = 's'
elif user stays and loses hand:
	tag = 'h'
</pre>

Example scenarios and expected data:

<pre>
Example 1

player hand: ( 3-s, 4-c )
player hits
player hand: ( 3-s, 4-c, 12-d )
player stays
dealer busts

generated data and tags:
(because we won the game, we assume every move was a good move)
7,  h # hit on 7
19, s # stay on 19

Example 2

player hand: ( 2-d, 10-c )
player hits
player hand: ( 2-d, 10-c, 2-s )
player hits
player hand: ( 2-d, 10-c, 2-s, 9-c )
player busts

generated data and tag

12, h
14, s
</pre>

# first Blackjack model

The first model was trained on 3,959 monte carlo simulations, and has a 70% accuracy rate. The serialized model can be found in the /models/ directory as blackjackmodel.h5 and blackjackmodel.json.

The model was a dense 2-layer neurel network. The first layer contained 4096 neurons, while the second only had two, for 'hit' or 'stay.' The 'adam' optimizer was used, with a loss of 'sparse_categorical_crossentropy.' Training and testing data was split 50/50 randomly. There were 10 epochs.

To find a heuristic, hand values from 2-21 were tested on the classifier.

<pre>
0
hit
1
hit
2
hit
3
hit
4
hit
5
hit
6
hit
7
hit
8
hit
9
hit
10
hit
11
hit
12
hit
13
hit
14
hit
15
hit
16
hit
17
stay
18
stay
19
stay
20
stay
</pre>

The model learned to hit on any hand value below 17. This happens to be the strategy used by the dealer.

Future data sets and models will focus learning more about the hand, ie. dealers cards, counting how many times a player has hit, etc. The longer term goal is to teach a model to count cards.

# second Blackjack model

This model will use all the previous techniques, but the data set will now include the dealer's upward facing card.

So where previously we used the single integer for data, we will now use a tuple of players_hand, and dealers_hand respectively.

Example

[ 18, 13, s ]

The data set consists of 5,323 entries, located in data_sets/blackjack.data.2 and data_sets/blackjack.tags.2.. The neural network used a similar layer scheme as the previous, with an 8-neuron second layer. The optimizer was 'nadam,' and there were 100 epochs.

The model has an accuracy of 0.74. A slightly better accuracy than model #1.

I found this nifty chart for Blackjack strategy at https://wizardofodds.com/games/blackjack/strategy/calculator/ . This will be compared to the results of the classifier

from wizardofodds.com
![Basic Blackjack Strategy](https://raw.githubusercontent.com/justinbodnar/artificial-intelligence-in-card-games/master/docs/blackjack_odds.png)

from Blackjack model #2
![Blackjack classifier results](https://raw.githubusercontent.com/justinbodnar/artificial-intelligence-in-card-games/master/docs/blackjack_odds_mine.png)

There is a clear pattern on both. This confirms the neural network has begun to learn the strategy of Blackjack.


# Deck.py
Deck.py is a class for a deck of cards. An instance of this class holds an array of 52 strings representing cards. Card strings consist of the face value and a suit seperated by a hyphen. Face values { A, 2, ... Q, K } are represented as { 1, 2, ... 12, 13 }. Suits are { 's', 'd', 'c', 'h' }. Some examples of valid card strings are '1-s' for the ace of spades, '4-c' for the four of clubs, and '12-h' for the queen of hearts.

Usage:

from Deck import Deck
deck = Deck()

Functions
	
deck.shuffle()
returns the array to 52 randomly organized card strings.

deck.deal()
removes a card string from the Deck object, and returns it

deck.checkDeck()
prints the current content of the deck
