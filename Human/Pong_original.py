import pygame
from pygame import *
from sys import exit
from random import randint
import numpy as np
import sys
import random

pygame.init()

screen=pygame.display.set_mode((800,600),0,32)
pygame.display.set_caption("Pong Original")
pygame.key.set_repeat(1,0)
fpsClock = pygame.time.Clock()


player1_x = 20
player2_x = 800-25
player1_y = 600/2-35
player2_y = 600/2-35
playersize_x = 10
playersize_y = 60
white = (255,255,255)
ball_x = 800/2
ball_y = 600/2
ball_radius =  10
player1_score = 0
player2_score = 0
accelerate = 3
font = pygame.font.SysFont("calibri",40)
player1_move = 0
player2_move = 0
maxspeed = 10
isPressed = False
player2_moving = False
ball_speed_x = -5
ball_speed_y = -5
framecount = False
frame = 0
fname = "Human"
fname2 = "Winrate"
wincount = 0.0
matchcount = 0.0
show_player1_score = 0
show_player2_score = 0
start = False

recordName = fname + ".txt"
try:
    data = np.load(str(fname)+'.npz')
    if data is not None:
        try:
            player1_score = int(data['playerS'])
            player2_score = int(data['aiS'])
            matchcount = float(data['matchS'])
            wincount = float(data['winS'])
            show_player1_score = int (data['show1'])
            show_player2_score = int (data['show2'])
            s = "Load data from " + str(fname) +".npz successfully."
            print (s)
            print (matchcount)
            print (wincount)
        except:
            sys.exit("Error: Can't load from input")
except IOError:
    s = "Cannot find file from " + str(fname) + ".npz, New file created."
    print (s)



def restart():

    sta = randint(0,4)



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            np.savez(fname,playerS = player1_score, aiS = player2_score, matchS = matchcount, winS = wincount, show1 = show_player1_score, show2 = show_player2_score)
            s="Data saved in " + str(fname) + ".npz"
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if (show_player1_score + show_player2_score) == 10:
                    show_player1_score = 0
                    show_player2_score = 0
                start=True
    screen.fill ((0,0,0))
    intro = font.render("Press Space to start", True,(255,255,255))
    S1 = font.render("Your score: " + str(show_player1_score), True,(255,255,255))
    S2 = font.render("Computer's score: " + str(show_player2_score), True,(255,255,255))
    screen.blit(intro,(800/4+45,100))
    screen.blit(S1,(800/4+45,100+50))
    screen.blit(S2,(800/4+45,100+100))
    pygame.display.update()
    fpsClock.tick(60)

    while start == True:
        isPressed = False
        for event in pygame.event.get():
            if event.type == QUIT:
                np.savez(fname,playerS = player1_score, aiS = player2_score, matchS = matchcount, winS = wincount, show1 = show_player1_score, show2 = show_player2_score)
                s="Data saved in " + str(fname) + ".npz"
                exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    isPressed = True
                    if player1_move > -maxspeed-2:
                        player1_move -= accelerate
                elif event.key == K_DOWN:
                    isPressed = True
                    if player1_move < maxspeed +2:
                        player1_move += accelerate


        screen.fill ((0,0,0))
        score1 = font.render(str(show_player1_score), True,(255,255,255))
        score2 = font.render(str(show_player2_score), True,(255,255,255))
        for i in range(30):
            n = i*20
            pygame.draw.line(screen, white, (400,n), (400,n+10) , 2)
        screen.blit(score1,(800/4,100))
        screen.blit(score2,(800/4*3,100))
        ball = ball_x, ball_y
        ballrect = Rect((ball_x-10,ball_y-10),(20,20))
        player1 = Rect((player1_x,player1_y),(playersize_x, playersize_y))
        player2 = Rect((player2_x,player2_y),(playersize_x, playersize_y))

        if not isPressed:
            if player1_move > 0:
                player1_move -= 1
            elif player1_move < 0:
                player1_move += 1
        player1_y += player1_move

        # Ai movement
        if player2_y+30 > ball_y:
            player2_moving = True
            if player2_move > -maxspeed:
                player2_move -= accelerate
        elif ball_y > player2_y+30:
            player2_moving = True
            if player2_move < maxspeed:
                player2_move += accelerate
        else:
            player2_moving = False

        if not player2_moving:
            if player2_move > 0:
                player2_move -= 1
            elif player2_move < 0:
                player2_move += 1
        player2_y += player2_move

        if player1_y >= 600-70:
            player1_y = 600-70
        if player1_y <= 0:
            player1_y = 0
        if player2_y >= 600-70:
            player2_y = 600-70
        if player2_y <= 0:
            player2_y = 0

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if player1.colliderect(ballrect):
            ball_speed_x = -ball_speed_x
            ball_speed_y = player1_move
            ball_x += 10
            if player1_move == 0:
                i = randint(0,1)
                if i == 0:
                    ball_speed_y += 1
                if i == 1:
                    ball_speed_y -= 1
        elif ball_x <= 0-20:
            player2_score += 1
            if (player1_score + player2_score)>=10:
                if (player1_score + player2_score)%10 == 0:
                    show_player2_score += 1
                    start = False
                else:
                    show_player2_score += 1
            else:
                show_player1_score = player1_score
                show_player2_score = player2_score
            ball_x = 800/2
            ball_y = 600/2
            ball_speed_x = random.choice([5,-5])
            ball_speed_y = randint(-5,5)
            if player2_score != 0:
                with open(fname + ".txt","a") as myfile:
                    s = str(player1_score+player2_score) + "," + str(player1_score) + "\n"
                    myfile.write(s)
                    print ("saved")
            matchcount += 1.0
            if matchcount >= 10:
                with open(fname2 + ".txt","a") as myfile:
                    s = str(player1_score+player2_score) + "," + str((wincount/matchcount)*100.0) + "\n"
                    myfile.write(s)
                    print ("saved winrate")
                    matchcount = 0.0
                    wincount = 0.0



        if player2.colliderect(ballrect):
            ball_speed_x = -ball_speed_x
            ball_speed_y = player2_move
            ball_x -= 10
            if player1_move == 0:
                i = randint(0,1)
                if i == 0:
                    ball_speed_y += 1
                if i == 1:
                    ball_speed_y -= 1
        elif ball_x >= 800+20:
            player1_score += 1
            if (player1_score + player2_score)>=10:
                if (player1_score + player2_score)%10 == 0:
                    show_player1_score += 1
                    start = False
                else:
                    show_player1_score += 1
            else:
                show_player1_score = player1_score
                show_player2_score = player2_score
            ball_x = 800/2
            ball_y = 600/2
            ball_speed_x = random.choice([5,-5])
            ball_speed_y = randint(-5,5)
            if player2_score != 0:
                with open(fname + ".txt","a") as myfile:
                    s = str(player1_score+player2_score) + "," + str(player1_score) + "\n"
                    myfile.write(s)
                    print ("saved")
            matchcount += 1.0
            wincount += 1.0
            if matchcount >= 10:
                with open(fname2 + ".txt","a") as myfile:
                    s = str(player1_score+player2_score) + "," + str(float(wincount)/float(matchcount)*100.0) + "\n"
                    myfile.write(s)
                    print ("saved winrate")
                matchcount = 0.0
                wincount = 0.0








        if ball_y >= 600-10:
            ball_speed_y = -ball_speed_y
        elif ball_y <= 10:
            ball_speed_y = -ball_speed_y


        ball = ball_x, ball_y
        ballrect = Rect((ball_x-10,ball_y-10),(20,20))
        player1 = Rect((player1_x,player1_y),(playersize_x, playersize_y))
        player2 = Rect((player2_x,player2_y),(playersize_x, playersize_y))


        pygame.draw.rect(screen, white, player1 , 0)
        pygame.draw.rect(screen, white, player2 , 0)
        pygame.draw.circle(screen, white, ball, ball_radius, 0)



        pygame.display.update()
        fpsClock.tick(60)
