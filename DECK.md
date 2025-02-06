# Deck Class Usage Examples

This README provides examples of how to use the `Deck` class which simulates a deck of cards with various functionalities like shuffling, dealing, and tracking cards.

## Initialization

```python
from deck_module import Deck  # Make sure the class is in a module named deck_module.py

# Create a new deck of cards
deck = Deck()
```

## Shuffling the Deck

The deck is automatically shuffled when it is initialized. However, you can shuffle it again at any time using:

```python
deck.shuffle()
```

## Dealing a Card

To deal a single card from the deck:

```python
card = deck.deal()
print(card)  # Outputs a card in the format "value-suit", e.g., "13-h"
```

## Checking the Deck

To print all cards currently in the deck and see the total count:

```python
deck.checkDeck()
```

## Getting the Number of Cards in the Deck

To get the current number of cards in the deck:

```python
count = deck.cardinality()
print(count)
```

## Getting the Negated Deck

To get an array representing the negated deck (i.e., cards that have been dealt so far):

```python
negated_deck = deck.negation()
print(negated_deck)  # Outputs an array of 0s and 1s representing the status of each card
```

Each method of the `Deck` class allows interaction with the deck of cards, mimicking real-world actions like shuffling and dealing, as well as tracking cards that have been used.
```

