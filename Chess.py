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

    def capture_piece(self, board, position):
        target_piece = board[position[0]][position[1]]
        if isinstance(target_piece, Piece):
            print(
                f"Figura {self.__class__.__name__} o kolorze {self.get_color()} zbiła figurę {target_piece.__class__.__name__} o kolorze {target_piece.get_color()}")
            # Usuń zbitą figurę z planszy
            board[position[0]][position[1]] = '.'


# Pionek
class Pawn(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)
        self.direction = -1 if color == 'white' else 1
        self.move_made = False

    def get_available_moves(self, board):
        available_moves = []
        current_row, current_col = self.position

        # Sprawdź możliwe ruchy dla piona w zależności od jego kierunku i czy wykonano już ruch
        if not self.move_made:
            # Możliwe ruchy gdy pion nie wykonał jeszcze ruchu
            if 0 <= current_row + self.direction < 8 and board[current_row + self.direction][current_col] == '.':
                available_moves.append((current_row + self.direction, current_col))
                if board[current_row + 2 * self.direction][current_col] == '.':
                    available_moves.append((current_row + 2 * self.direction, current_col))
            # Sprawdź możliwość zbijania pionka przeciwnika w lewo
            if current_col > 0 and board[current_row + self.direction][current_col - 1] not in ['.', self.color]:
                available_moves.append((current_row + self.direction, current_col - 1))
            # Sprawdź możliwość zbijania pionka przeciwnika w prawo
            if current_col < 7 and board[current_row + self.direction][current_col + 1] not in ['.', self.color]:
                available_moves.append((current_row + self.direction, current_col + 1))
        else:
            # Możliwy ruch gdy pion już wykonał ruch
            if 0 <= current_row + self.direction < 8 and board[current_row + self.direction][current_col] == '.':
                available_moves.append((current_row + self.direction, current_col))
            # Sprawdź możliwość zbijania pionka przeciwnika w lewo
            if current_col > 0 and board[current_row + self.direction][current_col - 1] not in ['.', self.color]:
                available_moves.append((current_row + self.direction, current_col - 1))
            # Sprawdź możliwość zbijania pionka przeciwnika w prawo
            if current_col < 7 and board[current_row + self.direction][current_col + 1] not in ['.', self.color]:
                available_moves.append((current_row + self.direction, current_col + 1))

        # Dodajemy warunek sprawdzający czy pionek porusza się w dobrym kierunku
        return [(row, col) for row, col in available_moves if
                (row - current_row) / abs(row - current_row) == self.direction]

    def move(self):
        self.move_made = True


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
        # print('move piece')
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        piece = self.board[start_row][start_col]  # Pobierz figurę z pozycji początkowej
        ########## Prosty if który sprawdza czy na polu na  które chcesz stanąć nie stoi żadna figura, jeżeli stoi to ją bije ##########
        if isinstance(self.board[end_row][end_col], Piece):
            print('piece type', type(piece), piece)
            piece.capture_piece(self.board, end_pos)

        self.board[start_row][start_col] = '.'  # Usuń figurę z pozycji początkowej
        self.board[end_row][end_col] = piece  # Umieść figurę na nowej pozycji

        # Aktualizacja pozycji figury ( potrzebne do śledzenia figury po ruchu)
        piece.set_position((end_row, end_col))

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
# chess_board = ChessBoard()

# Wyświetl planszę przed ruchem
# print("Plansza przed ruchem:")
# chess_board.display()
# wyświetl pozycję każdego pionka na planszy
# chess_board.print_piece_positions()
# w taki sposób odwołujesz się do nowo stworzonych instancji. Poniżej przykładowy kod gdzie szukasz informacji o figurze położonej na współrzędnych 0,0
# piece_at_0_0 = chess_board.board[0][0]
# print(piece_at_0_0)
########################################################################################################################
# Kod nie używany, ale działa ;)
########################################################################################################################
###### TESTUJE TUTAJ ZBIJANIE PIONKA NA PODSTAWIE WEJŚCIU W NIEGO ORAZ SPRAWDZAM CZY RUCH ZOSTAŁ Z AKTUALIZOWANY ###### !!!!!!!!! WAŻNE
# Wykonaj ruch pionka z pozycji (6, 0) do (1, 0)
# start_position = (6, 0)
# end_position = (1, 0)
# chess_board.move_piece(start_position, end_position)
# Wyświetl planszę po ruchu
# print("\nPlansza po ruchu:")
# chess_board.display()
# start_position = (1, 0)
# end_position = (2, 0)
# chess_board.move_piece(start_position, end_position)
# print("\nPlansza po ruchu:")
# chess_board.display()
# chess_board.print_piece_positions()
