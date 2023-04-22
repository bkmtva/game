import pygame, sys
from button import Button
from pygame.locals import *
import random


pygame.init()

SCREEN = pygame.display.set_mode((1280, 650))


BG = pygame.image.load("img/Background.png")


def get_font(size): 
    return pygame.font.Font("img/font.ttf", size)






ROCK_IMG = pygame.image.load("img/rock.png").convert_alpha()
ROCK_IMG = pygame.transform.scale(ROCK_IMG, (15, 15))
PAPER_IMG = pygame.image.load("img/paper.png").convert_alpha()
PAPER_IMG = pygame.transform.scale(PAPER_IMG, (15, 15))
SCISSORS_IMG = pygame.image.load("img/scissors.png").convert_alpha()
SCISSORS_IMG = pygame.transform.scale(SCISSORS_IMG, (15, 15))


teams = ['rock', 'paper', 'scissors']



class RPS(object):

    def __init__(self):
        self.team_name = random.choice(teams)
        self.speed_x = 1
        self.speed_y = 1
        if self.team_name == 'rock':
            self.target = 'scissors'
        elif self.team_name == 'paper':
            self.target = 'rock'
        elif self.team_name == 'scissors':
            self.target = 'paper'
        self.obj_spawn()
        self.rec = Rect(random.randrange(190, 990, 1), random.randrange(200, 500, 1), self.width, self.height)
        

    def obj_spawn(self):
        self.width = 15
        self.height = 15

    
    def obj_drawing(self):
        if self.team_name == 'rock':
            self.target = 'scissors'
            # pygame.draw.rect(SCREEN, (0, 105, 176), (self.rec),3)
            SCREEN.blit(ROCK_IMG, self.rec)
        elif self.team_name == 'paper':
            
            self.target = 'rock'
            # pygame.draw.rect(SCREEN, (0, 255, 176), (self.rec),3)
            SCREEN.blit(PAPER_IMG, self.rec)
        elif self.team_name == 'scissors':
            
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
                element.rec.x += element.speed_x
                element.rec.y += element.speed_y
                if (element.rec.left <= 200 and element.speed_x < 0)  or (element.rec.right >= 1000 and element.speed_x > 0):
                        element.speed_x *= -1
        
                if (element.rec.top <= 200 and element.speed_y < 0) or (element.rec.bottom >= 500 and element.speed_y > 0):
                    element.speed_y *= -1
             
                

                tollerance = 7
                for maybe_target in m:
                    if element != maybe_target and element.rec.colliderect(maybe_target.rec):
                        if maybe_target.team_name == element.target:
                            maybe_target.team_name = element.team_name
                        if abs(maybe_target.rec.top - element.rec.bottom) < tollerance and element.speed_y > 0:
                            element.speed_y*=-1
                        elif abs(maybe_target.rec.bottom - element.rec.top) < tollerance and element.speed_y < 0:
                            element.speed_y*=-1
                        elif abs(maybe_target.rec.right - element.rec.left) < tollerance and element.speed_x < 0:
                            element.speed_x*=-1
                        elif abs(maybe_target.rec.left - element.rec.right) < tollerance and element.speed_x > 0:
                            element.speed_x*=-1
                    
                    
                     
               
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
        if gamer.team_name == 'rock':
            rocks_score += 1
        elif gamer.team_name == 'paper':
            papers_score +=1
        elif gamer.team_name == 'scissors':
            scissors_score +=1
    if rocks_score == total:
        return 'Rocks Won!'
    if papers_score == total:
        return 'Papers Won!'
    if scissors_score == total:
        return 'Scissors Won!'
    return False


def drow_schield(team_name, total, score):
    top = 20
    top_corner = 18.5
    top_name = 30
    left_name = 164
    if team_name == 'papers':
        top += 40 
        top_corner += 40
        top_name += 40
        left_name += 5
    elif team_name == 'scissors':
        top += 80
        top_corner += 80
        top_name += 80
        left_name += 14
    persent, player_shield_color = shield_bar(total, score)
    pygame.draw.rect(SCREEN, (220,220,220), (20, top_corner, 104, 24), 3)
    pygame.draw.rect(SCREEN, player_shield_color, (22, top, persent, 20))
    TEAM_NAME = get_font(10).render(team_name, True, "White")
    TEAM_RECT = TEAM_NAME.get_rect(center=(left_name, top_name)) 
    SCREEN.blit(TEAM_NAME, TEAM_RECT) 


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




def play():
    pygame.mixer.music.pause()
    pygame.mixer.music.load('img/gigachad.mp3')

    print("music started playing....")

    #Set preferred volume
    pygame.mixer.music.set_volume(0.2)

    #Play the music
    pygame.mixer.music.play()	
    
    pygame.display.set_caption("Play")
    gamers = []
    n = random.randint(50, 300)

    for i in range(n):
        paper = RPS()
        gamers.append(paper)
    
    total = len(gamers)
    
    while True:
        clock.tick(60)
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        
        
        SCREEN.fill("black")
        

        rec = Rect(200, 200, 800, 310)
        pygame.draw.rect(SCREEN, (255, 255, 0), (rec),3)


        move_elements(gamers)
        winner = win_checker(gamers)

        drow_schield("rocks", total, rocks_score)
        drow_schield("papers", total, papers_score)
        drow_schield("scissors", total, scissors_score)
        
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
    pygame.mixer.music.load('img/music.mp3')

    print("music started playing....")

    #Set preferred volume
    pygame.mixer.music.set_volume(0.2)

    #Play the music
    pygame.mixer.music.play()
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