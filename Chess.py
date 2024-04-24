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
            available_moves += self.check_initial_moves(board, current_row, current_col)
        else:
            available_moves += self.check_subsequent_moves(board, current_row, current_col)

        # Dodajemy warunek sprawdzający czy pionek porusza się w dobrym kierunku
        return [(row, col) for row, col in available_moves if
                (row - current_row) / abs(row - current_row) == self.direction]

    def check_initial_moves(self, board, current_row, current_col):
        initial_moves = []
        if 0 <= current_row + self.direction < 8 and board[current_row + self.direction][current_col] == '.':
            initial_moves.append((current_row + self.direction, current_col))
            if board[current_row + 2 * self.direction][current_col] == '.':
                initial_moves.append((current_row + 2 * self.direction, current_col))
        # Sprawdź możliwość zbijania pionka przeciwnika w lewo
        if current_col > 0 and board[current_row + self.direction][current_col - 1] not in ['.', self.color]:
            initial_moves.append((current_row + self.direction, current_col - 1))
        # Sprawdź możliwość zbijania pionka przeciwnika w prawo
        if current_col < 7 and board[current_row + self.direction][current_col + 1] not in ['.', self.color]:
            initial_moves.append((current_row + self.direction, current_col + 1))
        return initial_moves

    def check_subsequent_moves(self, board, current_row, current_col):
        subsequent_moves = []
        if 0 <= current_row + self.direction < 8 and board[current_row + self.direction][current_col] == '.':
            subsequent_moves.append((current_row + self.direction, current_col))
        # Sprawdź możliwość zbijania pionka przeciwnika w lewo
        if current_col > 0:
            target_piece = board[current_row + self.direction][current_col - 1]
            if target_piece != '.' and target_piece.color != self.color:
                subsequent_moves.append((current_row + self.direction, current_col - 1))
        # Sprawdź możliwość zbijania pionka przeciwnika w prawo
        if current_col < 7:
            target_piece = board[current_row + self.direction][current_col + 1]
            if target_piece != '.' and target_piece.color != self.color:
                subsequent_moves.append((current_row + self.direction, current_col + 1))
        return subsequent_moves

    def move(self):
        self.move_made = True


# Wieża
class Rook(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        available_moves = []

        # Sprawdź ruchy w kierunku pionowym
        for i in range(self.position[0] + 1, 8):
            if board[i][self.position[1]] in ['.', self.color]:
                available_moves.append((i, self.position[1]))
                if board[i][self.position[1]] == self.color:
                    break
            else:
                if board[i][self.position[1]].color != self.color:  # Jeśli pole zajęte przez przeciwną figurę
                    available_moves.append((i, self.position[1]))
                break

        for i in range(self.position[0] - 1, -1, -1):
            if board[i][self.position[1]] in ['.', self.color]:
                available_moves.append((i, self.position[1]))
                if board[i][self.position[1]] == self.color:
                    break
            else:
                if board[i][self.position[1]].color != self.color:
                    available_moves.append((i, self.position[1]))
                break

        # Sprawdź ruchy w kierunku poziomym
        for j in range(self.position[1] + 1, 8):
            if board[self.position[0]][j] in ['.', self.color]:
                available_moves.append((self.position[0], j))
                if board[self.position[0]][j] == self.color:
                    break
            else:
                if board[self.position[0]][j].color != self.color:
                    available_moves.append((self.position[0], j))
                break

        for j in range(self.position[1] - 1, -1, -1):
            if board[self.position[0]][j] in ['.', self.color]:
                available_moves.append((self.position[0], j))
                if board[self.position[0]][j] == self.color:
                    break
            else:
                if board[self.position[0]][j].color != self.color:
                    available_moves.append((self.position[0], j))
                break

        return available_moves


# Koń
class Horse(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        available_moves = []
        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for direction in directions:
            new_row = self.position[0] + direction[0]
            new_col = self.position[1] + direction[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board[new_row][new_col]
                if target_piece == '.' or target_piece.color != self.color:
                    available_moves.append((new_row, new_col))
        return available_moves


# Goniec
class Bishop(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        available_moves = []

        # Sprawdź przekątną w prawo-górę
        for i, j in zip(range(self.position[0] - 1, -1, -1), range(self.position[1] + 1, 8)):
            if board[i][j] in ['.', self.color]:
                available_moves.append((i, j))
                if board[i][j] == self.color:
                    break
            else:
                if board[i][j].color != self.color:
                    available_moves.append((i, j))
                break

        # Sprawdź przekątną w lewo-górę
        for i, j in zip(range(self.position[0] - 1, -1, -1), range(self.position[1] - 1, -1, -1)):
            if board[i][j] in ['.', self.color]:
                available_moves.append((i, j))
                if board[i][j] == self.color:
                    break
            else:
                if board[i][j].color != self.color:
                    available_moves.append((i, j))
                break

        # Sprawdź przekątną w prawo-dół
        for i, j in zip(range(self.position[0] + 1, 8), range(self.position[1] + 1, 8)):
            if board[i][j] in ['.', self.color]:
                available_moves.append((i, j))
                if board[i][j] == self.color:
                    break
            else:
                if board[i][j].color != self.color:
                    available_moves.append((i, j))
                break

        # Sprawdź przekątną w lewo-dół
        for i, j in zip(range(self.position[0] + 1, 8), range(self.position[1] - 1, -1, -1)):
            if board[i][j] in ['.', self.color]:
                available_moves.append((i, j))
                if board[i][j] == self.color:
                    break
            else:
                if board[i][j].color != self.color:
                    available_moves.append((i, j))
                break

        return available_moves


# Królowa
class Queen(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        rook_moves = Rook.get_available_moves(self, board)
        bishop_moves = Bishop.get_available_moves(self,board)
        return rook_moves + bishop_moves


# Król
class King(Piece):
    def __init__(self, color, id):
        super().__init__(color, id)

    def get_available_moves(self, board):
        available_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            new_row = self.position[0] + direction[0]
            new_col = self.position[1] + direction[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board[new_row][new_col]
                if target_piece == '.' or target_piece.color != self.color:
                    available_moves.append((new_row, new_col))
        return available_moves


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