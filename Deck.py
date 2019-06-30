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
		self.values = [ "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K" ]
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

	# checks for specific hands in poker
	def checkHand( self, hand ):
		if self.__royalFlush( hand ):
			return "Royal Flush!"
		elif self.__straight( hand ):
			return "Straight!"
		else:
			return "Failed to identify a hand!!"

	# these private functions return true or false
	def __royalFlush( self, hand ):
		# check for royal flush
		suit = hand[0][-1]
		t = False
		j = False
		q = False
		k = False
		a = False
		for card in hand:
			if suit not in card:
				return False
			if "10" in card:
				t = True
			if "J" in card:
				j = True
			if "Q" in card:
				q = True
			if "K" in card:
				k = True
			if "A" in card:
				a = True
		# if we get here, it's at least all the same suit
		if t and j and q and k and a:
			return True
		else:
			return False

	def __straight( self, hand ):
		# get a list of numbers
		nums = []
		for card in hand:
			if "10" in card:
				nums.append( 10 )
			elif "J" in card:
				nums.append( 11 )
			elif "Q" in card:
				nums.append( 12 )
			elif "K" in card:
				nums.append( 13 )
			elif "A" in card:
				nums.append( 1 )
				nums.append( 14 )
			else:
				nums.append( ord( card[:1] ) - 48 )
		nums.sort()
		# now we have a sorted list on ints denoting face values
		if nums[0] is 1 and nums[1] is 2 and nums[2] is 3 and nums[3] is 4 and nums[4] is 5:
			return True
		elif nums[0] is 1:
			while 1 in nums:
				nums.remove( 1 )
		inarow = 0
		last = 0
		for value in nums:
			print( "last =  " + str( last ) )
			print( "value = " + str( value ) )
			# dont forget that Ace is counted twice....
			if last == (value -1):
				inarow = inarow + 1
			print( inarow )
			last = value

		# now just check if we had 5 in a row
		if inarow >= 4:
			return True
		else:
			return False
