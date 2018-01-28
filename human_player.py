from i_player import IPlayer

suit_names = {"S": "Spades", "H": "Hearts", "C": "Clubs", "D": "Diamonds"}


class HumanPlayer(IPlayer):

	def __init__(self):
		IPlayer.__init__(self)
		self.player_id = 0
		self.teammate_id = 2
		self.team_id = 0
		self.score = None
		self.bids = None
		self.trick_count = {i: 0 for i in range(4)}

	def give_hand(self, cards):
		"""
		Give a hand of cards to this player, by passing a list of cards.

		cards: a list of 13 Card objects.
		"""
		self.hand = HumanPlayer.order_cards(cards)
		print("You have received the following hand:")
		HumanPlayer.print_cards(self.hand)
		print()

	@staticmethod
	def order_cards(cards):
		res = {"S": [], "H": [], "C": [], "D": []}
		for current_card in cards:
			res[current_card.suit].append(current_card)
		for suit in res:
			res[suit] = sorted(res[suit], key=lambda x: int(x))
		return res

	@staticmethod
	def hand_to_list(hand):
		res = []
		for suit_key in hand:
			res += hand[suit_key]
		return res

	@staticmethod
	def print_cards(cards, show_ids=False):
		for suit in cards:
			print(suit_names[suit] + ':', ", ".join([HumanPlayer.card_to_string(card, show_ids) for card in cards[suit]]))

	@staticmethod
	def card_to_string(card, show_id=False):
		if show_id:
			return str(card) + " (" + str(int(card)) + ")"
		return str(card)

	@staticmethod
	def print_bids(bids, final=False):
		assert not final or len(bids) == 4
		for i in range(4):
			if i not in bids:
				bids.add_bid('?', i)
		team0_sum = ""
		team1_sum = ""
		if final:
			print("The bids for this round:")
			team0_sum = " = " + "+".join([str(bid) for bid in bids.get_team_bid(0)])
			team1_sum = " = " + "+".join([str(bid) for bid in bids.get_team_bid(1)])
		else:
			print("Bids so far:")
		print("\tteam 0: " + str(bids[0]) + " + " + str(bids[2]) + team0_sum)
		print("\tteam 1: " + str(bids[1]) + " + " + str(bids[3]) + team1_sum)

	def make_bid(self, bids):
		""""
		Ask this player to make a bid at the start of a round.

		bids: a dict containing all bids so far, with keys 0-3 (player_id) and values 0-13 or "B" for Blind Nill.
		return value: An integer between 0 (a Nill bid) and 13 minus the teammate's bid (inclusive).
		"""
		teammate_bid = 0
		if 2 in bids:
			pass
		if self.teammate_id in bids:
			teammate_bid = bids[self.teammate_id]
		max_bid = 13 - teammate_bid

		print("Please make a bid for this round")
		HumanPlayer.print_bids(bids)

		answer = -1
		while not (0 <= answer <= max_bid):
			try:
				answer = int(input("Please enter a number between 0 and " + str(13-teammate_bid) + "\n"))
			except ValueError:
				answer = -1
		print()
		return answer

	def play_card(self, trick, valid_cards):
		"""
		Ask this player to play a card, given the trick so far.

		trick: a Trick object with the cards played so far.
		valid_cards: a list of Card objects present in your hand that are valid to play for this trick.
						Intended purely to assist in choosing a card.
		return value: a Card object present in your hand.
		"""
		print("It's your turn to play a card!")
		print("The trick so far:", str(trick))
		print("Your hand:")
		HumanPlayer.print_cards(self.hand, True)
		valid_ids = [int(card) for card in valid_cards]
		chosen_card_nr = ""
		while chosen_card_nr not in valid_ids:
			if not isinstance(chosen_card_nr, int):
				try:
					chosen_card_nr = int(input("Please enter the value of the card you wish to play (shown in parenthesis)\n"))
				except ValueError:
					chosen_card_nr = -1
			if chosen_card_nr not in valid_ids:
				try:
					chosen_card_nr = int(input("That card is not valid for this trick, please choose another\n"))
				except ValueError:
					chosen_card_nr = ""
		chosen_card = None
		for card in valid_cards:
			if int(card) == chosen_card_nr:
				chosen_card = card
				break
		self.hand[chosen_card.suit].remove(chosen_card)
		print("You have played " + str(chosen_card))
		print()
		return chosen_card

	def offer_blind_nill(self, bids):
		""""
		Ask this player if they want to bid a Blind Nill.

		bids: a dict containing all bids so far, with keys 0-3 (player_id) and values 0-13
		return value: True or False
		"""
		print("You are allowed to bid a Blind Nill this round.")
		print("Bids so far are: " + str(bids))
		answer = input("Bid Blind Nill? (y/n)\n")
		while answer not in ["y", "Y", "n", "N"]:
			answer = input("Please answer y or n\n")
		return answer in ["y", "Y"]

	def receive_blind_nill_cards(self, cards):
		""""
		Receive 2 cards from your teammate in case of a Blind Nill.

		cards: a list of 2 Card objects.
		"""
		print("Your teammate has given you the following cards:", HumanPlayer.card_to_string(cards[0]), HumanPlayer.card_to_string(cards[1]))
		print()

	def request_blind_nill_cards(self):
		""""
		Donate 2 cards to your teammate in case of a Blind Nill.

		return value: a list of 2 Card objects present in your hand.
		"""
		print("Please select 2 cards to give to your teammate")
		print("Your hand:")
		HumanPlayer.print_cards(self.hand, True)
		hand_cards = HumanPlayer.hand_to_list(self.hand)
		hand_card_ids = [int(card) for card in hand_cards]
		chosen_card_numbers = []
		chosen_card_nr = ""
		ordinals = ["first", "second"]
		while chosen_card_nr not in hand_card_ids and len(chosen_card_numbers) < 2:
			if not isinstance(chosen_card_nr, int):
				try:
					chosen_card_nr = int(input("Please enter the value of the {} card you wish to give (shown in parenthesis)\n".format(ordinals[len(chosen_card_numbers)])))
				except ValueError:
					print("Invalid card value given. Card values must be integers")
					chosen_card_nr = ""
					continue
			if chosen_card_nr not in hand_card_ids:
				try:
					if len(chosen_card_numbers) == 1 and chosen_card_nr == chosen_card_numbers[0]:
						chosen_card_nr = int(input("You have already picked that card, please choose another\n"))
					else:
						chosen_card_nr = int(input("That card is not in your hand, please choose another\n"))
				except ValueError:
					print("Invalid card value given. Card values must be integers")
					chosen_card_nr = ""
				continue
			else:
				chosen_card_numbers.append(chosen_card_nr)
				hand_card_ids.remove(chosen_card_nr)
				chosen_card_nr = ""

		chosen_cards = []
		for chosen_card_nr in chosen_card_numbers:
			for card in hand_cards:
				if int(card) == chosen_card_nr:
					chosen_cards.append(card)
					self.hand[card.suit].remove(card)
					break
		print("You have given your teammate", str(chosen_cards[0]), "and", str(chosen_cards[1]))
		print()
		return chosen_cards

	def announce_bids(self, bids):
		""""
		Tell the player about the bids that have been made.

		bids: a dict containing all bids, with keys 0-3 (player_id) and values 0-13 or "B" for Blind Nill.
		"""
		HumanPlayer.print_bids(bids, True)
		self.bids = bids
		print()

	def announce_trick(self, trick):
		""""
		Tell the player about a completed trick.

		trick: a Trick object with the cards played.
		"""
		self.trick_count[trick.get_winner()] += 1
		print("Result:", str(trick))
		winner = trick.get_winner()
		if winner == self.player_id:
			print("Congratulations! The trick is yours!")
		elif winner == self.teammate_id:
			print("Well done, the trick goes to your teammate")
		else:
			print("Alas, the trick has gone to your opponent")

		progress_strings = []
		for team_id in range(2):
			res = "Team " + str(team_id) + ": "
			if self.bids.team_has_nill(team_id):
				res += str(self.trick_count[0 + team_id]) + "/" + str(self.bids[0 + team_id])
				res += " + "
				res += str(self.trick_count[2 + team_id]) + "/" + str(self.bids[2 + team_id])
			else:
				trick_sum = self.trick_count[0 + team_id] + self.trick_count[2 + team_id]
				res += str(trick_sum) + "/" + str(self.bids.get_team_bid(team_id)[0])
			progress_strings.append(res)

		print("Current trick count:", self.trick_count, "Progress:", ", ".join(progress_strings))
		print()

	def announce_score(self, score):
		""""
		Tell the player about the new scores for each team.

		score: a dict containing the scores of each team (keys 0 and 1).
		"""
		if self.score is None:
			self.announce_start()
			self.score = score
		else:
			self.score = score
			print("The new scores are " + str(score))
			print()

	def announce_start(self):
		print("Welcome, player " + str(self.player_id) + "!")
		print("You are on team " + str(self.team_id) + " together with player " + str(self.teammate_id))
		print()
