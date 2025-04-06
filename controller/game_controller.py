from game.board import Board
from controller import mapping


class GameController:
    def __init__(self, env, p1_logic, p2_logic, player1_role, board_size):
        self.env = env
        self.player1 = None
        self.player2 = None
        self.current_player = None # only need for local

        self.board = Board(size=board_size)

        if env == 'local' and not p2_logic:
            raise ValueError('Player 2 logic should be provided when env is local ')

        self.init_players(p1_logic, p2_logic, player1_role)

    def init_players(self, p1_logic, p2_logic, player1_role):
        self.player1 = mapping.players[p1_logic](player1_role)

        if self.env == 'local':
            if player1_role == 'Thor':
                self.player2 = mapping.players[p2_logic]('Loki')
                self.current_player = self.player1
            else:
                self.player2 = mapping.players[p2_logic]('Thor')
                self.current_player = self.player2

    def run_local(self):
        move_count = 0

        while not self.board.is_full():
            token, row, col = self.current_player.get_move(self.board)

            if self.board.place_token(token, row, col):
                move_count += 1
                print(f"{self.current_player.player_type} places {token} at ({row}, {col})")
                self.board.print_board()

                if self.board.is_winning_move(token, row, col):
                    if self.current_player.player_type == "Thor":
                        print(f"Thor wins in {move_count} moves!")
                        return "Thor"
                    else:
                        print(f"Loki formed a winning line — Thor wins by default.")
                        return "Thor"  # Not a Loki win

                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            else:
                print(f"Invalid move attempted at ({row}, {col})!")

        print("Board full with no 5-in-a-row — Loki wins!")
        return "Loki"

    def run(self):
        if self.env == 'local':
            self.run_local()
        else:
            # ideally self.run_with_apis()
            raise NotImplementedError(f"{self.env} environment is not implemented yet.")
