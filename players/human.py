from players.player import *


class Human(Player):
    def __init__(self, current_player):
        super().__init__(current_player)

    # def play(self, board) -> Tuple[int, int]:
    #     while True:
    #         try:
    #             # input
    #             position = int(input("Please enter a number between 1 and 9 included: ")) - 1
    #             # out of range
    #             if position > 8 or position < 0:
    #                 print("This number isn't between 1 and 9. Try again.")
    #             # convert for 3*3 board
    #             y = position // 3
    #             x = position % 3
    #             # check if empty
    #             if board[y][x] == 0:
    #                 return x, y
    #             else:
    #                 print("This position is already taken. Try again.")
    #         except ValueError:
    #             print("That was no valid number. Try again.")

    def play_position(self, board, position) -> Tuple[int, int]:
        while True:
            # out of range
            if position > 8 or position < 0:
                return -1, -1
            # convert for 3*3 board
            y = position // 3
            x = position % 3
            # check if empty
            if board[y][x] == 0:
                return x, y
            else:
                return -1, -1

    def player_type(self):
        return "Human"
