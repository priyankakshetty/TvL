from abc import ABC, abstractmethod
from game.board import Board


class Player(ABC):

    def __init__(self, player_type: str):
        self.player_type = player_type
        self.tokens = ['X', 'O']

    @abstractmethod
    def get_move(self, board:Board):
        pass
