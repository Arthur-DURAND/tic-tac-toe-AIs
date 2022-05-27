from typing import Tuple


class Player:
    def __init__(self, current_player):
        self.current_player = current_player

    def play(self, board) -> Tuple[int, int]:
        pass

    def play_position(self, board, position) -> Tuple[int, int]:
        pass

    def feed_reward(self, reward):
        pass

    def reset_ai(self):
        pass

    def player_type(self) -> str:
        pass
