import random
import numpy as np
import copy

from players.player import *


class ReinforcementLearningAI(Player):
    def __init__(self, current_player, exp_rate=0.3):
        super().__init__(current_player)
        self.states = []
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}

    def play(self, board) -> Tuple[int, int]:
        # Play
        list_possible_moves = possible_moves(board)
        position = None

        if random.random() <= self.exp_rate:
            position = random.choice(list_possible_moves)
        else:
            max_value = -999

            for move in list_possible_moves:
                board[move[1]][move[0]] = self.current_player
                next_board_hash = self._get_hash(board)
                board[move[1]][move[0]] = 0

                if self.states_value.get(next_board_hash) is None:
                    value = 0
                else:
                    value = self.states_value.get(next_board_hash)
                if value >= max_value:
                    max_value = value  # TODO random
                    position = move

        # Train
        board[position[1]][position[0]] = self.current_player
        self.states.append(self._get_hash(board))
        board[position[1]][position[0]] = 0

        return position

    def _get_hash(self, board) -> str:  # TODO use symetries
        str_hash = ""
        for i in range(3):
            for j in range(3):
                str_hash += str(board[i][j])
        return str_hash

    def player_type(self):
        return "Reinforcement learning AI"

    def feed_reward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset_ai(self):
        self.states = []


def possible_moves(board):
    list_possible_moves = list()
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                list_possible_moves.append((j, i))
    return list_possible_moves
