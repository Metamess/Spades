suit_names = {"S": "Spades", "H": "Hearts", "C": "Clubs", "D": "Diamonds", None: "Empty"}


class Trick:

	def __init__(self):
		self.played_by = []
		self.cards = []
		self.won_by_spade = False
		self.suit = None

	def add_card(self, card, player_id):
		""""Add a newly played card to the trick."""
		assert 4 > len(self.cards) == len(self.played_by)
		if len(self.cards) == 0:
			self.suit = card.suit
		self.cards.append(card)
		self.played_by.append(player_id)

		if card.suit == "S":
			self.won_by_spade = True

	def get_suit(self):
		"""Get the suit of this trick."""
		if len(self.cards) > 0:
			return self.cards[0].suit
		return None

	def get_winner(self):
		""""Return the player id of the player currently winning trick."""
		winning_card = None
		for i, card in enumerate(self.cards):
			if card > winning_card:
				winning_card = card
		assert len(self.cards) == 0 or winning_card is not None
		if winning_card is None:
			return None
		return self.played_by[self.cards.index(winning_card)]

	def __str__(self):
		t = {i: "??" for i in range(4)}
		for i in range(len(self.cards)):
			t[self.played_by[i]] = self.cards[i]
		card_str = ", ".join([str(i) + ": " + str(t[i]) for i in range(4)])
		return suit_names[self.suit] + " Trick: " + card_str + " (Winner: " + str(self.get_winner()) + ")"


