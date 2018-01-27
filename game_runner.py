from game_manager import GameManager
from braindead_player import BraindeadPlayer


def main():
	players = [BraindeadPlayer() for i in range(4)]
	manager = GameManager(players)
	print(manager.play_game())


main()
