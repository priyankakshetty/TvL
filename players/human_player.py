from .player import Player
from game.board import Board

class HumanPlayer(Player):

    def get_move(self, board:Board):
        row_size, col_size = board.len()
        print(f'Choose your next move as {self.player_type} in board with row={row_size} and col={col_size}')
        row = int(input('Row: '))
        col = int(input('Col: '))
        token = input('Token X or O: ')

        return token, row, col