from MainWindow import MainWindow
from game import *
from static_ai import *
from human import *

if __name__ == '__main__':

    player1 = Human(1)
    player2 = StaticAI(2)
    game = Game(player1, player2)

    window_size = 800
    main_window = MainWindow(window_size, game)
