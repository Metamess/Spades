

class Trick:

	def __init__(self):
		self.played_by = []
		self.cards = []
		self.won_by_spade = False
		self.suit = None

	""""Add a newly played card to the trick"""
	def add_card(self, card, player_id):
		assert 4 > len(self.cards) == len(self.played_by)
		if len(self.cards) == 0:
			self.suit = card.suit
		self.cards.append(card)
		self.played_by.append(player_id)

		if card.suit == "S":
			self.won_by_spade = True

	"""Get the suit of this trick"""
	def get_suit(self):
		if len(self.cards) > 0:
			return self.cards[0].suit
		return None

	""""Return the player id of the player currently winning trick"""
	def get_winner(self):
		winning_card = None
		for i, card in enumerate(self.cards):
			if card > winning_card:
				winning_card = card
		if winning_card is None:
			return None
		return self.played_by[self.cards.index(winning_card)]
