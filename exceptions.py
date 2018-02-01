
class SpadesError(Exception):
	"""The base class for all errors defined by the Spades framework"""


class PlayerCountError(SpadesError):
	"""Raised when there are not 4 players passed to the game manager"""
	def __init__(self, players):
		msg = "Expected 4 IPlayer instances, got {0} instead".format(players)
		super().__init__(msg)
		self.players = players


class RuleViolationError(SpadesError):
	"""Raised when a game rule has been violated"""

	def __init__(self, player_id, msg=None):
		if msg is None:
			msg = "A game rule was violated by player " + str(player_id)
		super().__init__(msg)
		self.player_id = player_id


class BidError(RuleViolationError):
	"""Raised when a player has made an illegal bid"""

	def __init__(self, player_id, bid, teammate_bid=None):
		if teammate_bid is None:
			msg = "Illegal bid by player {0}: {1}".format(player_id, bid)
		else:
			msg = "Illegal bid by player {0}: {1}, teammate has bid {2}".format(player_id, bid, teammate_bid)
		super().__init__(player_id, msg)
		self.bid = bid


class CardError(RuleViolationError):
	"""Raised when a player tries to play an invalid card"""

	def __init__(self, player_id, card=None, msg=None):
		if msg is None:
			if card is None:
				msg = "Player {0} tried to play an illegal card".format(player_id)
			else:
				msg = "Player {0} tried to play an illegal card: {1}".format(player_id, {1})
		super().__init__(player_id, msg)
		self.card = card


class CardSwapError(CardError):
	"""Raised when a player doesn't give 2 valid cards when swapping cards for a Blind Nill"""

	def __init__(self, player_id, cards=None, msg=None):
		if msg is None:
			if cards is None:
				msg = "Player {0} failed to provide 2 valid cards for swapping".format(player_id)
			else:
				msg = "Player {0} failed to provide 2 valid cards for swapping; received {1}".format(player_id, {1})
		super().__init__(player_id, msg=msg)
		self.cards = cards
