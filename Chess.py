import random
import time


class Piece:
    def __init__(self, color, id):
        self.color = color
        self.position = None
        self.id = id

    def get_color(self):
        return self.color

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def get_available_moves(self, board):
        pass

    def __str__(self):
        return self.id


# Pionek
class Pawn(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)
        self.starting_row = 1 if color == 'white' else 6  # Wiersz, z którego pionek może ruszyć o dwa pola
        self.direction = -1 if color == 'white' else 1  # Kierunek poruszania się pionka

    def get_available_moves(self, board):
        pass


# Wieża
class Rook(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        pass


# Koń
class Horse(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        pass


# Goniec
class Bishop(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        pass


# Królowa
class Queen(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        pass


# Król
class King(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        pass


class ChessBoard:
    def __init__(self):
        self.board = [
            ['r1', 'h1', 'b1', 'q', 'k', 'b2', 'h2', 'r2'],
            ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'],
            ['R1', 'H1', 'B1', 'Q', 'K', 'B2', 'H2', 'R2']
        ]
        self.assign_pieces()

    def display(self):
        for row in self.board:
            print(" ".join(str(piece) for piece in row))

    def move_piece(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        piece = self.board[start_row][start_col]  # Pobierz figurę z pozycji początkowej
        self.board[start_row][start_col] = '.'  # Usuń figurę z pozycji początkowej
        self.board[end_row][end_col] = piece  # Umieść figurę na nowej pozycji

    def assign_pieces(self):
        for i in range(8):
            for j in range(8):
                piece_code = self.board[i][j]
                if piece_code != '.':
                    color = 'white' if piece_code.isupper() else 'black'
                    piece_type = piece_code.upper()[0]
                    if piece_type == 'P':
                        piece = Pawn(color, piece_code)
                    elif piece_type == 'R':
                        piece = Rook(color, piece_code)
                    elif piece_type == 'H':
                        piece = Horse(color, piece_code)
                    elif piece_type == 'B':
                        piece = Bishop(color, piece_code)
                    elif piece_type == 'Q':
                        piece = Queen(color, piece_code)
                    elif piece_type == 'K':
                        piece = King(color, piece_code)
                    piece.set_position((i, j))
                    self.board[i][j] = piece
                    # Printuje potwierdzenie stworzenia instancji dla każdej figury z tabeli, podaje jej pozycję oraz id ##########################

    #                    print(
    #                        f"Utworzono instancję {piece.__class__.__name__} o kolorze {piece.get_color()} z ID {piece.id} na pozycji {piece.get_position()}")

    def print_piece_positions(self):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if isinstance(piece, Piece):
                    print(
                        f"Figura {piece.__class__.__name__} o kolorze {piece.get_color()} jest na pozycji {piece.get_position()}")


# Utwórz instancję szachownicy
chess_board = ChessBoard()

# Wyświetl planszę przed ruchem
print("Plansza przed ruchem:")
chess_board.display()
# wyświetl pozycję każdego pionka na planszy
# chess_board.print_piece_positions()
# w taki sposób odwołujesz się do nowo stworzonych instancji. Poniżej przykładowy kod gdzie szukasz informacji o figurze położonej na współrzędnych 0,0
piece_at_0_0 = chess_board.board[0][0]
print(piece_at_0_0)
########################################################################################################################
                                            # Kod nie używany, ale działa ;)
########################################################################################################################
# # Wykonaj ruch pionka z pozycji (6, 0) do (5, 0)
# start_position = (6, 0)
# end_position = (5, 0)
# chess_board.move_piece(start_position, end_position)
#
# Wyświetl planszę po ruchu
# print("\nPlansza po ruchu:")
# chess_board.display()
