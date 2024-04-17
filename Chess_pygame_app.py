import tkinter as tk
import os
import pygame
import Chess_pygame_configfile as config

class Piece(pygame.sprite.Sprite):
    def __init__ (self, position, piece_color, piece_type, piece_x_size = 100, piece_y_size = 100):
        super().__init__()
        self.piece_type = piece_type
        self.position = position
        self.piece_color = piece_color

        piece_image_path = "images/pieces/" + self.piece_color + "/" + self.piece_type + ".png"
        self.image = pygame.image.load(piece_image_path)
        self.image = pygame.transform.scale(self.image, (piece_x_size, piece_y_size))

        self.image.set_colorkey((34, 177, 76))

        self.rect = self.image.get_rect(center=self.position)

    def set_position(self, position):
        position = self.position


class ChessApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # inicjalizacja pygame i tworzenie okna
        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        pygame.display.init()
        self.window_size = (self.winfo_reqwidth(), self.winfo_reqheight())
        self.screen = pygame.display.set_mode(self.window_size)


        self.field_coords = []
        #wyliczanie szachownicy dla zadanej rozdzielczości
        self.create_chessboard()


        self.pygame_loop()

    def pygame_loop(self):
        #ustaw kolor tła na niebieski
        self.screen.fill((0, 0, 255))
        #rysuj szachownice
        self.draw_chessboard()
        #rysuj pionki
        self.draw_pieces()

        pygame.display.flip()
        self.after(1, self.pygame_loop)

    def draw_pieces(self):


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




