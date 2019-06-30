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
			card1 = card[:1]
			# deal with the Ace situation
			if card1 is "A":
				 
				print( "Count Ace as 1 or 11?" )
				choice = raw_input()
				if choice is "1":
					card1 = 1
				else:
					card1 = 11
			elif card1 is "1" or card1 is "J" or card1 is "Q" or card1 is "K":
				card1 = 10
			else: card1 = int( card1 )
			summ = summ + card1
		return summ

	# if its the dealers hand
	elif player is 2:
		aces = 0
		# loop through cards in a hand
		for card in hand:
			# grab first character of the card
			card1 = card[:1]
			# deal with the Ace situation
			if card1 is "A":
				aces = aces + 1
				continue
			elif card1 is "1" or card1 is "J" or card1 is "Q" or card1 is "K":
				card1 = 10
			else: card1 = int( card1 )
			summ = summ + card1
		# by now we may have some aces collected
		while aces > 0:
			aces = aces - 1
			# we cant go above 21
			if (summ + aces + 1) is 21:
				return 21
			elif (summ + aces + 1) > 21:
				return summ + aces
			elif (summ + 11 + aces) > 21:
				return summ + 11 + aces
			elif (summ + 11 + aces) is 21:
				return 21
			else:
				return summ + 11
		return summ
	else:
		return -1
# loop through rounds
while True:

	# this is the data we need
	# the data array holds 3 pieces of info:
	# the value of the current hand, whether it was hit/stay
	# the outcome as 'w' or 'l'
	data = []

	choices = [ "hit", "stay" ]

	flag = False

	# empty all hands to deck
	deck.shuffle()
	dealers_hand = [ ]
	players_hand = [ ]


	# deal the cards
	# players get two cards face-up
	# dealer gets one face-up, one face-down
	dealers_hand = [ deck.deal(), deck.deal() ]
	players_hand = [ deck.deal(), deck.deal() ]

	# add first datum
	data = data + [ str( hand_value( players_hand, 1 ) ) ]

	# print current game
	print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
	print
	print( "Player: " + players_hand[0] + "   " + players_hand[1] )
	print
	summ = hand_value( players_hand, 1 )
	if summ is 21 and hand_value( dealers_hand, 2 ) is 21:
		print( "21 each." )
		print( "TIED GAME" )
		# add 'w' to data
		data = data + [ 'w' ]
		continue
	elif summ is 21 and hand_value( dealers_hand, 2 ) is not 21:
		print( "BlackJack!" )
		print( "PLAYER WINS" )
		# add 'w' to data
		data = data + [ 'w' ]
	elif summ > 21:
		print( "Bust." )
		print( "PLAYER LOSES" )
		# add 'l' to data
		data = data + [ 'l' ]
		continue
	else:
		players_summ = summ

	i = 0
	while i < 5:
		i = i + 1
		if flag:
			break
		#  hit or stay?
		print( "Hit or stay? (Enter 'h' or 's'): " )
		choice = raw_input()
	
		if choice is "h":
			# hit
			print( "Hitting" )
			# add 'h' to data
			data = data + [ 'h' ]
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
#			print( "Dealer's count: " + str( hand_value( dealers_hand, 2 ) ) )
#			print( "Player's count: " + str( hand_value( players_hand, 1 ) ) )
			summ = hand_value( players_hand, 1 )
			if summ > 21:
				print( "Bust." )
				print( "PLAYER LOSES" )
				# add 'l' to data
				data = data + [ 'l' ]
				pause = raw_input( "Press Enter to continue:" )
				flag = True
			elif summ is 21:
				print( "21" )
				# add 'w' to data
				data = data + [ 'w' ]
				pause = raw_input( "Press Enter to continue:" )
				flag = True
			else:
				players_summ = summ

		else:
			# stay
			print( "Staying" )
			# add 's' to data
			data = data + [ 's' ]
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
				pause = raw_input( "Press Enter to continue: " )
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
				# add 'w' to data
				data = data + [ 'w' ]
				print
				pause = raw_input( "Press Enter to continue: " )
			elif summ is 21:
				dealers_hand_str = ""
				for card in dealers_hand:
					dealers_hand_str = dealers_hand_str + card + "   "
				print( "Dealer: " +  dealers_hand_str )
				print( "Player: " + players_hand_str )
				print( "Dealer has 21." ) 
				print( "PLAYER LOSES" )
				print
				# add 'l' to data
				data = data + [ 'l' ]
				pause = raw_input( "Press Enter to continue: " )
			else:
				dealers_hand_str = ""
				for card in dealers_hand:
					dealers_hand_str = dealers_hand_str + card + "   "
				print( "Dealer: " + dealers_hand_str )
				print( "Player: " + players_hand_str )
				if summ > players_summ:
					print( "PLAYER LOSES" )
					# add 'l' to data
					data = data + 'l'
					pause = raw_input( "Press Enter to continue: " )
				else:
					print( "PLAYER WINS" )
					# add 'w' to data
					data = data + [ 'w' ]
					pause = raw_input( "Press Enter to continue: " )			
			flag = True
	print( data )
