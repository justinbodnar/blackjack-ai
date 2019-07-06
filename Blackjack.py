# blackjack.py
# an implementation of the classic card game using justinbodnar/Deck.py

from Deck import Deck
import random as rand
import tensorflow as tf
import keras
import numpy as np

# instantiate deck of cards
global deck
deck = Deck()

# function to count the value of a hand
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
# level 1: only gather data about the players cards
# level 2: gather level 1 AND the dealers face up card
# level 3: gather level 2 AND the history of which cards have been seen
def hand( montecarlo, level, debug ):

	# these lists are for collecting data
	data = []
	tags = []

	if level < 3:
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
			choice = rand.choice( ["h","s"] )
#			choice = "h"
		else:
			print( "Hit or stay? (Enter 'h' or 's'): " )
			choice = raw_input()

		# if hitting
		if choice is "h":
			# add data
			if level is 1:
				data = data + [ hand_value( players_hand ) ]
			elif level is 2:
				data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
			elif level is 3:
				 data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] + deck.negation() ]
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
			if level is 1:
				data = data + [ hand_value( players_hand ) ]
			elif level is 2:
				data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
			elif level is 3:
				 data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] + deck.negation() ]
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

####################################
# function for testing an AI model #
####################################
# takes as input a model name string, a number of games to preform,
# a boolean where True implies we use a fresh deck for each hand,
# an integer representing which level we should be testing at,
# and a boolean for debugging/verbosity
# prints win/loss ratio
def test_model( model_name, num_of_tests, fresh_deck, level, debug ):

	# statistics
	wins = 0
	losses = 0
	ties = 0

	# deserialize model
	json_file = open('models/'+model_name+'.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	model = keras.models.model_from_json( loaded_model_json, custom_objects={"GlorotUniform": tf.keras.initializers.glorot_uniform} )
	model.load_weights( "models/"+model_name+".h5" )
	print( "Model " + model_name + " loaded from disk" )

	# get deck ready
	deck = Deck()

	# random choices
	choices = [ 'h', 's' ]

	# loop through the number of tests parameter
	for i in range( num_of_tests ):

		# prepare data for eventual input to model
		data = []

		# check if we need to shuffle
		if fresh_deck or deck.cardinality() < 15:
			deck.shuffle()

		# instantiate two empty hands
		dealers_hand = [ ]
		ais_hand = [ ]

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
			ties = ties + 1
			continue
		elif summ is 21 and hand_value( dealers_hand ) is not 21:
			if debug:
				print( "BlackJack!" )
				print( "PLAYER WINS" )
			wins = wins + 1
			continue
		elif summ > 21:
			if debug:
				print( "Bust." )
				print( "PLAYER LOSES" )
			losses = losses + 1
			continue
		else:
			players_summ = summ

		# hit up to 5 times
		for j in range(5):

			# add data
			if level is 1:
				data = [ hand_value( players_hand ) ]
			elif level is 2:
				data = [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
			elif level is 3:
				 data = [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] + deck.negation() ]


			prediction = model.predict( np.array( data ) )
			if prediction[0][0] > prediction[0][1]:
				choice = "s"
			else:
				choice = "h"

			# temp code to generate random choice
#			choice = rand.choice( [ 'h', 's' ] )
#			choice = "s"

			#print( i, choice )

			# if hitting
			if choice is "h":

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
					if debug:
						print( "Bust." )
						print( "PLAYER LOSES" )
					losses = losses + 1
					continue
				elif summ is 21:
					# add tag
					if debug:
						print( "21" )
					wins = wins + 1
					continue
				else:
					# add tag
					players_summ = summ

			# if staying
			else:
				# add data
				if level is 1:
					data = [ hand_value( players_hand ) ]
				elif level is 2:
					data = [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
				elif level is 3:
					 data = [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] + deck.negation() ]
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
					if debug:
						dealers_hand_str = ""
						for card in dealers_hand:
							dealers_hand_str = dealers_hand_str + card + "   "
						print( "Dealer: " + dealers_hand_str )
						print( "Player: " + players_hand_str )
						print( "Dealer busts." )
						print( "PLAYER WINS" )
					wins = wins + 1
				elif summ is 21:
					# add tag
					if debug:
						dealers_hand_str = ""
						for card in dealers_hand:
							dealers_hand_str = dealers_hand_str + card + "   "
						print( "Dealer: " +  dealers_hand_str )
						print( "Player: " + players_hand_str )
						print( "Dealer has 21." ) 
						print( "PLAYER LOSES" )
					losses = losses + 1
				else:
					if debug:
						dealers_hand_str = ""	
						for card in dealers_hand:	
							dealers_hand_str = dealers_hand_str + card + "   "
						print( "Dealer: " + dealers_hand_str )
						print( "Player: " + players_hand_str )
					if summ > players_summ:
						# add tag
						if debug:
							print( "PLAYER LOSES" )
						losses = losses + 1
					else:
						# add tag
						if debug:
							print( "PLAYER WINS" )
						wins = wins + 1
	# return stats
	return float(wins), float(losses), float(ties)

# function to add some number of
# data points to the blackjack data set
def gen_data_set( num_of_games, name, level, shuffle ):
	# loop through simulations
	for i in range( num_of_games ):
		print( i )
		try:
			data, tags = hand( True, level,  False )

			if len(data) < len(tags) or len(data) > len(tags):
				print( "ERROR" )
				print( data )
				print( tags )



			dataf = open( "data_sets/" + str(name) + ".data", "a" )
			tagf = open( "data_sets/" + str(name) + ".tags", "a" )
			for datum in data:
				dataf.write( str( datum ) + "\n" )
			for tag in tags:
				tagf.write( tag  + "\n" )
			dataf.close()
			tagf.close()
			# check if we need to reshuffle the deck
			# only needed for data set level 3
#			print( deck.cardinality() )
			if shuffle:
				deck.shuffle()
		except Exception as e:
			print( e )
			deck.shuffle()
