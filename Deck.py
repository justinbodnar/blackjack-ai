import random
class Deck:

	# shuffles the deck randomly
	def shuffle( self ):
		self.cards= []
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
		self.cards = [ ]
		self.suits = [ "c", "s", "d", "h" ]
		self.values = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13" ]
		self.shuffle()

	# this is to test the class
	def checkDeck( self ):
		for card in self.cards:
			print( card )
		print( len( self.cards ) )

	# deals a single card, removing it from the deck
	# returns a string
	def deal( self ):
		element = random.choice( self.cards )
		self.cards.remove( element )
		return element

