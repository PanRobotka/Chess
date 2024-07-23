import math
import random
import json
import os
from Chess import Piece, ChessBoard, Pawn, King, Queen, Rook, Bishop, Horse


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

        move_averages = {move: sum(evals) / len(evals) for move, evals in move_evaluations.items()}
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
            best_move = self.minimax_choose_move(chess_board)

        chess_board.move_piece_ai(best_move[0], best_move[1])
        evaluation = self.evaluate_board(chess_board)
        chess_board.undo_move()

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
        self.game_history.print_game_history()
        print("Gra zakończona i zapisana w historii")

    def get_board_state(self, chess_board):
        return str([[str(piece) for piece in row] for row in chess_board.board])

    def minimax_choose_move(self, chess_board):
        best_score = -math.inf
        best_move = None
        all_moves = self._get_all_moves(chess_board)
        max_depth = self.dynamic_depth(chess_board)

        for move in all_moves:
            chess_board.move_piece_ai(move[0], move[1])
            score = self.minimax(chess_board, max_depth, -math.inf, math.inf, False)
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

    def dynamic_depth(self, chess_board):
        num_pieces = sum(isinstance(piece, Piece) for row in chess_board.board for piece in row)
        if num_pieces > 20:
            return 3  # Early game
        elif num_pieces > 10:
            return 4  # Middle game
        else:
            return 5  # End game

    def evaluate_board(self, chess_board):
        score = 0
        piece_values = {'pawn': 1, 'horse': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 0}

        for row in range(8):
            for col in range(8):
                piece = chess_board.board[row][col]
                if isinstance(piece, Piece):
                    value = piece_values[piece.__class__.__name__.lower()]
                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value

        # Additional evaluation metrics
        score += self.evaluate_mobility(chess_board)
        score += self.evaluate_control_center(chess_board)
        score += self.evaluate_king_safety(chess_board)

        return score

    def evaluate_mobility(self, chess_board):
        mobility_score = 0
        for row in range(8):
            for col in range(8):
                piece = chess_board.board[row][col]
                if isinstance(piece, Piece) and piece.color == self.color:
                    piece_moves = piece.get_available_moves(chess_board.board)
                    mobility_score += len(piece_moves)
        return mobility_score

    def evaluate_control_center(self, chess_board):
        center_pieces = [(3, 3), (3, 4), (4, 3), (4, 4)]
        control_center_score = 0
        for row, col in center_pieces:
            piece = chess_board.board[row][col]
            if isinstance(piece, Piece):
                if piece.color == self.color:
                    control_center_score += 1
                else:
                    control_center_score -= 1
        return control_center_score

    def evaluate_king_safety(self, chess_board):
        king_safety_score = 0
        for row in range(8):
            for col in range(8):
                piece = chess_board.board[row][col]
                if isinstance(piece, King) and piece.color == self.color:
                    king_safety_score += (4 - abs(3.5 - row) - abs(3.5 - col))
        return king_safety_score

    def _get_all_moves(self, chess_board):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = chess_board.board[row][col]
                if isinstance(piece, Piece) and piece.color == self.color:
                    piece_moves = piece.get_available_moves(chess_board.board)
                    for move in piece_moves:
                        moves.append(((row, col), move))
        return moves
