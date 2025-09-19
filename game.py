import socket, sys, pickle
import Host
import Join
from _thread import start_new_thread
import pygame
import my_pygame
import classes

pygame.init()

clock = pygame.time.Clock()

surrender_text = "Surrender"
win_text = "Congrajulation! Won by Checkmate"
lose_text = "Lost by Checkmate"
draw_text = "Stalemate..."
resign_text = "End of game by Resign"

fonts = pygame.font.SysFont("Comic sans MS", 25)

blue = (58, 130, 252)
light_blue = (153, 191, 255)
orange = (255, 189, 77)
red = (255, 53, 48)
light_red = (255, 120, 117)


your_turn = False

selected = 100
is_selected = False


wood_image = pygame.image.load("wood.png").convert_alpha()
Wood = classes.Imager(0, 0, wood_image, 1)

board_image = pygame.image.load("resources/Board.png")
Board = classes.Imager(0, 0, board_image, 0.6)
Board.image = pygame.transform.scale(board_image, (640, 640))

white_image_list = ["W_r", "W_n", "W_b", "W_q", "W_k", "W_b", "W_n", "W_r", "W_p", "W_p", "W_p", "W_p", "W_p", "W_p", "W_p", "W_p"]
black_image_list = ["B_r", "B_n", "B_b", "B_q", "B_k", "B_b", "B_n", "B_r", "B_p", "B_p", "B_p", "B_p", "B_p", "B_p", "B_p", "B_p"]




captured_black_pieces = []
captured_white_pieces = []

valid_moves = []
opp_valid_moves = []
start_piece = ""

is_check_opp = False
is_check_you = False
is_checkmate_you = False
is_checkmate_opp = False
is_stalemate_you = False
is_stalemate_opp = False
king_moved = False
rook1_moved = False
rook2_moved = False

"""-------------------------------------------------------------finding every possible moves for every pieces-------------------------------------------------------"""

def check_pawn_moves(index):
    global valid_moves
    if p == 0:
        pos = classes.Your_white_pos[index]
        if (pos[0], pos[1]-1) not in classes.Your_white_pos and (pos[0], pos[1]-1) not in classes.Opp_black_pos and pos[1] > 1:
            valid_moves.append((pos[0], pos[1]-1))
            if (pos[0], pos[1]-2) not in classes.Your_white_pos and (pos[0], pos[1]-2) not in classes.Opp_black_pos and pos[1] == 6:
                valid_moves.append((pos[0], pos[1]-2))
        if (pos[0]-1, pos[1]-1) in classes.Opp_black_pos:
            valid_moves.append((pos[0]-1, pos[1]-1))
        if (pos[0]+1, pos[1]-1) in classes.Opp_black_pos:
            valid_moves.append((pos[0]+1, pos[1]-1))
    elif p == 1:
        pos = classes.Your_black_pos[index]
        if (pos[0], pos[1]-1) not in classes.Your_black_pos and (pos[0], pos[1]-1) not in classes.Opp_white_pos and pos[1] > 1:
            valid_moves.append((pos[0], pos[1]-1))
            if (pos[0], pos[1]-2) not in classes.Your_black_pos and (pos[0], pos[1]-2) not in classes.Opp_white_pos and pos[1] == 6:
                valid_moves.append((pos[0], pos[1]-2))
        if (pos[0]-1, pos[1]-1) in classes.Opp_white_pos:
            valid_moves.append((pos[0]-1, pos[1]-1))
        if (pos[0]+1, pos[1]-1) in classes.Opp_white_pos:
            valid_moves.append((pos[0]+1, pos[1]-1))

def check_rook_moves(index):
    global valid_moves
    if p == 0:
        pos = classes.Your_white_pos[index]
        for i in range(4): #0:down 1:up 2:right 3:left 
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            elif i == 3:
                x = -1
                y = 0
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in classes.Your_white_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in classes.Opp_black_pos:
                        break
                    chain += 1
                else:
                    break
    elif p == 1:
        pos = classes.Your_black_pos[index]
        for i in range(4): #0:down 1:up 2:right 3:left 
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            elif i == 3:
                x = -1
                y = 0
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in classes.Your_black_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in classes.Opp_white_pos:
                        break
                    chain += 1
                else:
                    break

def check_knight_moves(index):
    global valid_moves
    if p == 0:
        pos = classes.Your_white_pos[index]
        if (pos[0]+1, pos[1]-2) not in classes.Your_white_pos and pos[0] < 7 and pos[1] > 1:
            valid_moves.append((pos[0]+1, pos[1]-2))
        if (pos[0]-1, pos[1]-2) not in classes.Your_white_pos and pos[0] > 0 and pos[1] > 1:
            valid_moves.append((pos[0]-1, pos[1]-2))
        if (pos[0]+1, pos[1]+2) not in classes.Your_white_pos and pos[0] < 7 and pos[1] < 6:
            valid_moves.append((pos[0]+1, pos[1]+2))
        if (pos[0]-1, pos[1]+2) not in classes.Your_white_pos and pos[0] > 0 and pos[1] < 6:
            valid_moves.append((pos[0]-1, pos[1]+2))
        if (pos[0]+2, pos[1]+1) not in classes.Your_white_pos and pos[0] < 6 and pos[1] < 7:
            valid_moves.append((pos[0]+2, pos[1]+1))
        if (pos[0]+2, pos[1]-1) not in classes.Your_white_pos and pos[0] < 6 and pos[1] > 0:
            valid_moves.append((pos[0]+2, pos[1]-1))
        if (pos[0]-2, pos[1]+1) not in classes.Your_white_pos and pos[0] > 1 and pos[1] < 7:
            valid_moves.append((pos[0]-2, pos[1]+1))
        if (pos[0]-2, pos[1]-1) not in classes.Your_white_pos and pos[0] > 1 and pos[1] > 0:
            valid_moves.append((pos[0]-2, pos[1]-1))
    elif p == 1:
        pos = classes.Your_black_pos[index]
        if (pos[0]+1, pos[1]-2) not in classes.Your_black_pos and pos[0] < 7 and pos[1] > 1:
            valid_moves.append((pos[0]+1, pos[1]-2))
        if (pos[0]-1, pos[1]-2) not in classes.Your_black_pos and pos[0] > 0 and pos[1] > 1:
            valid_moves.append((pos[0]-1, pos[1]-2))
        if (pos[0]+1, pos[1]+2) not in classes.Your_black_pos and pos[0] < 7 and pos[1] < 6:
            valid_moves.append((pos[0]+1, pos[1]+2))
        if (pos[0]-1, pos[1]+2) not in classes.Your_black_pos and pos[0] > 0 and pos[1] < 6:
            valid_moves.append((pos[0]-1, pos[1]+2))
        if (pos[0]+2, pos[1]+1) not in classes.Your_black_pos and pos[0] < 6 and pos[1] < 7:
            valid_moves.append((pos[0]+2, pos[1]+1))
        if (pos[0]+2, pos[1]-1) not in classes.Your_black_pos and pos[0] < 6 and pos[1] > 0:
            valid_moves.append((pos[0]+2, pos[1]-1))
        if (pos[0]-2, pos[1]+1) not in classes.Your_black_pos and pos[0] > 1 and pos[1] < 7:
            valid_moves.append((pos[0]-2, pos[1]+1))
        if (pos[0]-2, pos[1]-1) not in classes.Your_black_pos and pos[0] > 1 and pos[1] > 0:
            valid_moves.append((pos[0]-2, pos[1]-1))

def check_bishop_moves(index):
    global valid_moves
    if p == 0:
        pos = classes.Your_white_pos[index]
        for i in range(4): #0:up_right 1:up_left 2:down_right 3:down_left 
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            elif i == 3:
                x = -1
                y = 1
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in classes.Your_white_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in classes.Opp_black_pos:
                        break
                    chain += 1
                else:
                    break
    elif p == 1:
        pos = classes.Your_black_pos[index]
        for i in range(4): #0:up_right 1:up_left 2:down_right 3:down_left 
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            elif i == 3:
                x = -1
                y = 1
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in classes.Your_black_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in classes.Opp_white_pos:
                        break
                    chain += 1
                else:
                    break

def check_queen_moves(index):
    global valid_moves
    if p == 0:
        pos = classes.Your_white_pos[index]
        for i in range(8): 
            chain = 1
            if i == 0:
                x = 0
                y = -1
            elif i == 1:
                x = 0
                y = 1
            elif i == 2:
                x = 1
                y = 0
            elif i == 3:
                x = -1
                y = 0
            elif i == 4:
                x = 1
                y = 1
            elif i == 5:
                x = -1
                y = 1
            elif i == 6:
                x = 1
                y = -1
            elif i == 7:
                x = -1
                y = -1
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in classes.Your_white_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in classes.Opp_black_pos:
                        break
                    chain += 1
                else:
                    break
    elif p == 1:
        pos = classes.Your_black_pos[index]
        for i in range(8):
            chain = 1
            if i == 0:
                x = 0
                y = -1
            elif i == 1:
                x = 0
                y = 1
            elif i == 2:
                x = 1
                y = 0
            elif i == 3:
                x = -1
                y = 0
            elif i == 4:
                x = 1
                y = 1
            elif i == 5:
                x = -1
                y = 1
            elif i == 6:
                x = 1
                y = -1
            elif i == 7:
                x = -1
                y = -1
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in classes.Your_black_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in classes.Opp_white_pos:
                        break
                    chain += 1
                else:
                    break

def check_king_moves(index):
    global valid_moves
    if p == 0:
        pos = classes.Your_white_pos[index]
        if not king_moved and not rook1_moved and (pos[0]+1, pos[1]) not in classes.Your_white_pos and (pos[0]+2, pos[1]) not in classes.Your_white_pos and (pos[0]+1, pos[1]) not in classes.Opp_black_pos and (pos[0]+2, pos[1]) not in classes.Opp_black_pos and not is_check_you:
            valid_moves.append((pos[0] + 2, pos[1]))
        if not king_moved and not rook2_moved and (pos[0]-1, pos[1]) not in classes.Your_white_pos and (pos[0]-2, pos[1]) not in classes.Your_white_pos and (pos[0]-3, pos[1]) not in classes.Your_white_pos and (pos[0]-1, pos[1])  not in classes.Opp_black_pos and (pos[0]-2, pos[1]) not in classes.Opp_black_pos and (pos[0]-3, pos[1]) not in classes.Opp_black_pos and not is_check_you:
            valid_moves.append((pos[0]- 2, pos[1]))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_x = pos[0] + i
                new_y = pos[1] + j
                if (new_x, new_y) not in classes.Your_white_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    valid_moves.append((new_x, new_y))
    if p == 1:
        pos = classes.Your_black_pos[index]
        if not king_moved and not rook1_moved and (pos[0]-1, pos[1]) not in classes.Your_black_pos and (pos[0]-2, pos[1]) not in classes.Your_black_pos and (pos[0]-1, pos[1]) not in classes.Opp_white_pos and (pos[0]-2, pos[1]) not in classes.Opp_white_pos and not is_check_you:
            valid_moves.append((pos[0] - 2, pos[1]))
        if not king_moved and not rook2_moved and (pos[0]+1, pos[1]) not in classes.Your_black_pos and (pos[0]+2, pos[1]) not in classes.Your_black_pos and (pos[0]+3, pos[1]) not in classes.Your_black_pos and (pos[0]+1, pos[1])  not in classes.Opp_white_pos and (pos[0]+2, pos[1]) not in classes.Opp_white_pos and (pos[0]-3, pos[1]) not in classes.Opp_white_pos and not is_check_you:
            valid_moves.append((pos[0] + 2, pos[1]))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_x = pos[0] + i
                new_y = pos[1] + j
                if (new_x, new_y) not in classes.Your_black_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    valid_moves.append((new_x, new_y))

"""----------------------------------------check if king or rook moved for castling---------------------------------------------------------"""

def check_king_moved(piece, index):
    global king_moved
    if piece == "king":
        if p == 0:
            if classes.Your_white_pos[index] != (4, 7):
                king_moved = True
        elif p == 1:
            if classes.Your_black_pos[index] != (3, 7):
                king_moved = True
                
def check_rook_moved(piece, index):
    global rook1_moved, rook2_moved
    if piece == "rook":
        if p == 0:
            if classes.Your_white_pos[index] == (0, 7):
                rook2_moved = True
            elif classes.Your_white_pos[index] == (7, 7):
                rook1_moved = True
        elif p == 1:
            if classes.Your_black_pos[index] == (0, 7):
                rook1_moved = True
                
            elif classes.Your_black_pos[index] == (7, 7):
                rook2_moved = True
                
"""---------------------------------------check opponent valid moves for check--------------------------------------------------"""

def check_opp_pawn_moves(index, your_pos, opp_pos):
    global opp_valid_moves
    if p == 0:
        pos = opp_pos[index]
        
        if (pos[0]-1, pos[1]-1) in your_pos:
            opp_valid_moves.append((pos[0]-1, pos[1]-1))
        if (pos[0]+1, pos[1]-1) in your_pos:
            opp_valid_moves.append((pos[0]+1, pos[1]-1))
    elif p == 1:
        pos = opp_pos[index]
        
        if (pos[0]-1, pos[1]-1) in your_pos:
            opp_valid_moves.append((pos[0]-1, pos[1]-1))
        if (pos[0]+1, pos[1]-1) in your_pos:
            opp_valid_moves.append((pos[0]+1, pos[1]-1))

def check_opp_rook_moves(index, your_pos, opp_pos):
    global opp_valid_moves
    if p == 0:
        pos = opp_pos[index]
        for i in range(4): #0:down 1:up 2:right 3:left 
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            elif i == 3:
                x = -1
                y = 0
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in opp_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    opp_valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in your_pos:
                        break
                    chain += 1
                else:
                    break
    elif p == 1:
        pos = classes.Opp_white_pos[index]
        for i in range(4): #0:down 1:up 2:right 3:left 
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            elif i == 3:
                x = -1
                y = 0
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in opp_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    opp_valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in your_pos:
                        break
                    chain += 1
                else:
                    break

def check_opp_knight_moves(index, your_pos, opp_pos):
    global opp_valid_moves
    if p == 0:
        pos = opp_pos[index]
        if (pos[0]+1, pos[1]-2) not in opp_pos and pos[0] < 7 and pos[1] > 1:
            opp_valid_moves.append((pos[0]+1, pos[1]-2))
        if (pos[0]-1, pos[1]-2) not in opp_pos and pos[0] > 0 and pos[1] > 1:
            opp_valid_moves.append((pos[0]-1, pos[1]-2))
        if (pos[0]+1, pos[1]+2) not in opp_pos and pos[0] < 7 and pos[1] < 6:
            opp_valid_moves.append((pos[0]+1, pos[1]+2))
        if (pos[0]-1, pos[1]+2) not in opp_pos and pos[0] > 0 and pos[1] < 6:
            opp_valid_moves.append((pos[0]-1, pos[1]+2))
        if (pos[0]+2, pos[1]+1) not in opp_pos and pos[0] < 6 and pos[1] < 7:
            opp_valid_moves.append((pos[0]+2, pos[1]+1))
        if (pos[0]+2, pos[1]-1) not in opp_pos and pos[0] < 6 and pos[1] > 0:
            opp_valid_moves.append((pos[0]+2, pos[1]-1))
        if (pos[0]-2, pos[1]+1) not in opp_pos and pos[0] > 1 and pos[1] < 7:
            opp_valid_moves.append((pos[0]-2, pos[1]+1))
        if (pos[0]-2, pos[1]-1) not in opp_pos and pos[0] > 1 and pos[1] > 0:
            opp_valid_moves.append((pos[0]-2, pos[1]-1))
    elif p == 1:
        pos = opp_pos[index]
        if (pos[0]+1, pos[1]-2) not in opp_pos and pos[0] < 7 and pos[1] > 1:
            opp_valid_moves.append((pos[0]+1, pos[1]-2))
        if (pos[0]-1, pos[1]-2) not in opp_pos and pos[0] > 0 and pos[1] > 1:
            opp_valid_moves.append((pos[0]-1, pos[1]-2))
        if (pos[0]+1, pos[1]+2) not in opp_pos and pos[0] < 7 and pos[1] < 6:
            opp_valid_moves.append((pos[0]+1, pos[1]+2))
        if (pos[0]-1, pos[1]+2) not in opp_pos and pos[0] > 0 and pos[1] < 6:
            opp_valid_moves.append((pos[0]-1, pos[1]+2))
        if (pos[0]+2, pos[1]+1) not in opp_pos and pos[0] < 6 and pos[1] < 7:
            opp_valid_moves.append((pos[0]+2, pos[1]+1))
        if (pos[0]+2, pos[1]-1) not in opp_pos and pos[0] < 6 and pos[1] > 0:
            opp_valid_moves.append((pos[0]+2, pos[1]-1))
        if (pos[0]-2, pos[1]+1) not in opp_pos and pos[0] > 1 and pos[1] < 7:
            opp_valid_moves.append((pos[0]-2, pos[1]+1))
        if (pos[0]-2, pos[1]-1) not in opp_pos and pos[0] > 1 and pos[1] > 0:
            opp_valid_moves.append((pos[0]-2, pos[1]-1))

def check_opp_bishop_moves(index, your_pos, opp_pos):
    global opp_valid_moves
    if p == 0:
        pos = opp_pos[index]
        for i in range(4): #0:up_right 1:up_left 2:down_right 3:down_left 
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            elif i == 3:
                x = -1
                y = 1
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in opp_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    opp_valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in your_pos:
                        break
                    chain += 1
                else:
                    break
    elif p == 1:
        pos = opp_pos[index]
        for i in range(4): #0:up_right 1:up_left 2:down_right 3:down_left 
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            elif i == 3:
                x = -1
                y = 1
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in opp_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    opp_valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in your_pos:
                        break
                    chain += 1
                else:
                    break

def check_opp_queen_moves(index, your_pos, opp_pos):
    global opp_valid_moves
    if p == 0:
        pos = opp_pos[index]
        
        for i in range(8): 
            chain = 1
            if i == 0:
                x = 0
                y = -1
            elif i == 1:
                x = 0
                y = 1
            elif i == 2:
                x = 1
                y = 0
            elif i == 3:
                x = -1
                y = 0
            elif i == 4:
                x = 1
                y = 1
            elif i == 5:
                x = -1
                y = 1
            elif i == 6:
                x = 1
                y = -1
            elif i == 7:
                x = -1
                y = -1
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in opp_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    opp_valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in your_pos:
                        break
                    chain += 1
                else:
                    break
    elif p == 1:
        pos = opp_pos[index]
        for i in range(8):
            chain = 1
            if i == 0:
                x = 0
                y = -1
            elif i == 1:
                x = 0
                y = 1
            elif i == 2:
                x = 1
                y = 0
            elif i == 3:
                x = -1
                y = 0
            elif i == 4:
                x = 1
                y = 1
            elif i == 5:
                x = -1
                y = 1
            elif i == 6:
                x = 1
                y = -1
            elif i == 7:
                x = -1
                y = -1
            while True:
                new_x = pos[0] + x*chain
                new_y = pos[1] + y*chain
                if (new_x, new_y) not in opp_pos and 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    opp_valid_moves.append((new_x, new_y))
                    if (new_x, new_y) in your_pos:
                        break
                    chain += 1
                else:
                    break


"""--------------------------------------------------------------- castling function ----------------------------------------------------------------"""

def castle(click_cord, pos):
    global king_moved, rook1_moved, rook2_moved
    if p == 0:
        if click_cord == (pos[0]+2, pos[1]):
            #classes.Your_white_pos[index] = click_cord
            rook_index = classes.Your_white_pos.index((7, 7))
            classes.Your_white_pos[rook_index] = (5, 7)
        elif click_cord == (pos[0]-2, pos[1]):
            #classes.Your_white_pos[index] = click_cord
            rook_index = classes.Your_white_pos.index((0, 7))
            classes.Your_white_pos[rook_index] = (3, 7)

    elif p == 1:
        if click_cord == (pos[0]+2, pos[1]):
            rook_index = classes.Your_black_pos.index((7, 7))
            classes.Your_black_pos[rook_index] = (4, 7)
        elif click_cord == (pos[0]-2, pos[1]):
            rook_index = classes.Your_black_pos.index((0, 7))
            classes.Your_black_pos[rook_index] = (2, 7)
    king_moved = True
    rook1_moved = True
    rook2_moved = True

"""----------------------------------------------------------draw board, pieces and border--------------------------------------------------------"""

def draw_pieces():
    if p == 0:
        for i in range(len(classes.White_pieces)):
            
            try:
                image = pygame.image.load("resources/" + white_image_list[i] + ".png").convert_alpha()
            except:
                
                return
            pos = classes.Your_white_pos[i]
            image = pygame.transform.scale(image,(60, 60))
            image_rect = image.get_rect()
            image_rect.center = (40 + pos[0]*80, 40 + pos[1]*80)
            win.blit(image, (image_rect.x, image_rect.y))

        for i in range(len(classes.Black_pieces)):
            try:
                image = pygame.image.load("resources/" + black_image_list[i] + ".png").convert_alpha()
            except:
                update()
                return
            pos = classes.Opp_black_pos[i]
            image = pygame.transform.scale(image,(60, 60))
            image_rect = image.get_rect()
            image_rect.center = (40 + pos[0]*80, 40 + pos[1]*80)
            win.blit(image, (image_rect.x, image_rect.y))
    elif p == 1:
        
        for i in range(len(classes.Black_pieces)):
            
            try:
                image = pygame.image.load("resources/" + black_image_list[i] + ".png").convert_alpha()
            except:
                update()
                return
            pos = classes.Your_black_pos[i]
            image = pygame.transform.scale(image,(60, 60))
            image_rect = image.get_rect()
            image_rect.center = (40 + pos[0]*80, 40 + pos[1]*80)
            win.blit(image, (image_rect.x, image_rect.y))

        for i in range(len(classes.White_pieces)):
            try:
                image = pygame.image.load("resources/" + white_image_list[i] + ".png").convert_alpha()
            except:
                update()
                return
            pos = classes.Opp_white_pos[i]
            image = pygame.transform.scale(image,(60, 60))
            image_rect = image.get_rect()
            image_rect.center = (40 + pos[0]*80, 40 + pos[1]*80)
            win.blit(image, (image_rect.x, image_rect.y))

def draw_border():
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(win, "black", (i*80, j*80, 80, 80), 1)

"""------------------------------------------------------check valid moves for selected piece------------------------------------------------------------"""

def check_white_valid_moves(selected):
    piece = classes.White_pieces[selected]
    if piece == "pawn":
        check_pawn_moves(selected)
    elif piece == "rook":
        check_rook_moves(selected)
    if piece == "knight":
        check_knight_moves(selected)
    if piece == "bishop":
        check_bishop_moves(selected)
    if piece == "queen":
        check_queen_moves(selected)
    if piece == "king":
        check_king_moves(selected)

def check_black_valid_moves(selected):
    piece = classes.Black_pieces[selected]
    if piece == "pawn":
        check_pawn_moves(selected)
    elif piece == "rook":
        check_rook_moves(selected)
    elif piece == "knight":
        check_knight_moves(selected)
    elif piece == "bishop":
        check_bishop_moves(selected)
    elif piece == "queen":
        check_queen_moves(selected)
    elif piece == "king":
        check_king_moves(selected)
    
"""---------------------------------------------------------add piece to captured list by order-------------------------------------------------------------"""

def add_to_captures(index):
    if p == 0:
        
        piece = classes.Black_pieces[index]
        if piece == "rook":
            captured_black_pieces.append("2rook")
        if piece == "knight":
            captured_black_pieces.append("4knight")
        if piece == "bishop":
            captured_black_pieces.append("3bishop")
        if piece == "queen":
            captured_black_pieces.append("1queen")
        if piece == "pawn":
            captured_black_pieces.append("5pawn")
    elif p == 1:
        piece = classes.White_pieces[index]
        if piece == "rook":
            captured_white_pieces.append("2rook")
        if piece == "knight":
            captured_white_pieces.append("4knight")
        if piece == "bishop":
            captured_white_pieces.append("3bishop")
        if piece == "queen":
            captured_white_pieces.append("1queen")
        if piece == "pawn":
            captured_white_pieces.append("5pawn")


"""-----------------------------------------------------------checking for CHECKS, CHECKMATES, and STALEMATE-------------------------------------------------"""

def check_Check():
    global is_check_opp
    flag = False
    if p == 0:
        for i in range(len(classes.White_pieces)):
            check_white_valid_moves(i)
            black_king_index = classes.Black_pieces.index("king")
            black_king_pos = classes.Opp_black_pos[black_king_index]
            if black_king_pos in valid_moves:
                flag = True
                is_check_opp = True
                break
        if not flag:
            is_check_opp = False

    if p == 1:
        for i in range(len(classes.Black_pieces)):
            check_black_valid_moves(i)
            white_king_index = classes.White_pieces.index("king")
            white_king_pos = classes.Opp_white_pos[white_king_index]
            if white_king_pos in valid_moves:
                flag = True
                is_check_opp = True
                break
        if not flag:
            is_check_opp = False

def check_checkmate_and_stalemate():
    global is_checkmate_you, valid_moves, is_stalemate_you
    all_moves = []
    if p == 0:
        for i in range(len(classes.Your_white_pos)):
            valid_moves = []
            check_white_valid_moves(i)
            check_unchecking(i)
            all_moves += valid_moves

        if all_moves == [] and is_check_you:
            is_checkmate_you = True
        elif all_moves == [] and not is_check_you:
            is_stalemate_you = True
    if p == 1:
        for i in range(len(classes.Your_black_pos)):
            valid_moves = []
            check_white_valid_moves(i)
            check_unchecking(i)
            all_moves += valid_moves

        if all_moves == [] and is_check_you:
            is_checkmate_you = True
        elif all_moves == [] and not is_check_you:
            is_stalemate_you = True

def check_your_checks(your_pos, opp_pos, opp_piece):
    global opp_valid_moves

    
    for pos in opp_pos:
        opp_valid_moves = []
        selected = opp_pos.index(pos)
        piece = opp_piece[selected]
        if piece == "pawn":
            check_opp_pawn_moves(selected, your_pos, opp_pos)
        elif piece == "rook":
            check_opp_rook_moves(selected, your_pos, opp_pos)
        elif piece == "knight":
            check_opp_knight_moves(selected, your_pos, opp_pos)
        elif piece == "bishop":
            check_opp_bishop_moves(selected, your_pos, opp_pos)
        elif piece == "queen":
            
            check_opp_queen_moves(selected, your_pos, opp_pos)
        if p == 0:
            your_king_index = classes.White_pieces.index("king")
        elif p == 1:
            your_king_index = classes.Black_pieces.index("king")
        
        your_king_pos = your_pos[your_king_index]
        if your_king_pos in opp_valid_moves:
            return True
        
    return False

def check_unchecking(index):
    my_moves = valid_moves.copy()
    if p == 0:
        for move in my_moves:
            temp_your_pos = classes.Your_white_pos.copy()
            temp_your_pos[index] = move
            temp_opp_pos = classes.Opp_black_pos.copy()
            temp_opp_piece = classes.Black_pieces.copy()
            if move in temp_opp_pos:
                temp_opp_pos.remove(move)
                temp_opp_piece.pop(classes.Opp_black_pos.index(move))
            check = check_your_checks(temp_your_pos, temp_opp_pos, temp_opp_piece)
            
            if check:
                valid_moves.remove(move)
            
    
    elif p == 1:
        for move in my_moves:
            temp_your_pos = classes.Your_black_pos.copy()
            temp_your_pos[index] = move
            temp_opp_pos = classes.Opp_white_pos.copy()
            temp_opp_piece = classes.White_pieces.copy()
            if move in temp_opp_pos:
                temp_opp_pos.remove(move)
                temp_opp_piece.pop(classes.Opp_white_pos.index(move))
            check = check_your_checks(temp_your_pos, temp_opp_pos, temp_opp_piece)
            
            if check:
                valid_moves.remove(move)
 
def show_captured_pieces():
    pass      


def send_data(b_i_l, w_i_l, w_p, b_p, y_pos, o_pos):
    x = []
    y = []
    
    for i in range(len(y_pos)):
        x_temp = 7 - y_pos[i][0]
        y_temp = 7 - y_pos[i][1]
        x.append((x_temp,y_temp))
    for i in range(len(o_pos)):
        x_temp = 7 - o_pos[i][0]
        y_temp = 7 - o_pos[i][1]
        y.append((x_temp,y_temp))

    prev_opp_move = (7-prev_move[0], 7-prev_move[1])
    now_opp_move = (7-now_move[0], 7-now_move[1])
    

    data_list = [b_i_l, w_i_l, w_p, b_p, x, y, is_check_opp, is_checkmate_you, prev_opp_move, now_opp_move]
    data_list_pickle = pickle.dumps(data_list)
    if p == 0:
        Host.send_data(data_list_pickle)
    elif p == 1:
        Join.send_data(data_list_pickle)

def receive_data(data_list_pickle):

    global black_image_list, white_image_list, your_turn, is_check_you, is_checkmate_opp, now_move, prev_move
    data_list = pickle.loads(data_list_pickle)
    if p == 0:
        black_image_list, white_image_list, classes.White_pieces, classes.Black_pieces, classes.Opp_black_pos, classes.Your_white_pos, is_check_you, is_checkmate_opp, prev_move, now_move = data_list
    elif p == 1:
        black_image_list, white_image_list, classes.White_pieces, classes.Black_pieces, classes.Opp_white_pos, classes.Your_black_pos, is_check_you, is_checkmate_opp, prev_move, now_move = data_list
    
    check_Check()
    check_checkmate_and_stalemate()
    print(is_check_you)
    print(is_checkmate_you)
    print(is_stalemate_you)
    your_turn = True
    

def update():

    Wood.draw()
    Board.draw()

    if prev_move:
        pygame.draw.rect(win, orange, (prev_move[0]*80, prev_move[1]*80, 80, 80))
        pygame.draw.rect(win, orange, (now_move[0]*80, now_move[1]*80, 80, 80))
    
    if is_selected:
        win.fill(blue, (x_cord*80, y_cord*80, 80, 80))
        for i in valid_moves:
            if p == 0:
                if (i[0], i[1]) not in classes.Opp_black_pos:
                    pygame.draw.rect(win, light_blue, (i[0]*80, i[1]*80, 80, 80))
                    
                else:
                    pygame.draw.rect(win, light_red, (i[0]*80, i[1]*80, 80, 80))
                    
            elif p == 1:
                if (i[0], i[1]) not in classes.Opp_white_pos:
                    pygame.draw.rect(win, light_blue, (i[0]*80, i[1]*80 , 80, 80))
                    
                else:
                    pygame.draw.rect(win, light_red, (i[0]*80, i[1]*80, 80, 80))
    

    if is_check_opp:
        if p == 0:
            black_king_index = classes.Black_pieces.index("king")
            black_king_pos = classes.Opp_black_pos[black_king_index]
            pygame.draw.rect(win, red, (black_king_pos[0]*80, black_king_pos[1]*80 , 80, 80))
        elif p == 1:
            white_king_index = classes.White_pieces.index("king")
            white_king_pos = classes.Opp_white_pos[white_king_index]
            pygame.draw.rect(win, red, (white_king_pos[0]*80, white_king_pos[1]*80 , 80, 80))

    elif is_check_you:
        if p == 0:
            white_king_index = classes.White_pieces.index("king")
            white_king_pos = classes.Your_white_pos[white_king_index]
            pygame.draw.rect(win, red, (white_king_pos[0]*80, white_king_pos[1]*80 , 80, 80))
        elif p == 1:
            black_king_index = classes.Black_pieces.index("king")
            black_king_pos = classes.Your_black_pos[black_king_index]
            pygame.draw.rect(win, red, (black_king_pos[0]*80, black_king_pos[1]*80 , 80, 80))

        



    draw_pieces()
    draw_border()
    show_captured_pieces()
    surrender_img = fonts.render(surrender_text, True, (255,0,0))
    
    win.blit(surrender_img ,(650, 570))

    pygame.display.update()

def start(t):
    global win, p, your_turn, x_cord, y_cord, valid_moves, is_selected, start_piece, black_image_list, white_image_list, is_check_you, prev_move, now_move
    p = t
    if p == 0:
        your_turn = True
    prev_move = ()

    win = pygame.display.set_mode((840, 640))
    pygame.display.set_caption("Chess Game")
    while True:
        clock.tick(60)
        update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if p == 0:
                    Host.conn.close()
                elif p == 1:
                    Join.client.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x_cord = event.pos[0] // 80
                y_cord = event.pos[1] // 80
                click_cord = (x_cord, y_cord)

                print("click_cord: " , click_cord)

                if your_turn:
                    if p == 0:
                        if click_cord in classes.Your_white_pos:
                            valid_moves = []
                            selected = classes.Your_white_pos.index(click_cord)
                            start_piece = classes.White_pieces[selected]
                            is_selected = True
                            check_white_valid_moves(selected)
                            check_unchecking(selected)
                            
                            print("valid_moves: " , valid_moves)

                        elif click_cord in valid_moves and is_selected:
                            prev_move = classes.Your_white_pos[selected]
                            if not king_moved:
                                check_king_moved(start_piece, selected)
                                if not rook1_moved or not rook2_moved:
                                    check_rook_moved(start_piece, selected)
                            pos = classes.Your_white_pos[selected]
                            if start_piece == "king" and click_cord in [(pos[0] + 2, pos[1]), (pos[0] - 2, pos[1])]:
                                castle(click_cord, pos)
                            
                            classes.Your_white_pos[selected] = click_cord
                        
                            if click_cord in classes.Opp_black_pos:
                                black_pos = classes.Opp_black_pos.index(click_cord)
                                add_to_captures(black_pos)
                                classes.Black_pieces.pop(black_pos)
                                classes.Opp_black_pos.remove(click_cord)
                                black_image_list.pop(black_pos)
                            
                            valid_moves= []
                            is_selected = False
                            check_Check()
                            now_move = click_cord
                            
                            send_data(black_image_list, white_image_list, classes.White_pieces, classes.Black_pieces,
                                      classes.Your_white_pos, classes.Opp_black_pos)
                            
                            your_turn = False
                            is_check_you = False

                        elif click_cord not in valid_moves and is_selected:
                            valid_moves = []
                            is_selected = False

                    elif p == 1:
                        if click_cord in classes.Your_black_pos:
                            valid_moves = []
                            selected = classes.Your_black_pos.index(click_cord)
                            start_piece = classes.Black_pieces[selected]
                            is_selected = True
                            check_black_valid_moves(selected)
                            
                            check_unchecking(selected)
                            print("valid_moves: " , valid_moves)

                        elif click_cord in valid_moves and is_selected:
                            prev_move = classes.Your_black_pos[selected]
                            if not king_moved:
                                
                                check_king_moved(start_piece, selected)
                                if not rook1_moved or not rook2_moved:
                                    
                                    check_rook_moved(start_piece, selected)
                            pos = classes.Your_black_pos[selected]
                            if start_piece == "king" and click_cord in [(pos[0] + 2, pos[1]), (pos[0] - 2, pos[1])]:
                                castle(click_cord, pos)
                            
                            classes.Your_black_pos[selected] = click_cord
                                

                            if click_cord in classes.Opp_white_pos:
                                white_pos = classes.Opp_white_pos.index(click_cord)
                                captured_white_pieces.append(classes.Opp_white_pos[selected])
                                classes.White_pieces.pop(white_pos)
                                classes.Opp_white_pos.remove(click_cord)
                                white_image_list.pop(white_pos)

                            valid_moves= []
                            is_selected = False
                            check_Check()
                            now_move = click_cord

                            send_data(black_image_list, white_image_list, classes.White_pieces, classes.Black_pieces,
                                      classes.Your_black_pos, classes.Opp_white_pos)
                            
                            your_turn = False
                            is_check_you = False

                        elif click_cord not in valid_moves and is_selected:
                            valid_moves = []
                            is_selected = False
        if is_checkmate_you:
            pygame.quit()
            sys.exit()
        
