from relative_data import RelativeData


class Score(RelativeData):

	def __init__(self, reference_id=0):
		super().__init__(reference_id)
		self.data = {0: 0, 1: 0}
		self.score = self.data
		self.data_size = 2

	def add_score(self, new_score, team_id):
		""""Add points to a team's score."""
		global_id = self.globalize_id(team_id)
		self.score[global_id] += new_score

	def can_blind(self, player_id):
		""""Return whether the team of this player is eligible for a Blind Nill this round"""
		global_team_id = self.globalize_id(player_id)
		other_team_id = self.globalize_id(player_id + 1)
		return self.score[global_team_id] <= self.score[other_team_id] - 100

	def __str__(self):
		team_0_id = self.localize_id(0)
		team_1_id = self.localize_id(1)
		return "Scores: Team 0: " + str(self.score[team_0_id]) + " Team 1: " + str(self.score[team_1_id])


