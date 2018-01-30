from card import suit_names
from card import Card


def generate_random_hand():
	from card import Card
	import random
	deck = []
	for s in range(4):
		for n in range(13):
			deck += [Card(s, n)]
	random.shuffle(deck)
	return CardSet(deck[:13])


class CardSet:

	def __init__(self, cards):
		""""Create a card set containing the cards sorted in ascending order per suit"""
		self.cards = {"S": [], "H": [], "C": [], "D": []}
		# Divide the cards over the suits
		for current_card in cards:
			self.cards[current_card.suit].append(current_card)
		# Sort the cards per suit
		for suit in self.cards:
			self.cards[suit] = sorted(self.cards[suit], key=lambda x: int(x))

	def get_suit_cards(self, suit):
		""""Get a list containing the cards of the given suit"""
		return self.cards[suit]

	def get_suit_size(self, suit):
		"""Get the amount of cards of this suit in the set"""
		return len(self.get_suit_cards(suit))

	def has_suit(self, suit):
		"""Return whether or not the set contains cards of a given suit"""
		return self.get_suit_size(suit) > 0

	def get_high_card(self, suit):
		"""Get the highest card of the given suit from the set"""
		if self.has_suit(suit):
			return self.cards[suit][-1:]
		return None

	def get_low_card(self, suit):
		"""Get the lowest card of the given suit from the set"""
		if self.has_suit(suit):
			return self.cards[suit][0]
		return None

	def to_list(self):
		"""Get all the cards in the set as a single list"""
		res = []
		for suit in self.cards:
			res += self.cards[suit]
		return res

	def remove(self, card):
		"""Remove a card from the CardSet"""
		if card not in self:
			raise ValueError("CardSet does not contain card " + str(card))
		self.get_suit_cards(card.suit).remove(card)

	def append(self, card):
		"""Add a card to the CardSet"""
		if not isinstance(card, Card):
			raise TypeError("must be Card, not " + str(type(card)))
		self.cards[card.suit].append(card)
		self.cards[card.suit] = sorted(self.cards[card.suit], key=lambda x: int(x))

	def __len__(self):
		return sum(len(suit_cards) for suit_cards in self.cards.values())

	def __contains__(self, card):
		for suit in self.cards:
			if card in self.cards[suit]:
				return True
		return False

	def __getitem__(self, i):
		for suit in self.cards:
			if i < len(self.cards[suit]):
				return self.cards[suit][i]
			else:
				i -= len(self.cards[suit])
		raise KeyError(i)

	def __iter__(self):
		return iter(self.to_list())

	def to_string(self, show_ids=False):
		"""Includes the option to print the card id with the card"""
		return "\n".join([suit_names[suit] + ': ' + ", ".join(
			[str(card) + (" (" + str(int(card)) + ")") * show_ids for card in self.cards[suit]]) for suit in self.cards])

	def __str__(self):
		return self.to_string()

	def __repr__(self):
		return "CardSet(" + ", ".join(str(card) for card in self.to_list()) + ")"
