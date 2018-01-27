from relative_data import RelativeData

suit_names = {"S": "Spades", "H": "Hearts", "C": "Clubs", "D": "Diamonds", None: "Empty"}


class Trick(RelativeData):

	def __init__(self, reference_id=0):
		super().__init__(reference_id)
		self.cards = self.data
		self.won_by_spade = False
		self.suit = None

	def add_card(self, card, player_id):
		""""Add a newly played card to the trick."""
		global_id = self.relative_to_global(player_id)
		assert len(self.cards) < self.data_size and global_id not in self.cards
		if len(self.cards) == 0:
			self.suit = card.suit
		self.cards[global_id] = card
		if card.suit == "S":
			self.won_by_spade = True

	def get_suit(self):
		"""Get the suit of this trick."""
		return self.suit

	def get_winner(self):
		""""Return the player id of the player currently winning trick."""
		winning_card = None
		winning_id = None
		for global_id in self.cards:
			card = self.cards[global_id]
			if card > winning_card:
				winning_card = card
				winning_id = global_id
		assert len(self.cards) == 0 or winning_card is not None
		if winning_card is None:
			return None
		return self.global_to_relative(winning_id)

	def __str__(self):
		t = {i: "??" for i in range(4)}
		for i in range(4):
			if i in self.cards:
				relative_id = self.global_to_relative(i)
				t[relative_id] = self.cards[i]
		# card_str = ", ".join([str(i) + ": " + str(t[i]) for i in range(4)])
		card_str = ", ".join([str(t[i]) for i in range(4)])
		return suit_names[self.suit] + " Trick: " + card_str + " (Winner: " + str(self.get_winner()) + ")"


