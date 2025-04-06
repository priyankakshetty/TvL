from .player import Player
from game.board import Board
import random


class RandomPlayer(Player):

    def get_move(self, board: Board):
        valid_moves = board.get_valid_moves()

        for token in self.tokens:
            for row, col in valid_moves:
                if board.is_winning_move(token, row, col):
                    if self.player_type == "Thor":
                        return token, row, col  # Winning move
                    elif self.player_type == "Loki":
                        return token, row, col  # Block win

        token = random.choice(self.tokens)
        row, col = random.choice(valid_moves)
        return token, row, col
