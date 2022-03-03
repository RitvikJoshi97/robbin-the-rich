import pygame as pg
import sys

def endGameCredits(total_money, winner):
    width = 800
    height = 600

    #creating screen
    screen = pg.display.set_mode((width,height))

    screen.fill((0, 0, 0))

    bg = pg.image.load("code/assets/images/bg.png")
    screen.blit(bg, (0,0))


    font = pg.font.Font('freesansbold.ttf', 24)
    if winner:
        score1 = font.render("My lord! You really know how to play this game!" , True, (255, 255, 255))
        screen.blit(score1, (10,50))
        score2 = font.render("You got a total score of £"+ str(total_money) +"! Tax the rich!", True, (255, 255, 255))
        screen.blit(score2, (10,80))
    else:
        score = font.render("You failed to Rob the Rich! Millions died of hunger...", True, (255, 255, 255))
        screen.blit(score, (10, 50))

    opportunities = font.render("There's always anther try ;)", True, (255,255,255))
    screen.blit(opportunities, (10, 110))

    press_to_continue = font.render("Press any key to continue", True, (255, 255, 255))
    screen.blit(press_to_continue,(10,height-120))    

    credits = font.render("Made with <3 by : Ritvik, Danyal, Karlo, Jack, Tanya and Shefali", True, (255, 255, 255))
    screen.blit(credits,(10,height-60))



    
    while True:
        for event in pg.event.get():
            # QUIT THE GAME
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                return "menu"

        pg.display.update()

    return "menu"

    

