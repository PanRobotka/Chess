import math
import random
from Chess import Piece

import json
import os


class GameHistory:
    def __init__(self, filename='game_history.json'):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.history = self.load_history()

    def load_history(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    return json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding {self.filename}. Starting with empty history.")
        except Exception as e:
            print(f"Error loading history: {e}")
        return []

    def save_history(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.history, f)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_game(self, moves):
        self.history.append(moves)
        self.save_history()

    def get_most_common_moves(self, board_state):
        move_counts = {}
        for game in self.history:
            for move in game:
                if move['board_state'] == board_state:
                    move_key = (tuple(move['start']), tuple(move['end']))
                    move_counts[move_key] = move_counts.get(move_key, 0) + 1
        return sorted(move_counts.items(), key=lambda x: x[1], reverse=True)


class AIPlayer:
    def __init__(self, color):
        self.color = color
        self.opponent_color = 'black' if color == 'white' else 'white'
        self.MAX_DEPTH = 2
        self.game_history = GameHistory()
        self.current_game_moves = []

    def choose_move(self, chess_board):
        board_state = self.get_board_state(chess_board)
        common_moves = self.game_history.get_most_common_moves(board_state)

        if common_moves and random.random() < 0.3:  # 30% szans na wybranie ruchu z historii
            best_move = common_moves[0][0]
        else:
            # Jeśli nie wybrano ruchu z historii, użyj algorytmu Minimax
            best_move = self.minimax_choose_move(chess_board)

        # Zapisz wykonany ruch
        self.current_game_moves.append({
            'board_state': board_state,
            'start': best_move[0],
            'end': best_move[1]
        })

        return best_move

    def end_game(self):
        self.game_history.add_game(self.current_game_moves)
        self.current_game_moves = []
        print("Gra zakończona i zapisana w historii")

    def get_board_state(self, chess_board):
        return str([[str(piece) for piece in row] for row in chess_board.board])

    def minimax_choose_move(self, chess_board):
        best_score = -math.inf
        best_move = None
        for move in self._get_all_moves(chess_board):
            chess_board.move_piece_ai(move[0], move[1])
            score = self.minimax(chess_board, self.MAX_DEPTH, -math.inf, math.inf, False)
            chess_board.undo_move()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, chess_board, depth, alpha, beta, maximizing_player):
        if depth == 0 or chess_board.is_king_dead('white') or chess_board.is_king_dead('black'):
            return self.evaluate_board(chess_board)

        if maximizing_player:
            max_eval = -math.inf
            for move in self._get_all_moves(chess_board):
                chess_board.move_piece_ai(move[0], move[1])
                eval = self.minimax(chess_board, depth - 1, alpha, beta, False)
                chess_board.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self._get_all_moves(chess_board):
                chess_board.move_piece_ai(move[0], move[1])
                eval = self.minimax(chess_board, depth - 1, alpha, beta, True)
                chess_board.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, chess_board):
        score = 0
        piece_values = {'pawn': 1, 'horse': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 0}

        for row in chess_board.board:
            for piece in row:
                if isinstance(piece, Piece):
                    value = piece_values[piece.__class__.__name__.lower()]
                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value

        return score

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
            'horse': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 15  # Król nie ma przypisanej wartości w tym prostym przykładzie
        }
        return piece_values.get(piece.__class__.__name__.lower(), 0)
