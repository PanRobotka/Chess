import math
import random
from Chess import Piece
from Chess import ChessBoard, Piece, Pawn, King, Queen, Rook, Bishop, Horse

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
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_game(self, moves):
        game_data = {
            "moves": [],
            "evaluations": []
        }
        for i, move in enumerate(moves):
            player = "white" if i % 2 == 0 else "black"
            game_data["moves"].append({
                "move_number": i // 2 + 1,
                "player": player,
                "from": move['start'],
                "to": move['end'],
                "board_state": move['board_state']
            })
            if 'evaluation' in move:
                game_data["evaluations"].append({
                    "move_number": i // 2 + 1,
                    "player": player,
                    "evaluation": move['evaluation']
                })

        self.history.append(game_data)
        self.save_history()

    def get_most_common_moves(self, board_state):
        move_counts = {}
        for game in self.history:
            for move in game['moves']:
                if move['board_state'] == board_state:
                    move_key = (tuple(move['from']), tuple(move['to']))
                    move_counts[move_key] = move_counts.get(move_key, 0) + 1
        return sorted(move_counts.items(), key=lambda x: x[1], reverse=True)

    def get_advanced_move_suggestions(self, board_state):
        move_counts = {}
        move_evaluations = {}

        for game in self.history:
            for move in game['moves']:
                if move['board_state'] == board_state:
                    move_key = (tuple(move['from']), tuple(move['to']))
                    move_counts[move_key] = move_counts.get(move_key, 0) + 1
                    if move_key not in move_evaluations:
                        move_evaluations[move_key] = []
                    move_evaluations[move_key].append(
                        self._get_move_evaluation(game, move['move_number'], move['player']))

        # Calculate average evaluation for each move
        move_averages = {move: sum(evals) / len(evals) for move, evals in move_evaluations.items()}

        # Sort by the most frequent moves and then by the best average evaluation
        sorted_moves = sorted(move_counts.items(), key=lambda x: (x[1], move_averages.get(x[0], 0)), reverse=True)
        return sorted_moves

    def _get_move_evaluation(self, game, move_number, player):
        evaluations = [eval['evaluation'] for eval in game['evaluations'] if
                       eval['move_number'] == move_number and eval['player'] == player]
        return evaluations[0] if evaluations else 0

    def print_game_history(self):
        for i, game in enumerate(self.history):
            print(f"Partia {i + 1}")
            for j in range(0, len(game['moves']), 2):
                white_move = game['moves'][j]
                black_move = game['moves'][j + 1] if j + 1 < len(game['moves']) else None

                white_str = f"{white_move['move_number']}. {white_move['from']} -> {white_move['to']}"
                black_str = f"{black_move['from']} -> {black_move['to']}" if black_move else ""

                print(f"{white_str:<30} {black_str}")
            print("\n")


class AIPlayer:
    def __init__(self, color):
        self.color = color
        self.opponent_color = 'black' if color == 'white' else 'white'
        self.MAX_DEPTH = 3
        self.game_history = GameHistory()
        self.current_game_moves = []

    def choose_move(self, chess_board):
        board_state = self.get_board_state(chess_board)
        common_moves = self.game_history.get_most_common_moves(board_state)

        if common_moves and random.random() < 0.2:  # 20% szans na wybranie ruchu z historii
            best_move = common_moves[0][0]
        else:
            # Jeśli nie wybrano ruchu z historii, użyj algorytmu Minimax
            best_move = self.minimax_choose_move(chess_board)

        # Ocena pozycji po wykonaniu ruchu
        chess_board.move_piece_ai(best_move[0], best_move[1])
        evaluation = self.evaluate_board(chess_board)
        chess_board.undo_move()

        # Zapisz wykonany ruch wraz z oceną
        self.current_game_moves.append({
            'board_state': board_state,
            'start': best_move[0],
            'end': best_move[1],
            'evaluation': evaluation
        })

        return best_move

    def end_game(self):
        self.game_history.add_game(self.current_game_moves)
        self.current_game_moves = []
        self.game_history.print_game_history()  # Dodaj tę linię, aby wyświetlić historię gry po jej zakończeniu
        print("Gra zakończona i zapisana w historii")

    def get_board_state(self, chess_board):
        return str([[str(piece) for piece in row] for row in chess_board.board])

    def get_advanced_move_suggestions(self, board_state):
        move_counts = {}
        move_evaluations = {}

        for game in self.history:
            for move in game['moves']:
                if move['board_state'] == board_state:
                    move_key = (tuple(move['from']), tuple(move['to']))
                    move_counts[move_key] = move_counts.get(move_key, 0) + 1
                    if move_key not in move_evaluations:
                        move_evaluations[move_key] = []
                    move_evaluations[move_key].append(
                        self._get_move_evaluation(game, move['move_number'], move['player']))

        # Calculate average evaluation for each move
        move_averages = {move: sum(evals) / len(evals) for move, evals in move_evaluations.items()}

        # Sort by the most frequent moves and then by the best average evaluation
        sorted_moves = sorted(move_counts.items(), key=lambda x: (x[1], move_averages.get(x[0], 0)), reverse=True)
        return sorted_moves

    def minimax_choose_move(self, chess_board):
        best_score = -math.inf
        best_move = None
        all_moves = self._get_all_moves(chess_board)

        for move in all_moves:
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
        control_center = 0
        king_safety = 0

        for row in range(8):
            for col in range(8):
                piece = chess_board.board[row][col]
                if isinstance(piece, Piece):
                    value = piece_values[piece.__class__.__name__.lower()]
                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value

        # Dodajemy bonus za kontrolowanie centrum planszy
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for row, col in center_squares:
            if isinstance(chess_board.board[row][col], Piece):
                if chess_board.board[row][col].color == self.color:
                    control_center += 0.5
                else:
                    control_center -= 0.5
        score += control_center

        # Ocena bezpieczeństwa króla
        king_position = self.find_king_position(chess_board)
        if king_position:
            king_row, king_col = king_position
            safety_score = self.evaluate_king_safety(king_row, king_col, chess_board)
            king_safety += safety_score
        score += king_safety

        return score

    def find_king_position(self, chess_board):
        for row in range(8):
            for col in range(8):
                piece = chess_board.board[row][col]
                if isinstance(piece, King) and piece.color == self.color:
                    return (row, col)
        return None

    def evaluate_king_safety(self, row, col, chess_board):
        # Przykładowa funkcja oceniająca bezpieczeństwo króla (można rozbudować)
        threats = 0
        for r in range(max(0, row - 1), min(8, row + 2)):
            for c in range(max(0, col - 1), min(8, col + 2)):
                target_piece = chess_board.board[r][c]
                if isinstance(target_piece, Piece) and target_piece.color != self.color:
                    threats += 0.5
        return -threats

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