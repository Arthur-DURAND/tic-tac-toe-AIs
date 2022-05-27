from tkinter import *


class MainWindow:
    def __init__(self, window_size, game):
        super().__init__()

        self.game = game

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
        start_button = Button(infos, text="Start game", command=self.start_game)
        start_button.place(x=10, y=10)
        # bouton stop (rename start)
        # input delay + bouton apply
        # input chose ai 1 & 2
        # input number of game
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

        self.delay = 100
        self.window.after(self.delay, self.clock())
        self.window.mainloop()

    def on_mouse_down(self, event, position):
        print(position)
        if (self.game.current_player == 1 and self.game.player1.player_type() == "Human"
                or self.game.current_player == 2 and self.game.player2.player_type() == "Human") \
                and self.game.playing:
            self.game.play_human(position)
            self.display_board()

    def start_game(self):
        # Clear canvas
        for canvas in self.cells:
            canvas.delete("all")
        # Start game
        self.game.start()

    def clock(self):
        if self.game.playing:
            self.game.play()
            self.display_board()
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
