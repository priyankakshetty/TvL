## players/mcts_player2.py

import copy
import random
import math
import time
import concurrent.futures

from .base import Player

# Node class remains exactly same as MCTSPlayer

# Updated select_candidate_moves for Chaos to prefer isolation
def select_candidate_moves(board, player_type):
    moves = board.get_legal_moves()
    move_scores = []

    for row, col in moves:
        for token in ['X', 'O']:
            if player_type == 'Order':
                score = line_potential(board, row, col, token)
            else:  # Chaos
                threat = disrupt_potential(board, row, col)
                isolation = -sum(1 for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]
                                 if 0 <= row + dx < board.size and 0 <= col + dy < board.size and board.grid[row + dx][col + dy] != '.')
                score = threat + isolation

            move_scores.append(((token, row, col), score))

    move_scores.sort(key=lambda x: x[1], reverse=True)
    return [move for move, _ in move_scores[:5]]

# line_potential, disrupt_potential, Node class and rest of MCTSPlayer logic remains as in your current file

# Only select_candidate_moves is modified for Chaos smart isolation

# Rest of the MCTSPlayer2 implementation stays same to allow fair A/B testing
