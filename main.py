from game import *
from static_ai import *
from human import *


if __name__ == '__main__':

    player1 = Human(1)
    player2 = StaticAI(2)
    game = Game(player1, player2)

    game_winner = game.winner()
    while game_winner == GameResult.CONTINUE:
        game.play()
        game_winner = game.winner()

    game.display_board()
    print()
    print()
    if game_winner == GameResult.DRAW:
        print("Draw !")
    else:
        print(game_winner, " won !")
