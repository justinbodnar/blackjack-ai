import random
class Deck:

	# shuffles the deck randomly
	def shuffle( self ):
		self.cards= []
		self.negated = []
		for suit in self.suits:
			for value in self.values:
				self.cards.append( value+"-"+suit )
		self.tempCards = [ ]
		for i in range(len(self.cards)):
			element = random.choice( self.cards )
			self.tempCards.append( element )
			self.cards.remove( element )
		self.cards = self.tempCards

	# constructor function
	def __init__( self ):
		self.cards = []
		self.negated = []
		self.suits = [ "c", "s", "d", "h" ]
		self.values = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13" ]
		self.shuffle()

	# returns number of cards
	def cardinality( self ):
		return len( self.cards )

	# this is to test the class
	def checkDeck( self ):
		for card in self.cards:
			print( card )
		print( len( self.cards ) )

	# return the negated deck
	# as in, all cards removed so far
	# used in data set level 3
	def negation( self ):
		final = []
		# pad the final list
		for i in range( 52 ):
			final.append( 0 )
		# now fill in the proper order
		for card in self.negated:
			value = int( card.split('-')[0] )
			# find the right place in the list
			# the first index for any value is 4 * (value-1)
			index = 4 * ( value - 1 )
			# is this the first, second, third or fourth instance of this card?
			if final[ index ] is 0:
				final[ index ] = 1
			elif final[ index+1 ] is 0:
				final[ index+1 ] = 1
			elif final[ index+2 ] is 0:
				final[ index+2 ] = 1
			else:
				final[ index+3 ] = 1
		return final

	# deals a single card, removing it from the deck
	# returns a string
	def deal( self ):
		element = random.choice( self.cards )
		self.cards.remove( element )
		self.negated.append( element )
		return element

