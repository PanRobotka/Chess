import random
import time


class Piece:
    def __init__(self, color):
        self.color = color
        self.position = None

    def get_color(self):
        return self.color

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def get_available_moves(self, board):
        pass


# Pionek
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.starting_row = 1 if color == 'white' else 6  # Wiersz, z którego pionek może ruszyć o dwa pola
        self.direction = -1 if color == 'white' else 1  # Kierunek poruszania się pionka



# Wieża
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)



# Koń
class Horse(Piece):
    def __init__(self, color):
        super().__init__(color)


# Goniec
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)



# Królowa
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)


# Król
class King(Piece):
    def __init__(self, color):
        super().__init__(color)


class ChessBoard:
    def __init__(self):
        self.board = [
            ['r', 'h', 'b', 'q', 'k', 'b', 'h', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'H', 'B', 'Q', 'K', 'B', 'H', 'R']
        ]

    def display(self):
        for row in self.board:
            print(" ".join(row))

    def move_piece(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        piece = self.board[start_row][start_col]  # Pobierz figurę z pozycji początkowej
        self.board[start_row][start_col] = '.'  # Usuń figurę z pozycji początkowej
        self.board[end_row][end_col] = piece  # Umieść figurę na nowej pozycji

    def print_piece_positions(self):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != '.':
                    print(f"Figura {piece} jest na pozycji ({i}, {j})")


# Przypisanie koloru i instancji do figur
p = Pawn("black")
P = Pawn("white")
h = Horse("black")
H = Horse("white")
b = Bishop("black")
B = Bishop("white")
q = Queen("black")
Q = Queen("white")
k = King("black")
K = King("white")


# Utwórz instancję szachownicy
chess_board = ChessBoard()

# Wyświetl planszę przed ruchem
print("Plansza przed ruchem:")
chess_board.display()
# wyświetl pozycję każdego pionka na planszy
chess_board.print_piece_positions()
# # Wykonaj ruch pionka z pozycji (6, 0) do (5, 0)
# start_position = (6, 0)
# end_position = (5, 0)
# chess_board.move_piece(start_position, end_position)
#
# # Wyświetl planszę po ruchu
# print("\nPlansza po ruchu:")
# chess_board.display()
