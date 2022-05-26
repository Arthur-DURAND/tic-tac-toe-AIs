import random

from players.player import *


class StaticAI(Player):
    def __init__(self, current_player):
        super().__init__(current_player)
        self.score_board = [[3, 2, 3],
                            [2, 4, 2],
                            [3, 2, 3]]

    def play(self, board) -> Tuple[int, int]:
        # Check win possibility
        plays = _winning_plays(board, self.current_player)
        if len(plays) > 0:
            i = random.randint(0, len(plays)-1)
            return plays[i]

        # Avoid loss todo

        if self.current_player == 1:
            enemy_player = 2
        else:
            enemy_player = 1
        plays = _winning_plays(board, enemy_player)
        if len(plays) > 0:
            i = random.randint(0, len(plays) - 1)
            return plays[i]

        # Choose random best option
        plays = self._max_move(board)
        i = random.randint(0, len(plays) - 1)
        return plays[i]

    def _max_move(self, board) -> list[Tuple[int, int]]:
        max_value = 0
        max_list = list()
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    if self.score_board[i][j] > max_value:
                        max_value = self.score_board[i][j]
                        max_list.clear()
                        max_list.append((j, i))
                    elif self.score_board[i][j] == max_value:
                        max_list.append((j, i))
        return max_list

    def player_type(self):
        return "Static AI"


def _winning_plays(board, player) -> list[Tuple[int, int]]:
    plays: list[Tuple[int, int]]
    plays = list()

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                # play move
                board[i][j] = player
                if _winning_play(board, i, j):
                    plays.append((j, i))
                # undo move
                board[i][j] = 0
    return plays


def _winning_play(board, y, x) -> bool:
    # check if win
    # row
    if board[0][x] == board[1][x] and board[0][x] == board[2][x]:
        return True
    if board[y][0] == board[y][1] and board[y][0] == board[y][2]:
        return True
    if ((x == 0 and y == 0) or (x == 1 and y == 1) or (x == 2 and y == 2)) and \
            (board[0][0] == board[1][1] and board[0][0] == board[2][2]):
        return True
    if ((x == 2 and y == 0) or (x == 1 and y == 1) or (x == 0 and y == 2)) and \
            (board[0][2] == board[1][1] and board[0][2] == board[2][0]):
        return True
    return False


