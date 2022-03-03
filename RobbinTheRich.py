from os import stat
import sys
sys.path.append('code/')
from inGame import inGame
from endLevel import endLevel
from endGameCredits import endGameCredits
import pygame as pg
from mainMenu import mainmenu
from addHighscore import addHighscore

level = 1
max_level = 6
playersave = None
cumalative_score = 0
levelVolume = 0
winner = False
levelDifficulty = 0
selectedCharacter = "robin1"

programIcon = pg.image.load('code/assets/images/icon.png')
pg.display.set_icon(programIcon)

## Start off game with the menu
state = "menu"

## Always run this loop; as the mainMenu already has a end function
while True:
    ## Main menu
    if state == "menu":
        state, levelVolume, levelSFX, levelDifficulty, selectedCharacter = mainmenu()
        level = 1

    ## Check if the game should proceed
    if level > max_level:
        state = "addHighscore"
        winner = True

    if state == "addHighscore":
        state = addHighscore(cumalative_score)
    
    
    ## Call the endGameCredits if the levels are done
    ## Call the menu if the game ends
    if state == "endGame":
        state = endGameCredits(cumalative_score, winner)

    
    ## Start level 
    if state == "play":
        playersave, gamestate = inGame(level, levelVolume, levelSFX, levelDifficulty, selectedCharacter)
        if playersave.money < gamestate.target:
            state = "endGame"
        else:
            endLevel(playersave.money,level)
            cumalative_score += playersave.money
            level += 1
        
        
    
