# blackjack.py
# an implementation of the classic card game using justinbodnar/Deck.py

from Deck import Deck

# instantiate deck of cards
deck = Deck()

# function to count the value of a given hand
# 'player' param is 1 for player, 2 for dealer
def hand_value( hand, player ):

	players_summ = 0
	summ = 0

	# if its a players hand
	if player is 1:
		# loop through cards in a hand
		for card in hand:
			# grab first character of the card
			card1 = int( card[:card.index('-')] )
			# deal with the Ace situation
			summ = summ + card1

	# if its the dealers hand
	elif player is 2:
		# loop through cards in a hand
		for card in hand:
			# grab first character of the card
			card1 = int( card[:card.index('-')] )
			summ = summ + card1

	return summ

########################################
# function for single monte carlo hand #
########################################
def rand_hand():

	# get cards ready
	deck.shuffle()

	# instantiate two empty hands
	dealers_hand = [ ]
	players_hand = [ ]


	# deal the cards
	# players get two cards face-up
	# dealer gets one face-up, one face-down
	dealers_hand = [ deck.deal(), deck.deal() ]
	players_hand = [ deck.deal(), deck.deal() ]

	# print current game
	print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
	print
	print( "Player: " + players_hand[0] + "   " + players_hand[1] )
	print

	# check for win/loss
	summ = hand_value( players_hand, 1 )
	if summ is 21 and hand_value( dealers_hand, 2 ) is 21:
		print( "21 each." )
		print( "TIED GAME" )
		return
	elif summ is 21 and hand_value( dealers_hand, 2 ) is not 21:
		print( "BlackJack!" )
		print( "PLAYER WINS" )
		return
	elif summ > 21:
		print( "Bust." )
		print( "PLAYER LOSES" )
		return
	else:
		players_summ = summ

	# hit up to 5 times
	for i in range(5):
		#  hit or stay?
		print( "Hit or stay? (Enter 'h' or 's'): " )
		choice = raw_input()

		# if hitting
		if choice is "h":
			# hit
			print( "Hitting" )
			players_hand = players_hand + [ deck.deal() ]
			# print current game
			players_hand_str = ""
			for card in players_hand:
				players_hand_str = players_hand_str + card + "   "
			print( "\n\n" )
			print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
			print
			print( "Player: " + players_hand_str )
			print
			summ = hand_value( players_hand, 1 )
			if summ > 21:
				print( "Bust." )
				print( "PLAYER LOSES" )
				return
			elif summ is 21:
				print( "21" )
				return
			else:
				players_summ = summ

		# if staying
		else:
			# stay
			print( "Staying" )
			# print current game
			players_hand_str = ""
			for card in players_hand:
				players_hand_str = players_hand_str + card + "   "
			# check if dealer needs card
			while hand_value( dealers_hand, 2 ) < 17:
				print( "Staying" )
				print
				dealers_hand = dealers_hand + [ deck.deal() ]
				print( "Dealer hits." )
				# print dealers hand
				dealers_hand_str = ""
				for card in dealers_hand:
					dealers_hand_str = dealers_hand_str + card + "   "
				print( "Dealer: " + dealers_hand_str )
				print( "Player: " + players_hand_str )
				print
			# check winner
			summ = hand_value( dealers_hand, 2 )
			if summ > 21:
				dealers_hand_str = ""
				for card in dealers_hand:
					dealers_hand_str = dealers_hand_str + card + "   "
				print( "Dealer: " + dealers_hand_str )
				print( "Player: " + players_hand_str )
				print( "Dealer busts." )
				print( "PLAYER WINS" )
				return
			elif summ is 21:
				dealers_hand_str = ""
				for card in dealers_hand:
					dealers_hand_str = dealers_hand_str + card + "   "
				print( "Dealer: " +  dealers_hand_str )
				print( "Player: " + players_hand_str )
				print( "Dealer has 21." ) 
				print( "PLAYER LOSES" )
				return
			else:
				dealers_hand_str = ""
				for card in dealers_hand:
					dealers_hand_str = dealers_hand_str + card + "   "
				print( "Dealer: " + dealers_hand_str )
				print( "Player: " + players_hand_str )
				if summ > players_summ:
					print( "PLAYER LOSES" )
					return
				else:
					print( "PLAYER WINS" )
					return

rand_hand()
