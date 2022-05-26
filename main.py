from mainwindow import MainWindow
from game import *
from static_ai import *
from human import *
from minimax import *

if __name__ == '__main__':

    player1 = MiniMax(1)
    player2 = StaticAI(2)
    game = Game(player1, player2)

    window_size = 800
    main_window = MainWindow(window_size, game)
