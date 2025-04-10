## players/mcts_player.py

import copy
import random
import math
import time
import concurrent.futures

from .player import Player

class Node:
    def __init__(self, board, parent, move, player_turn):
        self.board = board
        self.parent = parent
        self.move = move  # (token, row, col)
        self.player_turn = player_turn  # 'Order' or 'Loki'
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_terminal(self):
        if self.move is None:
            return False
        return self.board.is_full() or self.board.is_winning_move(self.move[1], self.move[2], self.move[0])

    def expand(self):
        explored_moves = {(child.move, child.player_turn) for child in self.children}
        candidate_moves = select_candidate_moves(self.board, self.player_turn)
        unexplored = [move for move in candidate_moves if (move, self.player_turn) not in explored_moves]

        if not unexplored:
            return None

        move = random.choice(unexplored)
        new_board = copy.deepcopy(self.board)
        new_board.place_token(*move)
        next_turn = 'Order' if self.player_turn == 'Loki' else 'Loki'

        child = Node(new_board, self, move, next_turn)
        self.children.append(child)
        return [child]

    def best_uct_child(self, c_param=1.4):
        best_score = -float('inf')
        best_child = None
        for child in self.children:
            if child.visits == 0:
                score = float('inf')
            else:
                win_rate = child.wins / child.visits
                score = win_rate + c_param * math.sqrt(math.log(self.visits) / child.visits)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child


class MCTSPlayer(Player):
    def __init__(self, player_type, time_limit=1.0):
        super().__init__(player_type)
        self.time_limit = time_limit

    def get_move(self, board):
        immediate = self.immediate_win_or_block(board, self.player_type)
        if immediate:
            return immediate

        root = Node(copy.deepcopy(board), None, None, self.player_type)
        end_time = time.time() + self.time_limit

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            while time.time() < end_time:
                futures.append(executor.submit(self.run_simulation, root))
            concurrent.futures.wait(futures)

        best_child = max(root.children, key=lambda n: n.visits, default=None)
        return best_child.move if best_child else random.choice([
            (token, row, col)
            for (row, col) in board.get_legal_moves()
            for token in ['X', 'O']
        ])

    def run_simulation(self, root):
        node = self.select(root)
        if node and not node.is_terminal():
            children = node.expand()
            if children:
                node = random.choice(children)
        result = self.simulate(node)
        self.backpropagate(node, result)

    def select(self, node):
        while not node.is_terminal() and node.children:
            next_node = node.best_uct_child()
            if not next_node:
                break
            node = next_node
        return node

    def simulate(self, node):
        temp_board = copy.deepcopy(node.board)
        current_player = node.player_turn
        while not temp_board.is_full():
            candidate_moves = select_candidate_moves(temp_board, current_player)
            if not candidate_moves:
                break
            move = random.choice(candidate_moves)
            temp_board.place_token(*move)
            if temp_board.is_winning_move(move[1], move[2], move[0]):
                return 1 if (current_player == 'Thor' and move[0] == 'X') or (current_player == 'Loki' and move[0] == 'O') else 0
            current_player = 'Thor' if current_player == 'Loki' else 'Loki'
        return 0.5  # Draw

    def backpropagate(self, node, result):
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent

    def immediate_win_or_block(self, board, player_type):
        legal_moves = board.get_legal_moves()
        for token in ['X', 'O']:
            for row, col in legal_moves:
                temp_board = copy.deepcopy(board)
                temp_board.place_token(token, row, col)
                if temp_board.is_winning_move(token, row, col):
                    if (player_type == 'Thor' and token == 'X') or (player_type == 'Loki' and token == 'O'):
                        return (token, row, col)
                    elif (player_type == 'Loki' and token == 'X') or (player_type == 'Thor' and token == 'O'):
                        return (token, row, col)
        return None


def line_potential(board, row, col, token):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    max_line = 1
    for dx, dy in directions:
        count = 1
        for dir in [1, -1]:
            x, y = row, col
            while 0 <= x + dx * dir < board.size and 0 <= y + dy * dir < board.size and board.grid[x + dx * dir][y + dy * dir] == token:
                count += 1
                x += dx * dir
                y += dy * dir
        max_line = max(max_line, count)
    return max_line


def disrupt_potential(board, row, col):
    opponent_tokens = ['X', 'O']
    max_threat = 1
    for token in opponent_tokens:
        threat = line_potential(board, row, col, token)
        max_threat = max(max_threat, threat)
    return max_threat


def select_candidate_moves(board, player_type):
    moves = board.get_legal_moves()
    move_scores = []
    for row, col in moves:
        for token in ['X', 'O']:
            if player_type == 'Thor':
                score = line_potential(board, row, col, token)
            else:
                score = disrupt_potential(board, row, col)
            move_scores.append(((token, row, col), score))

    move_scores.sort(key=lambda x: x[1], reverse=True)
    return [move for move, _ in move_scores[:5]]
