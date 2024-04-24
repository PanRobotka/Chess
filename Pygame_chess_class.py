import pygame
from Chess import ChessBoard, Piece, Pawn, King


class Chess_app:
    def __init__(self, board_size=800, margin=50):
        self.board_size = board_size
        self.margin = margin

        pygame.init()
        pygame.display.set_caption("Szachy")
        self.font = pygame.font.SysFont(None, 40)  # Wybierz odpowiedni rozmiar czcionki
        self.piece_font = pygame.font.SysFont(None, 60)  # Wybierz odpowiedni rozmiar czcionki dla figur

        width, height = self.board_size + 2 * self.margin, self.board_size + 2 * self.margin
        window_size = (width, height)
        self.fps = 30
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(window_size)
        # kolory
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (200, 200, 200)
        self.red = (255, 0, 0)

        self.start_text = self.font.render("Start Game", True, self.black)
        self.start_rect = self.start_text.get_rect(center=(width // 2, width // 3))

        self.quit_text = self.font.render("Quit Game", True, self.black)
        self.quit_rect = self.quit_text.get_rect(center=(width // 2, height // 2))

        self.selected_piece = None  # Przechowaj informacje o wybranym pionku
        self.running = True
        self.game_started = False
        self.should_capture_mouse = False

        self.current_player = 'white'  # Ustaw aktualnego gracza jako białego na początku gry
        self.chess_board = ChessBoard()
        # Zmienne do obsługi wyświetlania tekstu
        self.invalid_move_message = None
        self.invalid_move_time = 0

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
                if current_time - self.invalid_move_time < 1500:  # Wyświetlaj komunikat przez 1.5 sekundy
                    self.draw_message_box(self.invalid_move_message, self.invalid_move_message_rect)
                else:
                    self.invalid_move_message = None  # Usuń komunikat po określonym czasie

            # Wyświetlenie informacji o aktualnym graczu
            player_text = self.font.render(f"Gracz: {self.current_player.capitalize()}", True, self.black)
            player_rect = player_text.get_rect(
                center=(self.board_size // 2 + self.margin, self.board_size + 3 * self.margin // 2))
            self.screen.blit(player_text, player_rect)

            pygame.display.flip()
            self.clock.tick(self.fps)

        # Zamknięcie Pygame
        pygame.quit()

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
                            if isinstance(piece, Piece) and piece.color == self.current_player:
                                self.selected_piece = piece
                        else:
                            start_position = self.selected_piece.position
                            end_position = (self.row, self.col)
                            available_moves = self.selected_piece.get_available_moves(self.chess_board.board)
                            if end_position in available_moves:
                                self.chess_board.move_piece(start_position, end_position)
                                if isinstance(self.selected_piece, Pawn) and not self.selected_piece.move_made:
                                    self.selected_piece.move()
                                # Zmiana gracza po poprawnym ruchu
                                self.current_player = 'black' if self.current_player == 'white' else 'white'
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
                if self.chess_board.board[r][c] != '.':
                    color = (255, 0, 0)  # Czerwony kolor dla zajętych pól
                else:
                    color = (0, 255, 0)  # Zielony kolor dla pustych pól
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
