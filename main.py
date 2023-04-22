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
        self.direction = 1
        self.speed_x = 4
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
            pygame.draw.rect(SCREEN, (0, 105, 176), (self.rec),3)
        elif self.obj_type == 'paper':
            # rock_img = pygame.image.load("assets/rock.png").convert_alpha()
            self.target = 'rock'
            pygame.draw.rect(SCREEN, (0, 255, 176), (self.rec),3)

        elif self.obj_type == 'scissors':
            
            self.target = 'paper'
            pygame.draw.rect(SCREEN, (135, 255, 0), (self.rec),3)



clock = pygame.time.Clock()


def move_elements(gamers):
    lngth = len(gamers)
    for i in range(lngth):
            element = gamers[i]
            m = gamers[:i] + gamers[i:]
            if not win_checker(gamers):
                if element.rec.left <= 190 or element.rec.right >= 1010:
                    element.speed_x *= -1
        
                if element.rec.top <= 190 or element.rec.bottom >= 510:
                    element.speed_y *= -1
                
                        
                    
                element.rec.x += element.speed_x
                element.rec.y += element.speed_y
        
                for j in range(len(m)):
                    maybe_target = m[j]
                    if element.rec.colliderect(maybe_target.rec) and maybe_target.obj_type == element.target:
                        maybe_target.obj_type = element.obj_type
                        print(f"element: {element.obj_type}", element.rec.x, element.rec.y)
                        print(f"target: {maybe_target.obj_type}", maybe_target.rec.x, maybe_target.rec.y)
            
                
            element.obj_drawing()
            
def win_checker(gamers):
    total = len(gamers)
    rocks = 0
    papers = 0
    scissors = 0
    for gamer in gamers:
        if gamer.obj_type == 'rock':
            rocks += 1
        elif gamer.obj_type == 'paper':
            papers +=1
        elif gamer.obj_type == 'scissors':
            scissors +=1
    if rocks == total:
        return 'Rocks!'
    if papers == total:
        return 'Papers!'
    if scissors == total:
        return 'Scissors!'
    return False
        

def play():
    
    
    gamers = []
    n = random.randint(50, 300)
    # n = 5
    for i in range(n):
        paper = RPS()
        gamers.append(paper)
    
    # lngth = len(gamers)
    
    while True:
        clock.tick(60)
        PLAY_MOUSE_POS = pygame.mouse.get_pos()


        
        SCREEN.fill("black")
        rec = Rect(random.randrange(200, 1000, 1), random.randrange(200, 500, 1), 10, 10)
        player_image = pygame.image.load("assets/rock.png").convert_alpha()
        # player_rect = player_image.get_rect(center=(300,200))
        pygame.Surface.blit(player_image, SCREEN, rec)
        # SCREEN.blit(player_image, player_rect)
        move_elements(gamers)
        winner = win_checker(gamers)

         
        PLAY_TEXT = get_font(40).render("PLAY screen." if not winner else winner, True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 50))
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