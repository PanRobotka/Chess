import pygame
from Chess import ChessBoard, Piece, Pawn, King, Queen, Rook, Bishop, Horse
from ai_player import AIPlayer


class Chess_app:
    def __init__(self, board_size=800, margin=50):
        self.board_size = board_size
        self.margin = margin

        pygame.init()
        pygame.display.set_caption("Szachy")
        self.font = pygame.font.SysFont(None, 40)
        self.piece_font = pygame.font.SysFont(None, 60)

        width, height = self.board_size + 2 * self.margin, self.board_size + 2 * self.margin
        window_size = (width, height)
        self.fps = 30
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(window_size)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (200, 200, 200)
        self.red = (255, 0, 0)

        self.start_text = self.font.render("Start Game", True, self.black)
        self.start_rect = self.start_text.get_rect(center=(width // 2, width // 3))

        self.quit_text = self.font.render("Quit Game", True, self.black)
        self.quit_rect = self.quit_text.get_rect(center=(width // 2, height // 2))

        self.selected_piece = None
        self.running = True
        self.game_started = False
        self.should_capture_mouse = False

        self.current_player = 'white'
        self.chess_board = ChessBoard()
        self.invalid_move_message = None
        self.invalid_move_time = 0

        self.ai_player = AIPlayer('black')

        self.pygame_loop()

    def draw_message_box(self, message, rect):
        # Dodanie marginesu
        margin = 30
        inner_rect = rect.inflate(margin, margin)

        # Rysowanie tła i ramki z uwzględnieniem marginesu
        pygame.draw.rect(self.screen, (255, 255, 255), inner_rect)  # Białe tło
        pygame.draw.rect(self.screen, (0, 0, 0), inner_rect, 2)  # Czarna ramka

        # Wyśrodkowanie tekstu wewnątrz prostokąta z uwzględnieniem marginesu
        text_rect = message.get_rect(center=inner_rect.center)
        self.screen.blit(message, text_rect)

    def promote_pawn(self, position):
        choices = [Queen, Rook, Bishop, Horse]
        choice_index = 0
        promoting = True

        promo_width = self.board_size // 1.5
        promo_height = self.board_size // 3
        promo_x = (self.board_size + 2 * self.margin - promo_width) // 2
        promo_y = (self.board_size + 2 * self.margin - promo_height) // 2

        while promoting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        choice_index = (choice_index - 1) % len(choices)
                    elif event.key == pygame.K_RIGHT:
                        choice_index = (choice_index + 1) % len(choices)
                    elif event.key == pygame.K_RETURN:
                        self.chess_board.promote_pawn(position, choices[choice_index])
                        promoting = False

            current_screen = self.screen.copy()

            pygame.draw.rect(self.screen, self.white, (promo_x, promo_y, promo_width, promo_height))
            pygame.draw.rect(self.screen, self.black, (promo_x, promo_y, promo_width, promo_height), 2)

            message = self.font.render("Wybierz figurę do promocji:", True, self.black)
            message_rect = message.get_rect(center=(promo_x + promo_width // 2, promo_y + 30))
            self.screen.blit(message, message_rect)

            for i, piece_class in enumerate(choices):
                piece_text = self.font.render(piece_class.__name__, True, self.black)
                x_pos = promo_x + (i + 1) * promo_width // (len(choices) + 1)
                y_pos = promo_y + promo_height // 2 + 20
                text_rect = piece_text.get_rect(center=(x_pos, y_pos))

                if i == choice_index:
                    pygame.draw.rect(self.screen, self.red, text_rect.inflate(20, 20), 2)
                self.screen.blit(piece_text, text_rect)

            pygame.display.flip()
            self.clock.tick(self.fps)

        self.screen.blit(current_screen, (0, 0))
        self.draw_board()
        pygame.display.flip()

    def pygame_loop(self):
        while self.running:
            self.screen.fill(self.gray)

            self.event_checker()

            if not self.game_started:
                self.screen.blit(self.start_text, self.start_rect)
                self.screen.blit(self.quit_text, self.quit_rect)
            else:
                self.draw_board()
                if self.selected_piece is not None:
                    self.draw_available_moves(self.selected_piece)

            if self.invalid_move_message is not None:
                current_time = pygame.time.get_ticks()
                if current_time - self.invalid_move_time < 1500:
                    self.draw_message_box(self.invalid_move_message, self.invalid_move_message_rect)
                else:
                    self.invalid_move_message = None

            if self.game_started:
                if self.chess_board.is_king_dead('white'):
                    self.ai_player.end_game()
                    self.draw_message_box(self.font.render("Koniec gry! Król biały został zbity.", True, self.black),
                                          pygame.Rect(0, 0, self.board_size, self.board_size))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    self.running = False
                elif self.chess_board.is_king_dead('black'):
                    self.ai_player.end_game()
                    self.draw_message_box(self.font.render("Koniec gry! Król czarny został zbity.", True, self.black),
                                          pygame.Rect(0, 0, self.board_size, self.board_size))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    self.running = False

                if self.current_player == 'black':
                    self.ai_move()

            player_text = self.font.render(f"Gracz: {self.current_player.capitalize()}", True, self.black)
            player_rect = player_text.get_rect(
                center=(self.board_size // 2 + self.margin, self.board_size + 3 * self.margin // 2))
            self.screen.blit(player_text, player_rect)

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()

    def ai_move(self):
        move = self.ai_player.choose_move(self.chess_board)
        if move:
            start_pos, end_pos = move
            piece = self.chess_board.board[start_pos[0]][start_pos[1]]
            self.chess_board.move_piece(start_pos, end_pos)

            if isinstance(piece, Pawn) and piece.can_promote():
                self.chess_board.promote_pawn(end_pos, Queen)

            self.current_player = 'white'

    def event_checker(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if not self.game_started:
                    if self.start_rect.collidepoint(x, y):
                        self.game_started = True
                    elif self.quit_rect.collidepoint(x, y):
                        self.running = False
                else:
                    if self.margin <= x <= self.margin + self.board_size and self.margin <= y <= self.margin + self.board_size:
                        self.row = int((y - self.margin) // (self.board_size / 8))
                        self.col = int((x - self.margin) // (self.board_size / 8))
                        if self.selected_piece is None:
                            piece = self.chess_board.board[self.row][self.col]
                            if isinstance(piece,
                                          Piece) and piece.color == self.current_player and self.current_player == 'white':
                                self.selected_piece = piece
                        else:
                            start_position = self.selected_piece.position
                            end_position = (self.row, self.col)
                            available_moves = self.selected_piece.get_available_moves(self.chess_board.board)
                            if end_position in available_moves:
                                target_piece = self.chess_board.board[self.row][self.col]
                                if not isinstance(target_piece, Piece) or target_piece.color != self.current_player:
                                    self.chess_board.move_piece(start_position, end_position)
                                    if isinstance(self.selected_piece, Pawn) and not self.selected_piece.move_made:
                                        self.selected_piece.move()

                                    if isinstance(self.selected_piece, Pawn) and self.selected_piece.can_promote():
                                        self.promote_pawn(end_position)

                                    self.current_player = 'black'
                                else:
                                    self.invalid_move_message = self.font.render("Nieprawidłowy ruch", True,
                                                                                 (255, 0, 0))
                                    self.invalid_move_message_rect = self.invalid_move_message.get_rect(
                                        center=(self.board_size // 2 + self.margin, self.board_size // 3 + self.margin))
                                    self.invalid_move_time = pygame.time.get_ticks()
                            else:
                                self.invalid_move_message = self.font.render("Nieprawidłowy ruch", True, (255, 0, 0))
                                self.invalid_move_message_rect = self.invalid_move_message.get_rect(
                                    center=(self.board_size // 2 + self.margin, self.board_size // 3 + self.margin))
                                self.invalid_move_time = pygame.time.get_ticks()
                            self.selected_piece = None
                        if isinstance(self.selected_piece, Piece):
                            self.draw_available_moves(self.selected_piece)

    def draw_available_moves(self, piece):
        if isinstance(piece, Piece):
            available_moves = piece.get_available_moves(self.chess_board.board)
            for move in available_moves:
                r, c = move
                if self.chess_board.board[r][c] == '.':
                    color = (0, 255, 0)  # Zielony kolor dla pustych pól
                elif self.chess_board.board[r][c].color != piece.color:
                    color = (255, 0, 0)  # Czerwony kolor dla zajętych pól z figurami przeciwnego koloru
                else:
                    continue  # Pomijamy podświetlenie pól z figurami tego samego koloru
                pygame.draw.rect(self.screen, color, (
                    self.margin + c * self.board_size / 8, self.margin + r * self.board_size / 8,
                    self.board_size / 8,
                    self.board_size / 8), 3)

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.white if (row + col) % 2 == 0 else self.black
                pygame.draw.rect(self.screen, color, (
                    self.margin + col * self.board_size / 8, self.margin + row * self.board_size / 8,
                    self.board_size / 8, self.board_size / 8))

                # Dodanie opisu pól
                if row == 0:  # Dla górnej krawędzi planszy
                    text = self.font.render(chr(65 + col), True, self.red)  # ASCII kod dla liter od a do h
                    self.screen.blit(text,
                                     (self.margin + col * self.board_size / 8 + 20, row * self.board_size / 8 + 5))
                if col == 0:  # Dla lewej krawędzi planszy
                    text = self.font.render(str(row + 1), True, self.red)  # Cyfry od 1 do 8
                    self.screen.blit(text,
                                     (col * self.board_size / 8 + 5, self.margin + row * self.board_size / 8 + 20))

                # Sprawdź, czy pole na planszy jest instancją klasy Piece
                piece = self.chess_board.board[row][col]

                # Dodaj figury na planszę
                if isinstance(piece, Piece):
                    text = self.piece_font.render(piece.id, True, self.red)
                    self.screen.blit(text, (
                        self.margin + col * self.board_size / 8 + 20, self.margin + row * self.board_size / 8 + 20))


if __name__ == "__main__":
    Chess_app()
