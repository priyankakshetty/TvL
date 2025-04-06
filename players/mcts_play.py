## players/mcts_player.py

import copy
import random
import math
import time

from .player import Player

class Node:
    def __init__(self, board, parent, move, player_turn):
        self.board = board
        self.parent = parent
        self.move = move  # (token, row, col)
        self.player_turn = player_turn  # 'Thor' or 'Loki'
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_terminal(self):
        if self.move is None:
            return False
        return self.board.is_full() or self.board.is_winning_move(*self.move)

    def expand(self):
        explored_moves = {(child.move, child.player_turn) for child in self.children}
        legal_moves = self.board.get_legal_moves()
        unexplored = [(token, row, col) for (row, col) in legal_moves 
                      for token in ['X', 'O'] if ((token, row, col), self.player_turn) not in explored_moves]

        if not unexplored:
            return None

        move = random.choice(unexplored)
        new_board = copy.deepcopy(self.board)
        new_board.place_token(move[0], move[1], move[2])
        next_turn = 'Thor' if self.player_turn == 'Loki' else 'Loki'

        child = Node(new_board, self, move, next_turn)
        self.children.append(child)
        return child

    def best_uct_child(self, exploration=True):
        C = math.sqrt(2) if exploration else 0
        best_score = -float('inf')
        best_child = None

        for child in self.children:
            if child.visits == 0:
                return child
            exploitation = child.wins / child.visits
            exploration_term = C * math.sqrt(math.log(self.visits) / child.visits)
            score = exploitation + exploration_term

            if score > best_score:
                best_score = score
                best_child = child

        return best_child


class MCTSPlayer(Player):
    def get_move(self, board):
        move = self.immediate_win_or_block(board)
        if move:
            return move

        return self._mcts(board)

    def immediate_win_or_block(self, board):
        for (row, col) in board.get_legal_moves():
            for token in ['X', 'O']:
                temp_board = copy.deepcopy(board)
                temp_board.place_token(token, row, col)
                if temp_board.is_winning_move(token, row, col):
                    if self.player_type == 'Thor' and token == 'X':
                        return token, row, col
                    if self.player_type == 'Loki' and token == 'O':
                        return token, row, col
        return None

    def _mcts(self, board):
        root = Node(copy.deepcopy(board), None, None, self.player_type)
        end_time = time.time() + 1.0  # 1 sec search budget

        while time.time() < end_time:
            node = self._select(root)
            if not node.is_terminal():
                node = node.expand() or node
            result = self._simulate(node)
            self._backpropagate(node, result)

        best_child = max(root.children, key=lambda c: c.visits, default=None)
        if not best_child:
            token = random.choice(['X', 'O'])
            row, col = random.choice(board.get_legal_moves())
            return (token, row, col)

        return best_child.move

    def _select(self, node):
        while not node.is_terminal() and node.children:
            next_node = node.best_uct_child()
            if next_node is None:
                break
            node = next_node
        return node

    def _simulate(self, node):
        temp_board = copy.deepcopy(node.board)
        player = node.player_turn

        while not temp_board.is_full():
            moves = temp_board.get_legal_moves()
            if not moves:
                print(temp_board.grid)
            move = random.choice(moves)
            token = random.choice(['X', 'O'])
            temp_board.place_token(token, move[0], move[1])
            print(move)
            if temp_board.is_winning_move(token, move[0], move[1]):
                return 1 if (player == 'Thor' and token == 'X') or (player == 'Loki' and token == 'O') else 0
        return 0.5  # Draw

    def _backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent
