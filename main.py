import pygame, sys
from button import Button
from pygame.locals import *
import random


pygame.init()

#screen size
SCREEN = pygame.display.set_mode((1200, 650))

#loading backgound imgs for menu and play
BG = pygame.image.load("img/manu_background.png")
BG = pygame.transform.scale(BG, (1200, 650))
BG2 = pygame.image.load("img/play_background.jpg")
BG2 = pygame.transform.scale(BG2, (1200, 650))


def get_font(size): 
    return pygame.font.Font("img/font.ttf", size)


BORDERS_IMG = pygame.image.load("img/borders.png").convert_alpha()
BORDERS_IMG = pygame.transform.scale(BORDERS_IMG, (830, 455))

#images for each team
ROCK_IMG = pygame.image.load("img/rock.png").convert_alpha()
ROCK_IMG = pygame.transform.scale(ROCK_IMG, (15, 15))
PAPER_IMG = pygame.image.load("img/paper.png").convert_alpha()
PAPER_IMG = pygame.transform.scale(PAPER_IMG, (15, 15))
SCISSORS_IMG = pygame.image.load("img/scissors.png").convert_alpha()
SCISSORS_IMG = pygame.transform.scale(SCISSORS_IMG, (15, 15))


team_names = ['rock', 'paper', 'scissors']

clock = pygame.time.Clock()

speed = 1

class RPS(object):

    def __init__(self):
        self.team_name = random.choice(team_names)
        self.width = 15
        self.height = 15

        # random direction for speed 1
        
        self.speed_x = random.choice([abs(speed), -abs(speed)])
        self.speed_y = random.choice([abs(speed), -abs(speed)])

        self.set_target()

        # random place (coordinates) for every gamer
        self.rec = Rect(random.randrange(230, 960, 1), random.randrange(150, 450, 1), self.width, self.height)

    def set_target(self):
        if self.team_name == 'rock':
            self.target = 'scissors'
        elif self.team_name == 'paper':
            self.target = 'rock'
        elif self.team_name == 'scissors':
            self.target = 'paper'
    

    def player_drawing(self):
        self.set_target()
        if self.team_name == 'rock':
            SCREEN.blit(ROCK_IMG, self.rec)
        elif self.team_name == 'paper':
            SCREEN.blit(PAPER_IMG, self.rec)
        elif self.team_name == 'scissors':
            SCREEN.blit(SCISSORS_IMG, self.rec)


def move_elements(players):
    for player in players:
            if not win_checker(players) and TIMER_DONE:
                player.rec.x += player.speed_x
                player.rec.y += player.speed_y

                #border collision
                if (player.rec.left <= 230 and player.speed_x < 0)  or (player.rec.right >= 1000 and player.speed_x > 0):
                        player.speed_x *= -1
        
                if (player.rec.top <= 160 and player.speed_y < 0) or (player.rec.bottom >= 470 and player.speed_y > 0):
                    player.speed_y *= -1
                
                # collision between players
                tollerance = 7
                for maybe_target in players:
                    if maybe_target != player:
                        if player != maybe_target and player.rec.colliderect(maybe_target.rec):
                            if maybe_target.team_name == player.target:
                                maybe_target.team_name = player.team_name
                            if abs(maybe_target.rec.top - player.rec.bottom) < tollerance and player.speed_y > 0:
                                player.speed_y*=-1
                            elif abs(maybe_target.rec.bottom - player.rec.top) < tollerance and player.speed_y < 0:
                                player.speed_y*=-1
                            elif abs(maybe_target.rec.right - player.rec.left) < tollerance and player.speed_x < 0:
                                player.speed_x*=-1
                            elif abs(maybe_target.rec.left - player.rec.right) < tollerance and player.speed_x > 0:
                                player.speed_x*=-1

            player.player_drawing()


rocks_score = 0
papers_score = 0
scissors_score = 0


def win_checker(players):
    total = len(players)
    global rocks_score
    global papers_score
    global scissors_score
    rocks_score = 0
    papers_score = 0
    scissors_score = 0 
    for gamer in players:
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
    '''display the graphic and track shield for the watcher'''

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

    persent, player_shield_color = get_persent_color(total, score)
    pygame.draw.rect(SCREEN, (220,220,220), (20, top_corner, 104, 24), 3)
    pygame.draw.rect(SCREEN, player_shield_color, (22, top, persent, 20))

    TEAM_SCORE = get_font(8).render(str(persent)+'%', True, "White")
    TEAM_RECT = TEAM_SCORE.get_rect(center=(107, top_name)) 
    SCREEN.blit(TEAM_SCORE, TEAM_RECT)  

    TEAM_NAME = get_font(10).render(team_name, True, "White")
    TEAM_RECT = TEAM_NAME.get_rect(center=(left_name, top_name))
    SCREEN.blit(TEAM_NAME, TEAM_RECT) 


def get_persent_color(total, player_shield):
    persent = player_shield*100//total
    if persent > 75:
        player_shield_color = (124,252,0)
    elif persent > 35:
        player_shield_color = (255,255,0)
    else:
        player_shield_color= (255,160,122)
    return persent, player_shield_color



def speed_controller(players, one):
    if win_checker(players): #we we have winner don change speed
        return 
    
    global speed
    if speed == 0 and one == -1:
        return
    speed += one
    
    for player in players:
        if player.speed_x == 0 and player.speed_y == 0:
            
            player.speed_x = random.choice([speed, -speed])
            player.speed_y = random.choice([speed, -speed])
        else:
            if player.speed_x < 0:
                player.speed_x = -speed
            elif player.speed_x > 0:
                player.speed_x = speed
            if player.speed_y < 0:
                player.speed_y = -speed
            elif player.speed_y > 0:
                player.speed_y = speed 



def play_button_controller(PLAY_MOUSE_POS, players):
    PLAY_BACK = Button(image=None, pos=(820, 600), 
                            text_input="BACK", font=get_font(50), base_color="White", hovering_color="Red")
    PLAY_RESTART = Button(image=None, pos=(450, 600), 
                        text_input="RESTART", font=get_font(50), base_color="White", hovering_color="Yellow")
    
    button_img = pygame.image.load("img/Quit Rect.png")
    button_img = pygame.transform.scale(button_img, (150, 40))

    speed_increase = Button(image=button_img, pos=(100, 250), 
                        text_input="faster", font=get_font(20), base_color="White", hovering_color="Green")
    speed_decrease = Button(image=button_img, pos=(100, 300), 
                        text_input="slower", font=get_font(20), base_color="White", hovering_color="Red")

    PLAY_BACK.changeColor(PLAY_MOUSE_POS)
    PLAY_BACK.update(SCREEN)
    PLAY_RESTART.changeColor(PLAY_MOUSE_POS)
    PLAY_RESTART.update(SCREEN)
    speed_increase.changeColor(PLAY_MOUSE_POS)
    speed_increase.update(SCREEN)
    speed_decrease.changeColor(PLAY_MOUSE_POS)
    speed_decrease.update(SCREEN)
    display_speed = get_font(10).render('SPEED '+ str(speed), True, "White")
    SPEED_RECT = display_speed.get_rect(center=(100, 200))
    SCREEN.blit(display_speed, SPEED_RECT)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if speed_increase.checkForInput(PLAY_MOUSE_POS):
                speed_controller(players, 1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if speed_decrease.checkForInput(PLAY_MOUSE_POS):
                speed_controller(players, -1)


TIMER_DONE = False
def play():
    global speed
    speed = 1
    pygame.display.set_caption("Play")

    global TIMER_DONE
    TIMER_DONE = False
    players = []
    total_players_num = random.randint(50, 200)

    for i in range(total_players_num):
        paper = RPS()
        players.append(paper)
    
    
    # fight music on
    pygame.mixer.music.pause()
    pygame.mixer.music.load('img/fight.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    
    
    
    timer = 4200  # milliseconds
    
    
    start_time = pygame.time.get_ticks()
    seconds_left = 3
    while pygame.time.get_ticks() - start_time < timer:
        SCREEN.fill("black")
        SCREEN.blit(BG2, (0, 0))
        move_elements(players)
        rec = Rect(200, 88, 800, 360)
        SCREEN.blit(BORDERS_IMG, rec)
        PLAY_TEXT = get_font(40).render("Observe the game!", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        
        # pygame.display.update()
        seconds_left_repeated = abs((pygame.time.get_ticks() - start_time)//1000-3)
        if seconds_left_repeated < seconds_left:
            seconds_left = seconds_left_repeated
        PLAY_TEXT = get_font(70).render(str(seconds_left if seconds_left != 0 else 'FIGHT'), False, (0,0,0,0))
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 300))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        pygame.display.update()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    TIMER_DONE = True

    

    #gigachad mucis on 
    pygame.mixer.music.pause()
    pygame.mixer.music.load('img/gigachad.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    win_sound = pygame.mixer.Sound('img/tbcontinued.mp3')
    zero_played = True # if win_sound played once it will not play again in one round, couse in one round we have one winner

    while True:
        
        clock.tick(60)

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        #background
        SCREEN.fill("black")
        SCREEN.blit(BG2, (0, 0))

        rec = Rect(200, 88, 800, 360)
        SCREEN.blit(BORDERS_IMG, rec)

        move_elements(players)

        winner = win_checker(players)

        drow_schield("rocks", total_players_num, rocks_score)
        drow_schield("papers", total_players_num, papers_score)
        drow_schield("scissors", total_players_num, scissors_score)
        
        PLAY_TEXT = get_font(40).render("Observe the game!" if not winner else "We have Winner!", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(600, 60))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

       
        if winner:
            if zero_played:
                pygame.mixer.music.pause()
                win_sound.play()
                zero_played = False
            WINNER_TEXT = get_font(40).render(winner, True, "Green")
            WINNER_RECT = WINNER_TEXT.get_rect(center=(630, 300))
            SCREEN.blit(WINNER_TEXT, WINNER_RECT)


        play_button_controller(PLAY_MOUSE_POS, players)

        pygame.display.update()
        
        
        

def main_menu():
    pygame.display.set_caption("Menu")

    #music
    pygame.mixer.music.load('img/music.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    

    while True:

        #set background img
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("img/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("img/Quit Rect.png"), pos=(640, 400), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()