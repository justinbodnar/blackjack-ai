# blackjack.py
# an implementation of the classic card game using justinbodnar/Deck.py

from Deck import Deck
import random as rand

# instantiate deck of cards
deck = Deck()

# function to count the value of a given hand
# 'player' param is 1 for player, 2 for dealer
def hand_value( hand ):

	summ = 0

	for card in hand:
		# grab first character of the card
		card1 = int( card[:card.index('-')] )
		# deal with the face card
		if card1 > 10:
			card1 = 10
		summ = summ + card1

	return summ

############################
# function for single hand #
############################
def hand( montecarlo, debug ):

	# these lists are for collecting data
	data = []
	tags = []

	# get cards ready
	deck.shuffle()

	# instantiate two empty hands
	dealers_hand = [ ]
	players_hand = [ ]

	# this is for monte carlo simulations
	choices = [ 'h', 's' ]

	# deal the cards
	# players get two cards face-up
	# dealer gets one face-up, one face-down
	dealers_hand = [ deck.deal(), deck.deal() ]
	players_hand = [ deck.deal(), deck.deal() ]

	# print current game
	if debug:
		print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
		print( "Player: " + players_hand[0] + "   " + players_hand[1] )

	# check for win/loss
	summ = hand_value( players_hand )
	if summ is 21 and hand_value( dealers_hand ) is 21:
		if debug:
			print( "21 each." )
			print( "TIE" )
		return data, tags
	elif summ is 21 and hand_value( dealers_hand ) is not 21:
		if debug:
			print( "BlackJack!" )
			print( "PLAYER WINS" )
		return data, tags
	elif summ > 21:
		if debug:
			print( "Bust." )
			print( "PLAYER LOSES" )
		return data, tags
	else:
		players_summ = summ

	# hit up to 5 times
	for i in range(5):
		#  hit or stay?
		if montecarlo:
			choice = choices[rand.randint(0,1)]
#			choice = "h"
		else:
			print( "Hit or stay? (Enter 'h' or 's'): " )
			choice = raw_input()

		# if hitting
		if choice is "h":
			# add data
			data = data + [ hand_value( players_hand ) ]
			# hit
			players_hand = players_hand + [ deck.deal() ]
			summ = hand_value( players_hand )
			if debug:
				print( "Hitting" )
				players_hand_str = ""
				for card in players_hand:
					players_hand_str = players_hand_str + card + "   "
				print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
				print( "Player: " + players_hand_str )
			if summ > 21:
				# add tag
				tags = tags + [ 's' ]
				if debug:
					print( "Bust." )
					print( "PLAYER LOSES" )
				return data, tags
			elif summ is 21:
				# add tag
				tags = tags + [ 'h' ]
				if debug:
					print( "21" )
				return data, tags
			else:
				# add tag
				tags = tags + [ 'h' ]
				players_summ = summ

		# if staying
		else:
			# add data
			data = data + [ hand_value( players_hand ) ]
			if debug:
				print( "Staying" )
				# print current game
				players_hand_str = ""
				for card in players_hand:
					players_hand_str = players_hand_str + card + "   "
			# check if dealer needs card
			while hand_value( dealers_hand ) < 17:
				dealers_hand = dealers_hand + [ deck.deal() ]
				if debug:
					print( "Dealer hits" )
					dealers_hand_str = ""
					for card in dealers_hand:
						dealers_hand_str = dealers_hand_str + card + "   "
					print( "Dealer: " + dealers_hand_str )
					print( "Player: " + players_hand_str )
			# check winner
			summ = hand_value( dealers_hand )
			if summ > 21:
				# add tag
				tags = tags + [ 's' ]
				if debug:
					dealers_hand_str = ""
					for card in dealers_hand:
						dealers_hand_str = dealers_hand_str + card + "   "
					print( "Dealer: " + dealers_hand_str )
					print( "Player: " + players_hand_str )
					print( "Dealer busts." )
					print( "PLAYER WINS" )
				return data, tags
			elif summ is 21:
				# add tag
				tags = tags + [ 'h' ]
				if debug:
					dealers_hand_str = ""
					for card in dealers_hand:
						dealers_hand_str = dealers_hand_str + card + "   "
					print( "Dealer: " +  dealers_hand_str )
					print( "Player: " + players_hand_str )
					print( "Dealer has 21." ) 
					print( "PLAYER LOSES" )
				return data, tags
			else:
				if debug:
					dealers_hand_str = ""
					for card in dealers_hand:
						dealers_hand_str = dealers_hand_str + card + "   "
					print( "Dealer: " + dealers_hand_str )
					print( "Player: " + players_hand_str )
				if summ > players_summ:
					# add tag
					tags = tags + [ 'h' ]
					if debug:
						print( "PLAYER LOSES" )
					return data, tags
				else:
					# add tag
					tags = tags + [ 's' ]
					if debug:
						print( "PLAYER WINS" )
					return data, tags

# loop through a thousand simulations
for i in range( 10000 ):
	print( i )
	data, tags = hand( True, False )

	print( data )
	print( tags )

	dataf = open( "data_sets/blackjack.data.1", "a" )
	tagf = open( "data_sets/blackjack.tags.1", "a" )
	for datum in data:
		dataf.write( str( datum ) + "\n" )
	for tag in tags:
		tagf.write( tag  + "\n" )
	dataf.close()
	tagf.close()
