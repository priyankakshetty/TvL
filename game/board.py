# board.py

class Board:
    WIN_LENGTH = 4  # Change to 4 if needed — applies globally to all instances

    def __init__(self, size=6):
        self.size = size
        self.grid = [["" for _ in range(size)] for _ in range(size)]
        self.empty_space = ''

    def len(self):
        return (len(self.grid), len(self.grid[0]))

    def print_board(self):
        for row in self.grid:
            print(" | ".join(cell if cell else " " for cell in row))
        print()

    def is_empty(self, row, col):
        return self.grid[row][col] == ""

    def get_valid_moves(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.is_empty(r, c)]

    def place_token(self, token, row, col):
        if self.is_empty(row, col):
            self.grid[row][col] = token
            return True
        return False

    def is_winning_move(self, token, row, col):
        directions = [
            (1, 0),   # vertical
            (0, 1),   # horizontal
            (1, 1),   # diagonal ↘
            (1, -1),  # diagonal ↙
        ]
        for dr, dc in directions:
            count = 1  # Start with the placed token

            for dir in [1, -1]:  # Forward and backward
                r, c = row, col
                for _ in range(self.WIN_LENGTH - 1):
                    r += dr * dir
                    c += dc * dir
                    if 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == token:
                        count += 1
                    else:
                        break

            if count >= self.WIN_LENGTH:
                return True

        return False

    def is_full(self):
        return all(cell for row in self.grid for cell in row)

    def get_legal_moves(self):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == self.empty_space:
                    moves.append((r, c))
        return moves

