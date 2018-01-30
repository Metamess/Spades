import functools

suit_symbols = ["♠", "♥", "♣", "♦"]
suits = ["S", "H", "C", "D"]
suit_names = {"S": "Spades", "H": "Hearts", "C": "Clubs", "D": "Diamonds"}
numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


@functools.total_ordering
class Card:
	def __init__(self, suit_id, number_id):
		self.suit_id = suit_id
		self.number_id = number_id
		self.suit = suits[suit_id]
		self.number = numbers[number_id]

	def __eq__(self, other):
		if other is None:
			return False
		if self.suit_id == other.suit_id:
			return self.number_id == other.number_id
		return False

	def __gt__(self, other):
		if other is None:
			return True
		if self.suit_id == other.suit_id:
			return self.number_id > other.number_id

		if self.suit_id == 0:
			return True

		return False

	def __str__(self):
		return suit_symbols[suits.index(self.suit)] + self.number

	def __int__(self):
		return self.suit_id * 13 + self.number_id

	def __repr__(self):
		return "Card(" + self.__str__() + ")"

