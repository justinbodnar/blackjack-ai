from Deck import Deck
deck = Deck()

print( "Dealer gets a hand" )
hand = []
i = 0
while i < 5:
	hand.append( deck.deal() )
	i = i + 1

print( hand )
print( "We get a hand" )
hand2 = [ "A-H", "2-D", "3-D", "4-D", "5-D" ]
print( hand2 )
print
print( "checking our hand" )
outcome = deck.checkHand( hand2 )
print( outcome )
print
print( "checking computers hand" )
outcome = deck.checkHand( hand )
print( outcome )

counter = 1
while outcome != "Straight!":
	deck.shuffle()
	hand = []
	i = 0
	while i < 5:
		hand.append( deck.deal() )
		i = i + 1
	outcome = deck.checkHand( hand )
	print( outcome )
	print( counter )
	counter = counter + 1
print( hand )

