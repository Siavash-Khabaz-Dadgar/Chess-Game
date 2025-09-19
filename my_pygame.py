import pygame, pygame_gui, socket, sys
from _thread import start_new_thread
import time
import Host
import Join
import game
import classes

pygame.init()
pygame.font.init() 
win = pygame.display.set_mode((600, 500))

fonts = pygame.font.SysFont("Comic sans MS", 30)
pygame.display.set_caption("My pygame")

Host_image = pygame.image.load("HOST.png").convert_alpha()
Join_image = pygame.image.load("JOIN.png").convert_alpha()
Menu_image = pygame.image.load("resources/Chess_logo.png").convert_alpha()

input_box = pygame.Rect(200, 200, 200, 35) 
outline = pygame.Rect(198, 198, 204, 39)
user_text = '' 

Host_clicked_image = pygame.image.load("HOST_clicked.png").convert_alpha()
Join_clicked_image = pygame.image.load("JOIN_clicked.png").convert_alpha()

text = "Host IP is: " + Host.ip
text2 = "Waiting for connection..."
text_join = "Enter Host's IP:"
text_invalid_ip = "Invalid IP Address"

active = False


    
Host_button = classes.Button(80, 300, Host_image, 0.25, Host_clicked_image)
Join_button = classes.Button(350, 300, Join_image, 0.25, Join_clicked_image)
Logo = classes.Imager(175, 100, Menu_image, 0.2)


"""---------------------------------------------------------------------------function for Host button----------------------------------------------------------------------------"""
def Host_f():
    win.fill((179, 242, 239))
    Join_button.draw()
    Host_button.draw_alt()
    Logo.draw()
    pygame.display.update()
    time.sleep(0.1)
    print("Host")
    start_new_thread(Host.connecter, ())
    while True:
        win.fill((179, 242, 239))
        img = fonts.render(text, True, (0,0,0))
        img2 = fonts.render(text2, True, (0,0,0))
        win.blit(img, (100, 150))
        win.blit(img2, (100, 250))
        if Host.connected:

            #START of GAME as WHITE and host
            game.start(0)

            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Host.s.close()
                sys.exit()
        pygame.display.update()
    
"""---------------------------------------------------------------------------function for Join button----------------------------------------------------------------------------"""


def input_ip():
    win.fill((179, 242, 239))
    Join_button.draw_alt()
    Host_button.draw()
    Logo.draw()
    pygame.display.update()
    print("Join")

    time.sleep(0.1)
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((600, 500))
    
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(150,240,300,50), manager=manager, object_id='#main_text_entry')
    text_input.set_text_length_limit(15)
    got_ip = False
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry':
                Join.ip = text_input.get_text()
                got_ip = True
                start_new_thread(Join.Joiner, ())


            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)
        img = fonts.render(text_join, True, (0,0,0))
        win.fill((179, 242, 239))
        win.blit(img, (180, 200))
        if got_ip and Join.connected:
            break
        if got_ip and not Join.connected:
            img2 = fonts.render(text_invalid_ip, True, (255,0,0))
            win.blit(img2, (170, 360))
        manager.draw_ui(win)
        pygame.display.update()
    
    #START of GAME as BLACK and Join
    game.start(1)

"""---------------------------------------------------------------------------function main menu and start----------------------------------------------------------------------------"""


def lobby():
    
    while True:
        win.fill((179, 242, 239))
        Host_button.draw()
        Join_button.draw()
        Logo.draw()
        Host_check = Host_button.clicked()
        Join_check = Join_button.clicked()
        if Host_check:
            Host_f()
            break

        elif Join_check:
            input_ip()
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    


    
if __name__ == "__main__":
    lobby()
