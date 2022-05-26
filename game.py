from enum import Enum
from player import *
from static_ai import *
from human import *


class GameResult(Enum):
    CONTINUE = 0
    PLAYER1 = 1
    PLAYER2 = 2
    DRAW = 3


class Game:
    board: list[list[int]]
    current_player: int
    player1: Player
    player2: Player

    def __init__(self, player1, player2) -> None:
        super().__init__()
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

        self.current_player = 1
        self.player1 = player1
        self.player2 = player2
        self.turn = 0
        self.playing = False

    def start(self):
        #game_winner = self.winner()
        #while game_winner == GameResult.CONTINUE:
        #    self.play()
        #    game_winner = self.winner()
#
        #self.display_board()
        #print()
        #print()
        #if game_winner == GameResult.DRAW:
        #    print("Draw !")
        #else:
        #    print(game_winner, " won !")
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.current_player = 1
        self.turn = 0
        self.playing = True


    def winner(self) -> GameResult:
        # rows
        for i in range(3):
            if self.board[i][0] != 0 and \
                    self.board[i][0] == self.board[i][1] and \
                    self.board[i][0] == self.board[i][2]:
                return GameResult(self.board[i][0])

        # columns
        for i in range(3):
            if self.board[0][i] != 0 and \
                    self.board[0][i] == self.board[1][i] and \
                    self.board[0][i] == self.board[2][i]:
                return GameResult(self.board[0][i])

        # diagonals
        if self.board[0][0] != 0 and \
                self.board[0][0] == self.board[1][1] and \
                self.board[1][1] == self.board[2][2]:
            return GameResult(self.board[0][0])

        if self.board[2][0] != 0 and \
                self.board[2][0] == self.board[1][1] and \
                self.board[2][0] == self.board[0][2]:
            return GameResult(self.board[2][0])

        empty_space = False
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    empty_space = True
        if not empty_space:
            return GameResult.DRAW

        return GameResult.CONTINUE

    def play(self):
        if self.winner() == GameResult.CONTINUE:
            if self.current_player == 1:
                # print("Player 1's turn : ", self.player1.player_type())
                # self.display_board()
                if self.player1.player_type() == "Human":
                    return
                x, y = self.player1.play(self.board)
            else:
                # print("Player 2's turn : ", self.player2.player_type())
                # self.display_board()
                if self.player2.player_type() == "Human":
                    return
                x, y = self.player2.play(self.board)
            self.board[y][x] = self.current_player
            self._switch_players()
        else:
            self.playing = False

    def play_human(self, position):
        if self.current_player == 1:
            if self.player1.player_type() == "Human":
                x, y = self.player1.play_position(self.board, position)
            else:
                print("Error : not human")
                return

        else:
            if self.player2.player_type() == "Human":
                x, y = self.player1.play_position(self.board, position)
            else:
                print("Error : not human")
                return
        if x != -1 and y != -1:
            self.board[y][x] = self.current_player
            self._switch_players()

    def display_board(self):
        print("-----------------------------------")
        for i in range(3):
            print(self.board[i][0], " ; ", self.board[i][1], " ; ", self.board[i][2])

    def _switch_players(self):
        if self.current_player == 1:
            self.current_player = 2
        else :
            self.current_player = 1
