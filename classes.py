import pygame
import my_pygame

"""-------------------------------------------------------------------------Imager class to creat image in pygame---------------------------------------------------------------------"""
class Imager():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
    def draw(self):
        my_pygame.win.blit(self.image, (self.rect.x, self.rect.y))

"""-------------------------------------------------------------------Button class to create button with an image by scaling it--------------------------------------------"""

class Button():
    def __init__(self, x, y, image, scale, alt):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        width_alt = alt.get_width()
        height_alt = alt.get_height()
        self.image_alt = pygame.transform.scale(alt, (int(width_alt*scale), int(height_alt*scale)))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect_alt = self.image_alt.get_rect()
        self.rect_alt.topleft = (self.x, self.y)
        self.pressed = False

        
    def draw(self):
        my_pygame.win.blit(self.image, (self.rect.x, self.rect.y))
    def draw_alt(self):
        my_pygame.win.blit(self.image_alt, (self.rect.x, self.rect.y))

    """---------------------------function for button to click-------------------------------"""
    def clicked(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                self.pressed = True
                print("Hello")
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.pressed = False
        return action
    

"""----------------------------------------------------DATABASE for chess game-----------------------------------------------"""
White_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
Your_white_pos = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
Your_black_pos = [(0, 7), (1, 7), (2, 7), (4, 7), (3, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

Black_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
Opp_white_pos = [(7, 0), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)]
Opp_black_pos = [(7, 0), (6, 0), (5, 0), (3, 0), (4, 0), (2, 0), (1, 0), (0, 0), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)]





