import pygame, sys
from button import Button
from pygame.locals import *
import random


pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

from3 = ['rock', 'paper', 'scissors']



class RPS(object):

    def __init__(self):
        self.obj_type = random.choice(from3)
        self.direction = random.choice([1,-1])
        self.speed_x = 2*self.direction
        self.speed_y = 3
        if self.obj_type == 'rock':
            self.target = 'scissors'
        elif self.obj_type == 'paper':
            self.target = 'rock'
        elif self.obj_type == 'scissors':
            self.target = 'paper'
        self.obj_spawn()
        self.rec = Rect(random.randrange(200, 1000, 1), random.randrange(200, 500, 1), self.width, self.height)
        

    def obj_spawn(self):
        self.width = 10
        self.height = 10

    
    def obj_drawing(self):
        if self.obj_type == 'rock':
            self.target = 'scissors'
            return pygame.draw.rect(SCREEN, (0, 105, 176), (self.rec),3)
        elif self.obj_type == 'paper':
            self.target = 'rock'
            return pygame.draw.rect(SCREEN, (0, 255, 176), (self.rec),3)
        elif self.obj_type == 'scissors':
            self.target = 'paper'
            return pygame.draw.rect(SCREEN, (135, 255, 0), (self.rec),3)



clock = pygame.time.Clock()
def play():
    
    l = []
    n = random.randint(10, 300)
    # n = 5
    for i in range(n):
        paper = RPS()
        l.append(paper)
    

    while True:
        clock.tick(60)
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")
        # print(l)
        for i in l:
            print(i.obj_type, i.target)
            # print(i.left, i.right, i.top, i.bottom)
            if i.rec.left <= 100 or i.rec.right >= 1100:
                i.direction *= -1
                i.speed_x *= i.direction
                i.speed_y *= i.direction
            if i.rec.top <= 100 or i.rec.bottom >= 550:
                i.direction *= -1
                i.speed_x *= i.direction
                i.speed_y *= i.direction
        
                
            
            i.rec.left += i.speed_x
            i.rec.top += i.speed_y
            i.obj_drawing()

         
        PLAY_TEXT = get_font(40).render("PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 30))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 600), 
                            text_input="BACK", font=get_font(60), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()