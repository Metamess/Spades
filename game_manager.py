import random
import card
from copy import deepcopy
from i_player import IPlayer
from trick import Trick
from bids import Bids


_BLIND_NILL_CHARACTER = "B"


class GameManager:

	def __init__(self, players=[IPlayer()]*4, playing_to=500):
		self.players = players
		self.playing_to = playing_to
		self.score = {0: 0, 1: 0}  # Players 0 and 2 form team 0, players 1 and 3 are team 1
		self.hands = {}
		self.dealer = 0
		self.bids = Bids()

	def deal_deck(self):
		"""
		Shuffle the deck and deal 13 cards to each player.
		Note that for Blind Nill purposes, the handing out of cards happens during the bidding phase.
		"""
		deck = []
		for suit_id in range(4):
			for number_id in range(13):
				deck.append(card.Card(suit_id, number_id))
		random.shuffle(deck)

		for i in range(4):
			hand = deck[13*i: 13*(i+1)]
			self.hands[i] = hand
		self.dealer = (self.dealer + 1) % 4

	def get_bids(self):
		""""Get the bids of all players in order."""
		self.bids = Bids()
		blind_accepted = False
		for i in range(4):
			# The value of 'dealer' will have been incremented at the end of the deal
			# Hence, it's current value is the player who should start bidding
			active_player_id = (self.dealer + i) % 4
			# First, we have to check if a Blind Nill bid is allowed, and if so, offer the option
			if not blind_accepted and self.score[active_player_id % 2] <= self.score[(active_player_id + 1) % 2] - 100:
				if self.players[active_player_id].offer_blind_nill(self.bids.make_copy(active_player_id)):
					blind_accepted = True
					self.bids.add_bid(_BLIND_NILL_CHARACTER, active_player_id)
					self.players[active_player_id].give_hand(deepcopy(self.hands[active_player_id]))
					continue
			# Hand out the cards to the player and ask for a bid
			self.players[active_player_id].give_hand(deepcopy(self.hands[active_player_id]))
			self.bids.add_bid(self.players[active_player_id].make_bid(self.bids.make_copy(active_player_id)), active_player_id)
		# When all bids have been made, inform all players about them
		for i, player in enumerate(self.players):
			player.announce_bids(self.bids.make_copy(i))

	def handle_card_exchange(self):
		""""Exchanges 2 cards between the players of the team running a Blind Nill."""
		assert self.bids.get_blinder_id() is not None
		blinder_id = self.bids.get_blinder_id()
		# Step 1: Get 2 cards from the person running the Blind Nill and give them to the teammate
		# Step 2: Get 2 cards from the teammate and give them to the person running the Blind Nill
		for i in [0, 2]:
			giver_id = (blinder_id + i) % 4
			receiver_id = (giver_id + 2) % 4
			offered_cards = deepcopy(self.players[giver_id].request_blind_nill_cards())
			# As always, don't trust the players, and check all conditions
			assert len(offered_cards) == 2
			for offered_card in offered_cards:
				assert offered_card in self.hands[giver_id]
				self.hands[giver_id].remove(offered_card)
			self.players[receiver_id].receive_blind_nill_cards(deepcopy(offered_cards))
			self.hands[receiver_id] += offered_cards

	def get_trick(self, starting_player, spades_broken):
		""""Play a trick by getting a card from each player in order."""
		current_trick = Trick()
		for i in range(4):
			player_id = (starting_player + i) % 4
			card_played = self.players[player_id].play_card(current_trick.make_copy(player_id), self.get_valid_cards(player_id, current_trick, spades_broken))
			assert self.verify_card_validity(card_played, player_id, current_trick, spades_broken)
			current_trick.add_card(card_played, player_id)
			self.hands[player_id].remove(card_played)
		return current_trick

	def verify_card_validity(self, played_card, player_id, trick, spades_broken):
		""""Verify that an offered card is valid to play."""
		try:
			# First off, a card can only be played if the player actually has it
			assert played_card in self.hands[player_id]
			# Secondly, check if the card is of the right suit
			# If the player starts the trick or matches the suit, all is fine
			if trick.suit is not None and played_card.suit != trick.suit:
				for hand_card in self.hands[player_id]:
					assert hand_card.suit != trick.suit
			# Thirdly, a player may only start a trick with a spade if a spade has been played before,
			# or if the player only has spades left in his hand
			if trick.suit is None and played_card.suit == "S" and not spades_broken:
				for hand_card in self.hands[player_id]:
					assert hand_card.suit == "S"
		except AssertionError:
			return False
		return True

	def get_valid_cards(self, player_id, trick, spades_broken):
		""""Generate a list of all cards in a player's hand that are valid to play for this trick."""
		valid_cards = []
		for hand_card in self.hands[player_id]:
			if self.verify_card_validity(hand_card, player_id, trick, spades_broken):
				valid_cards.append(hand_card)
		return deepcopy(valid_cards)

	def play_round(self):
		""""Play a round, consisting of 13 tricks."""
		# Set up the round
		spades_broken = False
		self.deal_deck()
		starting_player = self.dealer
		self.get_bids()
		trick_count = {0: 0, 1: 0, 2: 0, 3: 0}
		if self.bids.get_blinder_id() is not None:
			self.handle_card_exchange()
		# Play the round
		for i in range(13):
			current_trick = self.get_trick(starting_player, spades_broken)
			if current_trick.won_by_spade:
				spades_broken = True
			starting_player = current_trick.get_winner()
			trick_count[starting_player] += 1
			# Inform all players of the final result of the trick
			for i, player in enumerate(self.players):
				player.announce_trick(current_trick.make_copy(i))
		# Handle the scoring
		for i in [0, 1]:
			self.award_scores(trick_count, i)
		# Inform all players about the new score
		for player in self.players:
			player.announce_score(self.score.copy())

	def award_scores(self, trick_count, team_id):
		""""Given the bids and a resulting trick count, decide the score for a team."""
		gained_score = 0
		handled = False

		# First, handle the situation of a player nilling
		for i in [0, 2]:
			nilled = False
			if self.bids[i + team_id] == 0:
				nilled = True
				if trick_count[i + team_id] == 0:
					gained_score += 50
				else:
					gained_score -= 50
			if self.bids[i + team_id] == _BLIND_NILL_CHARACTER:
				nilled = True
				if trick_count[i + team_id] == 0:
					gained_score += 100
				else:
					gained_score -= 100
			if nilled:
				handled = True
				other_bid = self.bids[(2-i) + team_id]
				# In the insane case of a double Nill
				if other_bid == 0 or other_bid == _BLIND_NILL_CHARACTER:
					continue
				# Handle the contract of the other player solo
				other_tricks = trick_count[(2-i) + team_id]
				if other_tricks < other_bid:
					gained_score -= other_bid * 10
				else:
					gained_score += other_bid * 10 + max(0, other_tricks - other_bid)

		# If there was no Nill, handle the scoring normally
		if not handled:
			bid = self.bids[0 + team_id] + self.bids[2 + team_id]
			tricks = trick_count[0 + team_id] + trick_count[2 + team_id]
			if tricks < bid:
				gained_score -= bid * 10
			else:
				gained_score += bid * 10 + max(0, tricks - bid)

		# Check for sandbagging
		if (self.score[team_id] % 10) + (gained_score % 10) >= 10:
			gained_score -= 100

		self.score[team_id] += gained_score

	def play_game(self):
		"""""Simulate one game of Spades with the given players."""
		assert len(self.players) == 4
		self.score = {0: 0, 1: 0}
		self.dealer = 0
		# Tell the player's about their id's
		for i in range(4):
			self.players[i].announce_ids(i, (i+2) % 4, i % 2)
		# Play rounds until one side wins
		while -self.playing_to < self.score[0] < self.playing_to and -self.playing_to < self.score[1] < self.playing_to:
			self.play_round()
		return self.score
