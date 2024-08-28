import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]
        if ' ' not in self.board:
            return 'Tie'
        return None

    def ai_move(self):
        available_moves = [i for i, spot in enumerate(self.board) if spot == ' ']
        return random.choice(available_moves)

    def get_board_display(self):
        return f"{self.board[0]}|{self.board[1]}|{self.board[2]}\n-+-+-\n{self.board[3]}|{self.board[4]}|{self.board[5]}\n-+-+-\n{self.board[6]}|{self.board[7]}|{self.board[8]}"