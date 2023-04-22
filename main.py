import pygame, sys
from button import Button
from pygame.locals import *
import random


pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))


BG = pygame.image.load("img/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("img/font.ttf", size)

ROCK_IMG = pygame.image.load("img/rock.png").convert_alpha()
ROCK_IMG = pygame.transform.scale(ROCK_IMG, (15, 15))
PAPER_IMG = pygame.image.load("img/paper.png").convert_alpha()
PAPER_IMG = pygame.transform.scale(PAPER_IMG, (15, 15))
SCISSORS_IMG = pygame.image.load("img/scissors.png").convert_alpha()
SCISSORS_IMG = pygame.transform.scale(SCISSORS_IMG, (15, 15))

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
        self.width = 15
        self.height = 15

    
    def obj_drawing(self):
        if self.obj_type == 'rock':
            self.target = 'scissors'
            # pygame.draw.rect(SCREEN, (0, 105, 176), (self.rec),3)
            SCREEN.blit(ROCK_IMG, self.rec)
        elif self.obj_type == 'paper':
            
            self.target = 'rock'
            # pygame.draw.rect(SCREEN, (0, 255, 176), (self.rec),3)
            SCREEN.blit(PAPER_IMG, self.rec)
        elif self.obj_type == 'scissors':
            
            self.target = 'paper'
            # pygame.draw.rect(SCREEN, (135, 255, 0), (self.rec),3)
            SCREEN.blit(SCISSORS_IMG, self.rec)


clock = pygame.time.Clock()


def move_elements(gamers):
    lngth = len(gamers)
    for i in range(lngth):
            element = gamers[i]
            m = gamers[:i] + gamers[i:]
            if not win_checker(gamers):
                if element.rec.left <= 190 or element.rec.right >= 1020:
                    element.speed_x *= -1
        
                if element.rec.top <= 190 or element.rec.bottom >= 520:
                    element.speed_y *= -1
                
                        
                    
                element.rec.x += element.speed_x
                element.rec.y += element.speed_y
        
                for j in range(len(m)):
                    maybe_target = m[j]
                    if element.rec.colliderect(maybe_target.rec) and maybe_target.obj_type == element.target:
                        maybe_target.obj_type = element.obj_type
                        # print(f"element: {element.obj_type}", element.rec.x, element.rec.y)
                        # print(f"target: {maybe_target.obj_type}", maybe_target.rec.x, maybe_target.rec.y)
            
                
            element.obj_drawing()


rocks_score = 0
papers_score = 0
scissors_score = 0


def win_checker(gamers):
    total = len(gamers)
    global rocks_score
    global papers_score
    global scissors_score
    rocks_score = 0
    papers_score = 0
    scissors_score = 0 
    for gamer in gamers:
        if gamer.obj_type == 'rock':
            rocks_score += 1
        elif gamer.obj_type == 'paper':
            papers_score +=1
        elif gamer.obj_type == 'scissors':
            scissors_score +=1
    if rocks_score == total:
        return 'Rocks Won!'
    if papers_score == total:
        return 'Papers Won!'
    if scissors_score == total:
        return 'Scissors Won!'
    return False

def shield_bar(total, player_shield):
    '''display the graphic and track shield for the gamers'''

    persent = player_shield*100//total

    if persent >= 100:
        player_shield_color = (124,252,0)
    elif persent > 75:
        player_shield_color = (124,252,0)
    elif persent > 50:
        player_shield_color = (255,255,0)
    else:
        player_shield_color= (255,160,122)
    return persent, player_shield_color

def drow_schield(team_name, total, score, top=5, top_corner=7):
    if team_name == 'papers':
        total+=40 
        top_corner+=40
    elif team_name == 'scissors':
        total+=80 
    player_shield_color, persent = shield_bar()
    pygame.draw.rect(SCREEN, (220,220,220), (5, top, 104, 24), 3)
    pygame.draw.rect(SCREEN, player_shield_color, (7, top_corner, persent, 20))
    TEAM_NAME = get_font(10).render("rocks", True, "White")
    TEAM_RECT = TEAM_NAME.get_rect(center=(144, 15)) 
    SCREEN.blit(TEAM_NAME, TEAM_RECT) 
    
def play():
    
    pygame.display.set_caption("Play")
    gamers = []
    n = random.randint(50, 300)
    # n = 5
    for i in range(n):
        paper = RPS()
        gamers.append(paper)
    
    total = len(gamers)
    
    while True:
        clock.tick(60)
        PLAY_MOUSE_POS = pygame.mouse.get_pos()


        
        SCREEN.fill("black")
        rec = Rect(random.randrange(200, 1000, 1), random.randrange(200, 500, 1), 10, 10)
        
        # player_rect = player_image.get_rect(center=(300,200))
        # pygame.Surface.blit()
        
        move_elements(gamers)
        winner = win_checker(gamers)

        drow_schield("rocks", total, rocks_score)
        # display score
        persent, player_shield_color = shield_bar(total, rocks_score)
        pygame.draw.rect(SCREEN, (220,220,220), (5, 5, 104, 24), 3)
        pygame.draw.rect(SCREEN, player_shield_color, (7, 7, persent, 20))
        TEAM_NAME = get_font(10).render("rocks", True, "White")
        TEAM_RECT = TEAM_NAME.get_rect(center=(144, 15)) 
        SCREEN.blit(TEAM_NAME, TEAM_RECT) 

        persent, player_shield_color = shield_bar(total, papers_score)
        pygame.draw.rect(SCREEN, (220,220,220), (5, 45, 104, 24), 3)
        pygame.draw.rect(SCREEN, player_shield_color, (7, 47, persent, 20))   
        TEAM_NAME = get_font(10).render("papers", True, "White")
        TEAM_RECT = TEAM_NAME.get_rect(center=(149, 55)) 
        SCREEN.blit(TEAM_NAME, TEAM_RECT)

        persent, player_shield_color = shield_bar(total, scissors_score)
        pygame.draw.rect(SCREEN, (220,220,220), (5, 95, 104, 24), 3)
        pygame.draw.rect(SCREEN, player_shield_color, (7, 97, persent, 20))   
        TEAM_NAME = get_font(10).render("scissors", True, "White")
        TEAM_RECT = TEAM_NAME.get_rect(center=(157, 105)) 
        SCREEN.blit(TEAM_NAME, TEAM_RECT)
        
        PLAY_TEXT = get_font(40).render("Observe the game!" if not winner else "We have Winner!", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        if winner:
            WON_TEXT = get_font(40).render(winner, True, "Yellow")
            WON_RECT = PLAY_TEXT.get_rect(center=(715, 330))
            SCREEN.blit(WON_TEXT, WON_RECT)

        PLAY_BACK = Button(image=None, pos=(820, 600), 
                            text_input="BACK", font=get_font(50), base_color="White", hovering_color="Red")
        PLAY_RESTART = Button(image=None, pos=(500, 600), 
                            text_input="RESTART", font=get_font(50), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_RESTART.changeColor(PLAY_MOUSE_POS)
        PLAY_RESTART.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_RESTART.checkForInput(PLAY_MOUSE_POS):
                    play()

        pygame.display.update()
        
    
def options():
    pygame.display.set_caption("Options")
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
    pygame.display.set_caption("Menu")
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("img/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("img/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("img/Quit Rect.png"), pos=(640, 550), 
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