import pygame as pg
import pandas as pd
from pygame.locals import *
import sys

# pygame settings
clock = pg.time.Clock()
pg.init()

# can we get the width and height from outOfGame?
width = 800
height = 600
screen = pg.display.set_mode((width,height))
screen.fill((0,0,0))

# game globals
levelVolume = 0.1
levelSFX = 0.1
levelDifficulty = 0
selectedCharacter = "robin1"

# graphics 
font = pg.font.Font('freesansbold.ttf', 32)
font_button = pg.font.Font('code/assets/fonts/BakbakOne-Regular.ttf', 20) 

WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)

# audio 
pg.mixer.init()
pg.mixer.music.load("code/assets/sounds/background.mp3")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(levelVolume)


# helper 

def mouse_obj_collision(x, y, width, height):
    """Function to detect if mouse is on top of a pygame Rect
    ...
    
    Inputs:
    ---
    x, y : float
        - top left coordinates of the pygame.Rect   
        
    width : float
        - width of the rectangle
        
    height : float 
        - height of the rectangle
        
    Output:
    ---
    bool, if mouse is on top of object
    """
    
    # get current mouse position
    mx_pos, my_pos = pg.mouse.get_pos()
    
    # checks if mouse is in region of object
    if (mx_pos > x) and (mx_pos < x + width):
        if (my_pos > y) and (my_pos < y + height):
            return True
    return False

class Button():
    """Creates a Button"""
    def __init__(self, name, x_pos, y_pos, width, height):
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        
    def draw(self):

        # draw button
        pg.draw.rect(screen, WHITE, pg.Rect(self.x_pos, self.y_pos, self.width, self.height))
        
        # add labels
        label = font_button.render(self.name, True, (0,0,0))
        label_rect = label.get_rect(center=(self.x_pos + self.width/2, self.y_pos + self.height/2))
        
        screen.blit(label, label_rect)        
    
    def click(self):
        return mouse_obj_collision(self.x_pos, self.y_pos, self.width, self.height)
        

class Slider():
    """Creates a Slider"""
    def __init__(self, left, top, width, height, choice):
        self.left = left
        self.top = top
        self.width = width
        self.height = height 
        self.choice = choice
    
    def draw(self):
        # draw back_bar (this is just some sort of frame for the slider)
        back_bar = pg.draw.rect(screen, WHITE, pg.Rect(self.left, self.top, self.width, self.height))
        
        # draw the bar as selected by the user, the width is dependent on where the user clicks
        user_bar = pg.draw.rect(screen, BLACK, pg.Rect(self.left, self.top, self.choice, self.height))
        
    def click(self):
        return mouse_obj_collision(self.left, self.top, self.width, self.height)
        
class CharacterPane():
    def __init__(self, name, img, left, top, width, height):
        self.name = name
        self.image = pg.image.load(img)
        self.image_rect = self.image.get_rect()
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        
    def draw(self):
        pane = pg.draw.rect(screen, WHITE, pg.Rect(self.left, self.top, self.width, self.height))
        self.image_rect = self.image.get_rect(center=pane.center)
        screen.blit(self.image, self.image_rect)
        
    def click(self):
        return mouse_obj_collision(self.left, self.top, self.width, self.height)

def charselect():
    
    global selectedCharacter
    highlight = 5
        
    # might need to change how we code the coords int this one
    char1 = CharacterPane("robin1", "code/assets/images/robin1.png", 145, 200, 200, 250)
    char2 = CharacterPane("robin2", "code/assets/images/robin2.png", 360, 200, 200, 250)    
    char_list = [char1, char2]
        
    while True:
        #print(selectedCharacter)
        
        img = pg.image.load("code/assets/images/page_charselect.png")
        screen.blit(img, (0, 0))
        
        returnbutton=Button('Main Menu',350,500,120,50)
        returnbutton.draw()

        for char in char_list:
            if char.name != selectedCharacter:
                char.chosen = False
            else:
                char.chosen = True
                pg.draw.rect(screen, BLACK, pg.Rect(char.left-highlight, char.top-highlight, char.width+(highlight*2), char.height+(highlight*2)))

            char.draw()

        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                
                for char in char_list:
                    if char.click():
                        selectedCharacter = char.name
                        #print(selectedCharacter)
                                        
                if returnbutton.click():
                    return
        
        pg.display.update() 
        
def settings():
    """Runs Settings menu page"""
    global levelVolume, levelSFX, levelDifficulty
    
    running = True
    while running:
        
        img = pg.image.load("code/assets/images/page_settings.png")
        screen.blit(img, (0, 0))

        # draw return button
        return_button = Button('Main Menu', 350, 500, 120, 50)
        return_button.draw()
        
        # add volume slider        
        music_barl, music_bart, barw, barh = 100, 245, 300, 25 
        music_slider = Slider(music_barl, music_bart, barw, barh, levelVolume*barw)
        music_slider.draw()        
        
        # add soundfx slider 
        sfx_barl, sfx_bart = 100, 320
        sfx_slider = Slider(sfx_barl, sfx_bart, barw, barh, levelSFX*barw)
        sfx_slider.draw()
        
        # difficulty 
        difficulty = ["Easy", "Normal", "Hard"]
        diff_button = Button(difficulty[levelDifficulty], 100, 395, 100, 50)
        diff_button.draw()
        
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                  
            if event.type == pg.MOUSEBUTTONDOWN:
                if return_button.click():
                    return

            if event.type == pg.MOUSEBUTTONDOWN:
                
                # get mouse pos
                mx_pos, my_pos = pg.mouse.get_pos()

                # check if mouse pos in rect
                if music_slider.click():
                    # if clicked, get the x position of the mouse and get the relative distance from the slider bar
                    levelVolume = (mx_pos - music_slider.left)/music_slider.width
                    
                    # set global volume level
                    pg.mixer.music.set_volume(levelVolume)

                # check if mouse pos in rect
                if sfx_slider.click():
                    # similar to music_slider logic
                    levelSFX = (mx_pos - sfx_slider.left)/sfx_slider.width

                        
                ## check if mouse pos in button
                if diff_button.click():
                    # if clicked, the moves to the next element of the list
                    # if >=3, the modulo will bring it back to 0
                    levelDifficulty = (levelDifficulty+1)%3
       
                        
            pg.display.update()

def howtoplay():
    """Runs How To Play menu page"""    
    img = pg.image.load("code/assets/images/page_howto.png")
    screen.blit(img, (0, 0))
        
    returnbutton=Button('Main Menu', 575, 455, 120, 50)
    returnbutton.draw()
    
    pg.display.update() 
    while True:
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if returnbutton.click():
                    return
                

def leaderboard(topn=10):
    """Runs Leaderboard menu page"""
    
    running = True
    filename = "scores.txt"
    font_content = pg.font.Font('code/assets/fonts/BakbakOne-Regular.ttf', 24) 
    
    # reads the scores file
    leaderboard = pd.read_csv(filename)
    
    while running:
        
        img = pg.image.load("code/assets/images/page_leaderboard.png")
        screen.blit(img, (0, 0))
        
        returnbutton=Button('Main Menu', 350, 500,120,50)
        returnbutton.draw()
        
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                        
            if event.type == pg.MOUSEBUTTONDOWN:
                if returnbutton.click():
                    return
        
        # prints each line of scores.txt 
        for i in range(topn):
            try:
                name_val, score_val = leaderboard.iloc[i, 0], str(leaderboard.iloc[i, 1]) 
            except:
                # this will be an error if scores.txt contains < 10 elements, if this the case defaults to "-"
                name_val, score_val = "-", "-"
            
            # print score and name
            name = font_content.render(f"{i+1}   {name_val}", True, WHITE)
            score = font_content.render(score_val, True, WHITE)
            screen.blit(name, (250, 200+20*i))
            screen.blit(score, (450, 200+20*i))
        
        pg.display.update()

def mainmenu():
    """Runs Main Menu page"""
    
    # width, height, and placement of buttons
    button_width = 200
    button_height = 50
    row1, row2, row3 = 50, 300, 550
    col1, col2 = 375, 475
    
    play = False
    while play == False:
        
        img = pg.image.load("code/assets/images/page_main.png")
        screen.blit(img, (0, 0))    
        
        # draw the buttons
        play_button=Button('Play', row1, col1, button_width, button_height)
        play_button.draw()
        
        charselect_button=Button('Character Select', row2, col1, button_width, button_height)
        charselect_button.draw()
        
        leaderboard_button=Button('Leaderboard', row3, col1, button_width, button_height)
        leaderboard_button.draw()
        
        settings_button=Button('Settings', row1, col2, button_width, button_height)
        settings_button.draw()
        
        howtoplay_button=Button('How to Play',row2, col2, button_width, button_height)
        howtoplay_button.draw()
        
        exit_button=Button('Exit', row3, col2, button_width, button_height)
        exit_button.draw()

        pg.display.update() 
        
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                    
            # if button is cicked, then it should the run the function associated with the button
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_button.click():
                    return "play", levelVolume, levelSFX, levelDifficulty, selectedCharacter
                
                elif charselect_button.click():
                    charselect()
                    
                elif leaderboard_button.click():        
                    leaderboard()
                    
                elif settings_button.click():
                    settings()
                    
                elif howtoplay_button.click():
                    howtoplay()
                    
                elif exit_button.click():
                    pg.quit()
                    sys.exit()           
    return