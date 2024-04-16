import tkinter as tk
import os
import pygame
import Chess_pygame_configfile as config




class ChessApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        pygame.display.init()
        self.window_size = (self.winfo_reqwidth(), self.winfo_reqheight())
        self.screen = pygame.display.set_mode(self.window_size)
        #inicjalizacja pygame i tworzenie okna

        #zmienne potrzebne do gry
        self.turn = 'white'
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

        self.field_coords = []

        self.create_chessboard()


        self.pygame_loop()

    def pygame_loop(self):
        self.screen.fill((0, 0, 255))
        self.draw_chessboard()

        pygame.display.flip()
        self.after(1, self.pygame_loop)

    def create_chessboard(self):
        field_size = (int(self.window_size[0]/8), int(self.window_size[1]/8))
        self.field_coords = []
        for row in range(8):
            for column in range(8):
                self.field_coords.append([column * field_size[0], row * field_size[1], field_size[0], field_size[1]])
        print('field coords', self.field_coords)
        print('len field coords', len(self.field_coords))

    def draw_chessboard(self):
        row_number = 0
        for field_index, field_coord in enumerate(self.field_coords):
            if field_index % 8 == 0:
                row_number += 1
            if field_index % 2 == 0 and row_number % 2 != 0:
                pygame.draw.rect(self.screen, config.white_field_color, field_coord)
            elif field_index % 2 != 0 and row_number % 2 != 0:
                pygame.draw.rect(self.screen, config.black_field_color, field_coord)
            elif field_index % 2 != 0 and row_number % 2 == 0:
                pygame.draw.rect(self.screen, config.white_field_color, field_coord)
            elif field_index % 2 == 0 and row_number %2 == 0:
                pygame.draw.rect(self.screen, config.black_field_color, field_coord)




