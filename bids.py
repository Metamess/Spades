from relative_data import RelativeData


class Bids(RelativeData):

	def __init__(self, reference_id=0):
		super().__init__(reference_id)
		self.bids = self.data

	def add_bid(self, bid, player_id):
		""""Add a new bid."""
		global_id = self.relative_to_global(player_id)
		assert len(self.bids) < self.data_size and global_id not in self.bids
		if bid == 0:
			bid = "N"
		self.bids[global_id] = bid

	def team_has_nill(self, team_id):
		"""Return whether a player on a team has bid a Nill."""
		global_team_id = (team_id + self.reference_id) % 2
		player_ids = [global_team_id, global_team_id + 2]
		for player_id in player_ids:
			if player_id in self.bids and (self.bids[player_id] == "N" or self.bids[player_id] == "B"):
				return True
		return False

	def get_blinder_id(self):
		for player_id in self.bids:
			if self.bids[player_id] == "B":
				return self.global_to_relative(player_id)
		return None

	def get_team_bid(self, team_id):
		""""
		Get the bid of a team.
		return: A list with a single entry if both players made a normal bid, or the separate bids if either player has bid a (Blind) Nill.
				List will contain '?' if a player has not yet made a bid.
		"""
		global_team_id = (team_id + self.reference_id) % 2
		player_ids = [global_team_id, global_team_id + 2]
		res = []
		summable = True
		for player_id in player_ids:
			if player_id in self.bids:
				if self.bids[player_id] == "N" or self.bids[player_id] == "B":
					summable = False
				res.append(self.bids[player_id])
			else:
				summable = False
				res.append('?')
		if summable:
			res = [res[0] + res[1]]
		return res

	def __str__(self):
		str_bids = {i: '?' for i in range(4)}
		for i in range(4):
			if i in self.bids:
				relative_id = self.global_to_relative(i)
				str_bids[relative_id] = str(self.bids[i])
		return "Bids: team 0: " + str_bids[0] + " + " + str_bids[2] + " team 1: " + str_bids[1] + " + " + str_bids[3]


