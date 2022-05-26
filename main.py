from mainwindow import MainWindow
from game import *
from players.static_ai import *
from players.minimax import *
from players.random_ai import *

if __name__ == '__main__':

    player1 = Random(1)
    player2 = StaticAI(2)
    game = Game(player1, player2)

    window_size = 800
    main_window = MainWindow(window_size, game)
