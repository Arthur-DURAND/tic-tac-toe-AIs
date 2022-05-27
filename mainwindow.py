from tkinter import *
from game import *


class MainWindow:
    def __init__(self, window_size, game):
        super().__init__()

        self.game = game
        self.delay = 1000
        self.game_number = 1
        self.current_game_number = 0
        self.loop_playing = False
        self.player1_win = 0
        self.player2_win = 0
        self.draws = 0

        # window
        self.window = Tk()
        self.window.geometry(str(window_size) + "x" + str(int(window_size * 7 / 6)))
        self.window.title('Tic Tac Toe')
        self.window.resizable(False, False)

        # Infos
        line_size = 4
        infos = Frame(self.window, height=int(1 / 6 * window_size) - line_size, width=window_size,
                      background="#606060")  # 525054
        line = Frame(self.window, height=line_size, width=window_size, background="#1e1e1f")

        # Buttons
        self.start_button = Button(infos, text="Start game", command=self.start_game)
        self.start_button.place(x=10, y=10)

        self.delay_entry = Entry(infos, width=10)
        self.delay_entry.insert(0, str(self.delay))
        self.delay_entry.place(x=10, y=40)
        self.delay_entry.bind('<Return>', self.change_delay)

        self.game_number_entry = Entry(infos, width=10)
        self.game_number_entry.insert(0, str(self.game_number))
        self.game_number_entry.place(x=10, y=70)
        self.game_number_entry.bind('<Return>', self.change_game_number)

        # TODO
        # input chose ai 1 & 2
        # display results (reset on start)

        # Board
        board = Frame(self.window, height=window_size, width=window_size, background="#2b2b2b")

        for i in range(3):
            board.columnconfigure(i, weight=1)
            board.rowconfigure(i, weight=1)

        self.cells = list()
        for i in range(9):
            canvas = Canvas(board, background="#1e1e1f", highlightthickness=3, highlightbackground="#606060")
            canvas.grid(column=(i % 3), row=(i // 3), padx=20, pady=20)
            canvas.bind("<Button-1>", lambda event, arg=i: self.on_mouse_down(event, arg))
            self.cells.append(canvas)
        self.drawings_size_ratio = 0.8

        # window
        infos.pack(side=TOP)
        line.pack(side=TOP)
        board.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.window.after(self.delay, self.clock())
        self.window.mainloop()

    def on_mouse_down(self, event, position):
        print(position)
        if (self.game.current_player == 1 and self.game.player1.player_type() == "Human"
                or self.game.current_player == 2 and self.game.player2.player_type() == "Human") \
                and self.game.playing:
            self.game.play_human(position)
            self.display_board()

    def change_delay(self, event):
        new_delay = self.delay
        try:
            new_delay = int(self.delay_entry.get())
        except ValueError:
            pass
        if new_delay > 0:
            self.delay = new_delay

    def change_game_number(self, event):
        game_number = self.game_number
        try:
            game_number = int(self.game_number_entry.get())
        except ValueError:
            pass
        if game_number > 0:
            self.game_number = game_number

    def start_game(self):
        if self.game.playing:
            self.game.playing = False
            self.start_button["text"] = "Start game"
            self.loop_playing = False
        else:
            # Clear canvas
            for canvas in self.cells:
                canvas.delete("all")
            # Change button
            self.start_button["text"] = "Stop game"
            # Start game
            self.loop_playing = True
            self.game.start()

    def clock(self):
        if self.game.playing:
            self.game.play()
            self.display_board()
        else:
            if self.loop_playing:

                result = winner(self.game.board)
                if result == GameResult.PLAYER1:
                    self.player1_win += 1
                elif result == GameResult.PLAYER2:
                    self.player2_win += 1
                elif result == GameResult.DRAW:
                    self.draws += 1

                self.current_game_number += 1
                if self.current_game_number >= self.game_number:
                    self.start_button["text"] = "Start game"
                    self.current_game_number = 0
                    self.loop_playing = False
                    print("---")
                    print(self.player1_win)
                    print(self.player2_win)
                    print(self.draws)
                    self.player1_win = 0
                    self.player2_win = 0
                    self.draws = 0
                else:
                    for canvas in self.cells:
                        canvas.delete("all")
                    self.game.start()
        self.window.after(self.delay, self.clock)

    def display_board(self):
        for i in range(3):
            for j in range(3):
                if self.game.board[i][j] == 1:
                    self.display1(3 * i + j)
                elif self.game.board[i][j] == 2:
                    self.display2(3 * i + j)

    def display1(self, position):
        canvas = self.cells[position]
        canvas.delete("all")
        canvas.create_oval(canvas.winfo_width() * (1 - self.drawings_size_ratio) / 2,
                           canvas.winfo_width() * (1 - self.drawings_size_ratio) / 2,
                           canvas.winfo_width() * (1 - (1 - self.drawings_size_ratio) / 2),
                           canvas.winfo_width() * (1 - (1 - self.drawings_size_ratio) / 2),
                           outline="#404040", width=11)
        canvas.create_oval(canvas.winfo_width() * (1 - self.drawings_size_ratio) / 2 + 0.5,
                           canvas.winfo_width() * (1 - self.drawings_size_ratio) / 2 + 0.5,
                           canvas.winfo_width() * (1 - (1 - self.drawings_size_ratio) / 2) - 0.5,
                           canvas.winfo_width() * (1 - (1 - self.drawings_size_ratio) / 2) - 0.5,
                           outline="#606060", width=10)

    def display2(self, position):
        canvas = self.cells[position]
        canvas.delete("all")
        canvas.create_line(canvas.winfo_width() * (1 - self.drawings_size_ratio) / 2,
                           canvas.winfo_width() * (1 - self.drawings_size_ratio) / 2,
                           canvas.winfo_width() * (1 - (1 - self.drawings_size_ratio) / 2),
                           canvas.winfo_width() * (1 - (1 - self.drawings_size_ratio) / 2),
                           fill="#606060", width=10, capstyle="round", joinstyle="round")

        canvas.create_line(canvas.winfo_width() * (1 - self.drawings_size_ratio) / 2,
                           canvas.winfo_width() * (1 - (1 - self.drawings_size_ratio) / 2),
                           canvas.winfo_width() * (1 - (1 - self.drawings_size_ratio) / 2),
                           canvas.winfo_width() * (1 - self.drawings_size_ratio) / 2,
                           fill="#606060", width=10, capstyle="round", joinstyle="round")
