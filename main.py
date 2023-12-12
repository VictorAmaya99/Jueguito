import pygame
from sys import exit
from config import *
from pygame.locals import *
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"Timer: {current_time}", False, (BLACK))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 380:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True
  
def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

#Inicializa modulos de pygame:
pygame.init()

#Configuracion de la pantalla principal
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("My first game")
clock = pygame.time.Clock()

#Superficie:
Surface = pygame.transform.scale(pygame.image.load("./src/assets/surface.png"), SCREEN_SIZE)

#Fuente:
test_font = pygame.font.Font("./src/assets/ShortBaby-Mg2w.ttf", 30)
#TExt0:
# score_surf = test_font.render("Game", False, BLACK)
# score_rect = score_surf.get_rect(center = (400, 50))

game_active = False
start_time = 0
timer = 0

#obstacles:
#Snail
snail_frame_1 = pygame.image.load("./src/assets/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("./src/assets/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
#Fly
fly_frame1 = pygame.image.load("./src/assets/Fly1.png").convert_alpha()
fly_frame2 = pygame.image.load("./src/assets/Fly2.png").convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]


obstacle_rect_list = []

player_walk_1 = pygame.image.load("./src/assets/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("./src/assets/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("./src/assets/jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,370))
player_gravity = 0

#Intro screen:
player_stand = pygame.image.load("./src/assets/player_stand.png").convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render("Run Run Marcian", False, CUSTOM2)
game_name_rect = game_name.get_rect(center = (400, 80))

game_mesage = test_font.render("Press space tu run", False, CUSTOM2)
game_mesage_rect = game_mesage.get_rect(center = (400, 330))

#Timer:
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 300)


is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE and player_rect.bottom >= 370:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),380)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
        

    #Game part
    if game_active:
        screen.fill(CUSTOM)
        screen.blit(Surface,ORIGIN) 
        timer = display_score()
    
        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 780
        # screen.blit(snail_surf, snail_rect)
        
        #player:
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 370:
            player_rect.bottom = 370
        player_animation()
        screen.blit(player_surf, player_rect)

        #obstacle movement:
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision:
        game_active = collisions(player_rect, obstacle_rect_list)
       
    #Intro
    else:
        screen.fill(GREY)
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 370)
        player_gravity = 0

        timer_message = test_font.render(f"Your Time: {timer} sec", False, CUSTOM2)
        timer_message_rect = timer_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)

        if timer == 0: 
            screen.blit(game_mesage, game_mesage_rect)
        else: 
            screen.blit(timer_message, timer_message_rect)

        

    

    pygame.display.update()
    clock.tick(FPS)

exit()