import random
from Chess import Piece


class AIPlayer:
    def __init__(self, color):
        """
        Inicjalizuje gracza AI z określonym kolorem.

        :param color: Kolor gracza ('white' lub 'black')
        """
        self.color = color

    def choose_move(self, chess_board):
        """
        Wybiera najlepszy ruch dla gracza AI na podstawie oceny ruchów.

        :param chess_board: Obiekt reprezentujący planszę szachową
        :return: Krotka zawierająca współrzędne (początkowe, docelowe) ruchu lub None, jeśli brak ruchów
        """
        all_moves = self._get_all_moves(chess_board)

        if not all_moves:
            return None

        # Ocena każdego ruchu
        evaluated_moves = [(move, self._evaluate_move(move, chess_board)) for move in all_moves]

        # Wybierz ruch z najwyższą oceną
        best_move = max(evaluated_moves, key=lambda x: x[1])[0]

        return best_move

    def _get_all_moves(self, chess_board):
        """
        Zbiera wszystkie możliwe ruchy dla aktualnego gracza.

        :param chess_board: Obiekt reprezentujący planszę szachową
        :return: Lista dostępnych ruchów jako krotki ((start, end))
        """
        moves = []
        for row in range(8):
            for col in range(8):
                piece = chess_board.board[row][col]
                if isinstance(piece, Piece) and piece.color == self.color:
                    piece_moves = piece.get_available_moves(chess_board.board)
                    for move in piece_moves:
                        end_row, end_col = move
                        # Sprawdzenie, czy ruch zbijający jest możliwy
                        if isinstance(chess_board.board[end_row][end_col], Piece) and chess_board.board[end_row][
                            end_col].color != self.color:
                            moves.append(((row, col), move))
                        elif chess_board.board[end_row][end_col] == '.':
                            moves.append(((row, col), move))
        return moves

    def _evaluate_move(self, move, chess_board):
        """
        Ocena ruchu na podstawie prostych heurystyk.

        :param move: Ruch do oceny (krotka ((start, end)))
        :param chess_board: Obiekt reprezentujący planszę szachową
        :return: Wartość oceny ruchu
        """
        start_pos, end_pos = move
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Wartość oceny
        score = 0

        # Pobierz pionka, który wykonuje ruch
        piece = chess_board.board[start_row][start_col]

        # Pobierz docelowy pionek
        target_piece = chess_board.board[end_row][end_col]

        # Ocena na podstawie wartości pionka
        piece_value = self._get_piece_value(piece)
        score += piece_value

        # Dodaj wartość za ruch, który zjada przeciwnika
        if isinstance(target_piece, Piece) and target_piece.color != self.color:
            target_piece_value = self._get_piece_value(target_piece)
            score += target_piece_value * 10  # Zwiększamy wagę zbijania przeciwnika

        return score

    def _get_piece_value(self, piece):
        """
        Zwraca wartość pionka na podstawie jego typu.

        :param piece: Pionek, którego wartość jest oceniana
        :return: Wartość pionka
        """
        piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 15  # Król nie ma przypisanej wartości w tym prostym przykładzie
        }
        return piece_values.get(piece.__class__.__name__.lower(), 0)
