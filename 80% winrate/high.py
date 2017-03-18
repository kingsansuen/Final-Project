import pygame
import sys
from pygame import *
from sys import exit
from random import randint
import random
import numpy as np
import time

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
resolution = 10
alpha = 0.5
l = 0.9
view = False;
wincount = 0.0
matchcount = 0.0
fname2 = "Winrate"

Rules = {
    'Alive':0,
    'Dead':-1000,
    'Win':100,
    'Hit':5
}

Q = np.zeros((840/resolution,1200/resolution,2,2))
R = 0

if len(sys.argv)>1:
    fname = str(sys.argv[1]).replace('.npz','')
    recordName = fname + ".txt"
    try:
         data = np.load(str(fname)+'.npz')
         if data is not None:
             try:
                 player1_score = int(data['playerS'])
                 player2_score = int(data['aiS'])
                 Q = data["memory"]
                 s = "Load data from " + str(fname) +".npz successfully."
                 print (s)
             except:
                 sys.exit("Error: Can't load from input")
    except IOError:
        s = "Cannot find file from " + str(fname) + ".npz, New file created."
        print (s)
else:
    sys.exit("Error: No file Name provided.")




while True:



    # check state
    diff_x = (ball_x+20)/resolution
    diff_y = (ball_y - player1_y)/resolution
    if ball_speed_x<0:
        x_dir = 0
    elif ball_speed_x>0:
        x_dir = 1

    #action 0=up 1=stay 2=down
    #chosenaction = randint (0,2)
    possibleaction = Q[diff_x,diff_y,x_dir,:]
    maxs = [i for i,x in enumerate(possibleaction) if x == np.argmax(possibleaction)]
    if len(maxs)>1:
        chosenaction=random.choice(maxs)
    else:
        chosenaction=np.argmax(possibleaction)
    R = Rules ["Alive"]




    screen.fill ((0,0,0))
    score1 = font.render(str(player1_score), True,(255,255,255))
    score2 = font.render(str(player2_score), True,(255,255,255))
    for i in range(30):
        n = i*20
        pygame.draw.line(screen, white, (400,n), (400,n+10) , 2)
    screen.blit(score1,(800/4,100))
    screen.blit(score2,(800/4*3,100))
    ball = ball_x, ball_y
    ballrect = Rect((ball_x-10,ball_y-10),(20,20))
    player1 = Rect((player1_x,player1_y),(playersize_x, playersize_y))
    player2 = Rect((player2_x,player2_y),(playersize_x, playersize_y))



    isPressed = False
    for event in pygame.event.get():
        if event.type == QUIT:
            np.savez(fname,playerS = player1_score, aiS = player2_score, memory=Q )
            s="Data saved in " + str(fname) + ".npz"
            print(s)
            exit()
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                view = True;
            if event.key == K_UP:
                view = False;

    if chosenaction == 0:
        isPressed = True
        if player1_move > -maxspeed-3:
            player1_move -= accelerate*3
    elif chosenaction == 1:
        isPressed = True
        if player1_move < maxspeed+3:
            player1_move += accelerate*3

    #if chosenaction == 1:
    #    isPressed = False
    #    if player1_move > 0:
    #        player1_move -= 1
    #    elif player1_move < 0:
    #        player1_move += 1
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
        R = Rules ["Hit"]
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
        R = Rules ["Dead"]
        player2_score += 1
        ball_x = 800/2
        ball_y = 600/2
        ball_speed_x = random.choice([5,-5])
        ball_speed_y = randint(-5,5)
        if (player1_score+player2_score)%100 == 0 and player2_score>0:
            with open(recordName,"a") as myfile:
                s = str(player1_score+player2_score) + "," + str(player1_score) + "\n"
                myfile.write(s)
        matchcount += 1.0
        if matchcount >= 100:
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
        framecount = False;
        if player1_move == 0:
            i = randint(0,1)
            if i == 0:
                ball_speed_y += 1
            if i == 1:
                ball_speed_y -= 1
    elif ball_x >= 800+20:
        R = Rules ["Win"]
        np.savez(fname,playerS = player1_score, aiS = player2_score, memory=Q )
        s="Data saved in " + str(fname) + ".npz"
        print(s)
        framecount = False;
        player1_score += 1
        ball_x = 800/2
        ball_y = 600/2
        ball_speed_x = random.choice([5,-5])
        ball_speed_y = randint(-5,5)
        if (player1_score+player2_score)%100 == 0 and player2_score>0:
            with open(recordName,"a") as myfile:
                s = str(player1_score+player2_score) + "," + str(player1_score) + "\n"
                myfile.write(s)
        matchcount += 1.0
        wincount += 1.0
        if matchcount >= 100:
            with open(fname2 + ".txt","a") as myfile:
                s = str(player1_score+player2_score) + "," + str(float(wincount)/float(matchcount)*100.0) + "\n"
                myfile.write(s)
                print ("saved winrate")
            matchcount = 0.0
            wincount = 0.0


    if ball_y >= 600-10:
        ball_speed_y = -ball_speed_y
        ball_y = 600-15
    elif ball_y <= 10:
        ball_speed_y = -ball_speed_y
        ball_y = 15

    ball = ball_x, ball_y
    ballrect = Rect((ball_x-10,ball_y-10),(20,20))
    player1 = Rect((player1_x,player1_y),(playersize_x, playersize_y))
    player2 = Rect((player2_x,player2_y),(playersize_x, playersize_y))

    pygame.draw.rect(screen, white, player1 , 0)
    pygame.draw.rect(screen, white, player2 , 0)
    pygame.draw.circle(screen, white, ball, ball_radius, 0)


    #Most important part (Use of algorithm)
    new_diff_x = (ball_x+20)/resolution
    new_diff_y = (ball_y - player1_y)/resolution
    if ball_speed_x<0:
        new_x_dir = 0
    elif ball_speed_x>0:
        new_x_dir = 1
    Q[diff_x,diff_y,x_dir,chosenaction] = Q[diff_x,diff_y,x_dir,chosenaction]+alpha*(R+l*np.amax(Q[new_diff_x,new_diff_y,new_x_dir])-Q[diff_x,diff_y,x_dir,chosenaction])




    pygame.display.update()
    if view == True:
        fpsClock.tick(60)
    else:
        pass
