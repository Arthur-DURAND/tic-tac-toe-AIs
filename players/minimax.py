import random
from players.player import *
import game


class MiniMax(Player):
    def __init__(self, current_player):
        super().__init__(current_player)

    def play(self, board) -> Tuple[int, int]:
        value, position = minimax(board, self.current_player, self.current_player)
        return position

    def player_type(self):
        return "MiniMax AI"


def minimax(board, player_turn, player_to_maximize):
    winner = game.winner(board)
    if (winner == game.GameResult.PLAYER1 and player_to_maximize == 1)\
            or (winner == game.GameResult.PLAYER2 and player_to_maximize == 2):
        return 1, (-1, -1)
    elif (winner == game.GameResult.PLAYER1 and player_to_maximize == 2)\
            or (winner == game.GameResult.PLAYER2 and player_to_maximize == 1):
        return -1, (-1, -1)
    elif winner == game.GameResult.DRAW:
        return 0, (-1, -1)

    max_value = -2
    max_plays = list()
    min_value = 2
    min_plays = list()
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                # Do
                board[i][j] = player_turn
                # Recursion
                value, _ = minimax(board, game.switch_players(player_turn), player_to_maximize)
                # Undo
                board[i][j] = 0

                if value == max_value:
                    max_plays.append((j, i))
                if value == min_value:
                    min_plays.append((j, i))
                if value > max_value:
                    max_value = value
                    max_plays.clear()
                    max_plays.append((j, i))
                if value < min_value:
                    min_value = value
                    min_plays.clear()
                    min_plays.append((j, i))

    if player_turn == player_to_maximize:
        i = random.randint(0, len(max_plays)-1)
        return max_value, max_plays[i]
    else:
        i = random.randint(0, len(min_plays)-1)
        return min_value, min_plays[i]
