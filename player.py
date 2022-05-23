from typing import Tuple


class Player:
    def __init__(self, current_player):
        self.current_player = current_player

    def play(self, board) -> Tuple[int, int]:
        pass

    def player_type(self) -> str:
        pass
