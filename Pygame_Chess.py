import pygame
from Chess import ChessBoard, Piece

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
BOARD_SIZE = 800
MARGIN = 50  # Dodaj margines do okna gry ( bez tego nie dodamy oznaczeń pól)
WIDTH, HEIGHT = BOARD_SIZE + 2 * MARGIN, BOARD_SIZE + 2 * MARGIN
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 30

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Font
font = pygame.font.SysFont(None, 30)  # Wybierz odpowiedni rozmiar czcionki
piece_font = pygame.font.SysFont(None, 60)  # Wybierz odpowiedni rozmiar czcionki dla figur

# Stworzenie okna gry
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Szachy")

# Definiowanie przycisków dla Menu (GUI)
start_text = font.render("Start Game", True, BLACK)
start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

quit_text = font.render("Quit Game", True, BLACK)
quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Zmienna śledząca stan gry (czy gra została już uruchomiona)
game_started = False

# Figury na planszy
chess_board = ChessBoard()


# Funkcja rysująca planszę
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (
                MARGIN + col * BOARD_SIZE / 8, MARGIN + row * BOARD_SIZE / 8, BOARD_SIZE / 8, BOARD_SIZE / 8))

            # Dodanie opisu pól
            if row == 0:  # Dla górnej krawędzi planszy
                text = font.render(chr(65 + col), True, RED)  # ASCII kod dla liter od a do h
                screen.blit(text, (MARGIN + col * BOARD_SIZE / 8 + 20, row * BOARD_SIZE / 8 + 5))
            if col == 0:  # Dla lewej krawędzi planszy
                text = font.render(str(row + 1), True, RED)  # Cyfry od 1 do 8
                screen.blit(text, (col * BOARD_SIZE / 8 + 5, MARGIN + row * BOARD_SIZE / 8 + 20))

            # Dodaj figury na planszę
            piece = chess_board.board[row][col]
            if isinstance(piece, Piece):  # Sprawdź, czy pole na planszy jest instancją klasy Piece
                text = piece_font.render(piece.id, True, RED)
                screen.blit(text, (MARGIN + col * BOARD_SIZE / 8 + 20, MARGIN + row * BOARD_SIZE / 8 + 20))


# Główna pętla gry
selected_piece = None  # Przechowaj informacje o wybranym pionku
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(GRAY)

    if not game_started:  # Jeśli gra nie została jeszcze uruchomiona, wyświetl menu
        # Narysuj przyciski
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)
    else:  # Jeśli gra została uruchomiona, wyświetl planszę szachową
        draw_board()

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if not game_started:  # Jeśli gra nie została jeszcze uruchomiona, obsłuż kliknięcia na przyciskach
                if start_rect.collidepoint(x, y):  # Kliknięto przycisk "Start Game"
                    game_started = True
                elif quit_rect.collidepoint(x, y):  # Kliknięto przycisk "Quit Game"
                    running = False
            else:  # Jeśli gra została uruchomiona, obsłuż kliknięcia na planszy
                row = int((y - MARGIN) // (BOARD_SIZE / 8))
                col = int((x - MARGIN) // (BOARD_SIZE / 8))
                if selected_piece is None:
                    selected_piece = (row, col)
                else:
                    start_position = selected_piece
                    end_position = (row, col)
                    chess_board.move_piece(start_position, end_position)
                    selected_piece = None

    pygame.display.flip()
    clock.tick(FPS)

# Zamknięcie Pygame
pygame.quit()
