from enum import Enum
from players.human import *
from players.reinforcement_learning_ai.reinforcement_learning_ai import ReinforcementLearningAI


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

    def play(self):
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
        self.current_player = switch_players(self.current_player)
        game_result = winner(self.board)
        if game_result != GameResult.CONTINUE:
            if game_result == GameResult.PLAYER1:
                self.player1.feed_reward(1)
                self.player2.feed_reward(0)
            elif game_result == GameResult.PLAYER2:
                self.player1.feed_reward(0)
                self.player2.feed_reward(1)
            else:
                self.player1.feed_reward(0.1)
                self.player2.feed_reward(0.5)
            self.player1.reset_ai()
            self.player2.reset_ai()
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
            self.current_player = switch_players(self.current_player)

        if winner(self.board) != GameResult.CONTINUE:
            self.playing = False


def display_board(board):
    print("-----------------------------------")
    for i in range(3):
        print(board[i][0], " ; ", board[i][1], " ; ", board[i][2])


def switch_players(current_player):
    if current_player == 1:
        return 2
    else :
        return 1


def winner(board) -> GameResult:
    # rows
    for i in range(3):
        if board[i][0] != 0 and \
                board[i][0] == board[i][1] and \
                board[i][0] == board[i][2]:
            return GameResult(board[i][0])

    # columns
    for i in range(3):
        if board[0][i] != 0 and \
                board[0][i] == board[1][i] and \
                board[0][i] == board[2][i]:
            return GameResult(board[0][i])

    # diagonals
    if board[0][0] != 0 and \
            board[0][0] == board[1][1] and \
            board[1][1] == board[2][2]:
        return GameResult(board[0][0])

    if board[2][0] != 0 and \
            board[2][0] == board[1][1] and \
            board[2][0] == board[0][2]:
        return GameResult(board[2][0])

    empty_space = False
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                empty_space = True
    if not empty_space:
        return GameResult.DRAW

    return GameResult.CONTINUE
