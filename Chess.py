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

    def get_available_moves(self, board):
        available_moves = []
        current_row, current_col = self.get_position()

        # Sprawdź ruch do przodu o jedno pole
        if board[current_row + self.direction][current_col] == '.':
            available_moves.append((current_row + self.direction, current_col))

            # Sprawdź ruch o dwa pola, jeśli pionek znajduje się na swoim wierszu startowym i pole bezpośrednio przed nim jest puste
            if current_row == self.starting_row and board[current_row + 2 * self.direction][current_col] == '.':
                available_moves.append((current_row + 2 * self.direction, current_col))

        # Sprawdź możliwe bicia w skos
        for col_offset in [-1, 1]:
            target_row = current_row + self.direction
            target_col = current_col + col_offset
            if 0 <= target_row < 8 and 0 <= target_col < 8:
                target_piece = board[target_row][target_col]
                if target_piece != '.' and target_piece.get_color() != self.color:
                    available_moves.append((target_row, target_col))

        return available_moves


# Wieża
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_available_moves(self, board):
        pass


# Koń
class Horse(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_available_moves(self, board):
        pass


# Goniec
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_available_moves(self, board):
        pass


# Królowa
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_available_moves(self, board):
        pass


# Król
class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_available_moves(self, board):
        pass


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
