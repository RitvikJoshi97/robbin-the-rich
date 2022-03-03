import pygame as pg
import sys
import random

font = pg.font.Font('freesansbold.ttf', 30)


def endLevel(money,level):
    width = 800
    height = 600

    #creating screen
    screen = pg.display.set_mode((width,height))
    screen.fill((0, 0, 0))

    screen.blit(pg.image.load("code/assets/images/bg.png"), (0,0))

    score = font.render("Level "+ str(level) + " score : " + str(money), True, (255, 255, 255))
    screen.blit(score, (10, 50))

    msg1 = font.render("You completed level " + str(level), True, (255, 255, 255))
    screen.blit(msg1, (10, 10))

    msg4 = font.render(random.choice(["Jeff Bezos", "Elon Musk", "Sir Richard Branson"]) + " now has £" + str(201700000000 - money) +'.', True, (255, 255, 255))
    screen.blit(msg4, (10, 200))

    msg5 = font.render("No. of McD meals you bought " + str(int(money/3.29)) +'.', True, (255, 255, 255))
    screen.blit(msg5, (10, 250))

    msg6 = font.render("Press any key to continue", True, (255, 255, 255))
    screen.blit(msg6, (10, 360))

    pg.display.update()


    while True:
        for event in pg.event.get():
            # QUIT THE GAME
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                return
    return