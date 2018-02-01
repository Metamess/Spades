from game_manager import GameManager
from braindead_player import BraindeadPlayer
from human_player import HumanPlayer
import exceptions
import sys


def main():
	human_player_count = 0
	if len(sys.argv) > 1:
		try:
			human_player_count = int(sys.argv[1])
			assert 0 <= human_player_count <= 2
		except (IndexError, ValueError, AssertionError):
			print("Please enter the amount of human players you want to add (0-2) as first parameter")
			exit()

	players = [BraindeadPlayer() for i in range(4 - human_player_count)] + [HumanPlayer() for i in range(human_player_count)]
	manager = GameManager(players)
	try:
		game_result = manager.play_game()
		victory_string = "a tie!"
		winner = game_result.get_winner()
		if winner is not None:
			victory_string = "won by team {0}.".format(winner)
		print("The game was " + victory_string)
		print("Final " + str(game_result))
	except exceptions.RuleViolationError as e:
		print("The game was ended due to a rule violation by player {0}:".format(e.player_id))
		print("\t", e)
		print("As a result, team {0} wins the game by forfeiture".format((e.player_id + 1) % 2))


main()
