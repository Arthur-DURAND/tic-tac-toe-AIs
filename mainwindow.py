from tkinter import *
from game import *
from players.static_ai import *
from players.minimax import MiniMax
from players.random_ai import *
from players.reinforcement_learning_ai.reinforcement_learning_ai import *


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
        infos = Frame(self.window, height=int(1 / 6 * window_size) - line_size, width=window_size, background="#606060")
        line = Frame(self.window, height=line_size, width=window_size, background="#1e1e1f")

        # Buttons, entries and labels
        for i in range(4):
            infos.columnconfigure(i, weight=1)
            infos.rowconfigure(i, weight=1)
        infos.columnconfigure(4, weight=1)
        infos.columnconfigure(5, weight=1)
        infos.columnconfigure(6, weight=1)

        label_font = ("Comic Sans MS", 14)
        self.start_button = Button(infos, text="Start game", command=self.start_game, font=("Comic Sans MS", 12))
        self.start_button.grid(column=6, row=0, pady=3)
        self.ai1_label = Label(infos, text="Player 1 starts", background="#606060", font=label_font)
        self.ai1_label.grid(column=6, row=1)

        self.delay_label = Label(infos, text="Delay : ", background="#606060", font=label_font)
        self.delay_label.grid(column=0, row=0, sticky=W)
        self.delay_entry = Entry(infos, width=10)
        self.delay_entry.insert(0, str(self.delay))
        self.delay_entry.grid(column=1, row=0, sticky=W)

        self.game_number_label = Label(infos, text="Nb of games : ", background="#606060", font=label_font)
        self.game_number_label.grid(column=0, row=1, sticky=W)
        self.game_number_entry = Entry(infos, width=10)
        self.game_number_entry.insert(0, str(self.game_number))
        self.game_number_entry.grid(column=1, row=1, sticky=W)

        self.player1_label = Label(infos, text="Player 1", background="#606060", font=label_font)
        self.player1_label.grid(column=3, row=0, sticky=W + E)
        self.ai1_type_label = Label(infos, text=self.game.player1.player_type(), background="#606060", font=label_font)
        self.ai1_type_label.grid(column=3, row=1, sticky=W + E)
        self.score_p1_label = Label(infos, text="0", background="#606060", font=label_font)
        self.score_p1_label.grid(column=3, row=2, sticky=W + E)
        self.player2_label = Label(infos, text="Player 2", background="#606060", font=label_font)
        self.player2_label.grid(column=5, row=0, sticky=W + E)
        self.ai2_type_label = Label(infos, text=self.game.player2.player_type(), background="#606060", font=label_font)
        self.ai2_type_label.grid(column=5, row=1, sticky=W + E)
        self.score_p2_label = Label(infos, text="0", background="#606060", font=label_font)
        self.score_p2_label.grid(column=5, row=2, sticky=W + E)
        self.draws_label = Label(infos, text="Ties", background="#606060", font=label_font)
        self.draws_label.grid(column=4, row=1, sticky=W + E)
        self.score_draw_label = Label(infos, text="0", background="#606060", font=label_font)
        self.score_draw_label.grid(column=4, row=2, sticky=W + E)

        self.ai1_label = Label(infos, text="AI 1 : ", background="#606060", font=label_font)
        self.ai1_label.grid(column=0, row=2, sticky=W)
        self.ai1 = 1
        ai1_string_var = StringVar()
        ai1_string_var.trace_add("write", self.change_ai1)
        self.ai1_entry = Entry(infos, textvariable=ai1_string_var, width=10)
        self.ai1_entry.insert(0, str(self.ai1))
        self.ai1_entry.grid(column=1, row=2, sticky=W)
        self.ai2_label = Label(infos, text="AI 2 : ", background="#606060", font=label_font)
        self.ai2_label.grid(column=0, row=3, sticky=W)
        self.ai2 = 1
        ai2_string_var = StringVar()
        ai2_string_var.trace_add("write", self.change_ai2)
        self.ai2_entry = Entry(infos, textvariable=ai2_string_var, width=10)
        self.ai2_entry.insert(0, str(self.ai2))
        self.ai2_entry.grid(column=1, row=3, sticky=W)

        # TODO
        # load / save data
        # change ai type label when typing in entry (not only with start button)

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
        infos.pack_propagate(False)
        infos.pack(side=TOP, fill=BOTH)
        line.pack(side=TOP)
        board.pack_propagate(False)
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

    def change_delay(self):
        new_delay = self.delay
        try:
            new_delay = int(self.delay_entry.get())
        except ValueError:
            pass
        if new_delay > 0:
            self.delay = new_delay

    def change_game_number(self):
        game_number = self.game_number
        try:
            game_number = int(self.game_number_entry.get())
        except ValueError:
            pass
        if game_number > 0:
            self.game_number = game_number

    def change_ai1(self, a, b, c):
        ai1 = self.ai1
        try:
            ai1 = int(self.ai1_entry.get())
        except ValueError:
            pass
        if 0 < ai1 < 6:
            self.game.playing = False
            self.start_button["text"] = "Start game"
            self.loop_playing = False

            self.ai1 = ai1
            if ai1 == 1:
                self.game.player1 = Human(1)
            elif ai1 == 2:
                self.game.player1 = Random(1)
            elif ai1 == 3:
                self.game.player1 = StaticAI(1)
            elif ai1 == 4:
                self.game.player1 = MiniMax(1)
            elif ai1 == 5:
                self.game.player1 = ReinforcementLearningAI(1)
            self.ai1_type_label["text"] = self.game.player1.player_type()

    def change_ai2(self, a, b, c):
        ai2 = self.ai2
        try:
            ai2 = int(self.ai2_entry.get())
        except ValueError:
            pass
        if 0 < ai2 < 6:
            self.game.playing = False
            self.start_button["text"] = "Start game"
            self.loop_playing = False

            self.ai1 = ai2
            if ai2 == 1:
                self.game.player2 = Human(2)
            elif ai2 == 2:
                self.game.player2 = Random(2)
            elif ai2 == 3:
                self.game.player2 = StaticAI(2)
            elif ai2 == 4:
                self.game.player2 = MiniMax(2)
            elif ai2 == 5:
                self.game.player2 = ReinforcementLearningAI(2)
            self.ai2_type_label["text"] = self.game.player2.player_type()

    def start_game(self):
        if self.game.playing:
            self.game.playing = False
            self.start_button["text"] = "Start game"
            self.loop_playing = False
        else:
            self.change_delay()
            self.change_game_number()
            self.change_ai1(None, None, None)
            self.change_ai2(None, None, None)
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
                    self.score_p1_label["text"] = str(self.player1_win)
                elif result == GameResult.PLAYER2:
                    self.player2_win += 1
                    self.score_p2_label["text"] = str(self.player2_win)
                elif result == GameResult.DRAW:
                    self.draws += 1
                    self.score_draw_label["text"] = str(self.draws)

                self.current_game_number += 1
                if self.current_game_number >= self.game_number:
                    self.start_button["text"] = "Start game"
                    self.current_game_number = 0
                    self.loop_playing = False
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
