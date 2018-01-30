from game_manager import GameManager
from braindead_player import BraindeadPlayer
from human_player import HumanPlayer
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
	print(manager.play_game())


main()
