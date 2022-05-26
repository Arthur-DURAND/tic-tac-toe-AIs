import random

from players.player import *


class Random(Player):
    def __init__(self, current_player):
        super().__init__(current_player)

    def play(self, board) -> Tuple[int, int]:
        possible_moves = list()
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    possible_moves.append((j, i))
        i = random.randint(0, len(possible_moves)-1)
        return possible_moves[i]

    def player_type(self):
        return "Random AI"
