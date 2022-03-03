
import pygame as pg
import sys
import os
import random
import pandas as pd

import pickle
import time

pg.init()

width, height = 800, 600
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()

FPS = 60
font = pg.font.Font(None, 32)


def addHighscore(cum_score):
    running = True
    username = ""
    max_character = 10
    score = cum_score
    n = 10
    WHITE = (255, 255, 255)

    ## Pandas option
    filename = "scores.txt"
    if filename not in os.listdir('code'):
        with open(filename, "w") as f:
            f.write("username,score")
        
    highscores = pd.read_csv(filename, header=0)

    ## Lemme know if you want to change to another filetype

    running = False
    if (score > highscores["score"].min()) or (highscores.shape[0] < n):
        running = True

    while running:
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                            
                if event.key == pg.K_BACKSPACE:
                    username = username[0:-1]        
            
                elif event.key == pg.K_RETURN and len(username)>0:  
                    
                    highscores = pd.concat([highscores, pd.DataFrame([[username, score]], columns=["username", "score"])], axis=0)
                    highscores.sort_values("score", ascending=False, inplace=True)                
                    highscores = highscores.iloc[0:n, :]   
                    highscores.to_csv("scores.txt", index=False) 
                    return "endGame"
                else:
                    if len(username) < max_character:
                        username = username + event.unicode
            
            screen.fill((0, 0, 0))

            text = font.render("Enter name, cause you've made it to the leader board!", True, (255, 255, 255))
            screen.blit(text, (10, 10))

            text = font.render(username, True, (255, 255, 255))
            screen.blit(text, (10, 30))
        
        pg.display.update()

        
