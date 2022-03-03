import pygame as pg
import random
import sys
import math
from pygame import mixer
from pygame import time

pg.init()

class GameState:

    def __init__(self, level = 1, levelDifficulty = 0):
        self.level = level
        self.width = 800
        self.height = 600
        self.border = 100 # unused, sigh
        self.levelDifficulty = levelDifficulty
        self.target = self.target() 
        self.background = pg.image.load('code/assets/images/bg.png')
        self.foreground = pg.image.load('code/assets/images/fg.png')
        self.background_x = 0
        self.background_y = 0
        
    
    def target(self):
        return 50000*self.level*(self.levelDifficulty+1)

class Hero:
    def __init__(self, char = "robin1", x_pos = 15, y_pos = 270, change_y_by= 0, arrow_state = "ready", money = 0):
        self.cur_img = 1    
        self.char = char 
        self.img = pg.image.load("code/assets/images/"+self.char+"/"+str(self.cur_img)+".png")
        self.y_upper_limit = gamestate.height - gamestate.border
        self.y_lower_limit = gamestate.height/4      
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.change_y_by = change_y_by
        self.rapid_time = None # used for rapidArrow
        self.shadow_hero_left = 1


        # arrow_state 
        # ["ready", "fire", "rapid"]
        self.arrow_state = arrow_state
        self.arrow = None
        self.money = money


    def move(self,type, key):
        #handle KEYUP
        if type == pg.KEYDOWN:
            if key == pg.K_UP:
                self.change_y_by = -5
            if key == pg.K_DOWN:
                self.change_y_by = 5

        #handle KEYDOWN
        if type == pg.KEYUP:
            if key == pg.K_UP or key == pg.K_DOWN:
                self.change_y_by = 0


    def imgChanger(self):
        if self.cur_img == 9:
            self.cur_img = 1
        else:
            self.cur_img += 1

        self.img = pg.image.load("code/assets/images/"+self.char+"/"+str(self.cur_img)+".png")

    
    
    def fired_arrow(self):
        if self.arrow.x_pos > gamestate.width:
            self.arrow_state = "ready"
            self.arrow = None
        else:
            # check collision for each opponent
            for each in opponents:
                if self.arrow.checkCollision(each.x_pos, each.y_pos) == True:
                    # destroy arrow object
                    self.arrow_state = "ready"
                    self.arrow = None

                    # create the money object
                    x = each.x_pos  # next line was becoming too long to read
                    y = each.y_pos  # remove if causing issues with time
                    obstacle.append(random.choice([Money(x, y), Money(x, y), Money(x, y), LawSuit(x, y)]))
                    coindropsound = mixer.Sound("code/assets/sounds/coindrop.wav")
                    coindropsound.play(loops=0)
                    coindropsound.stop()
                    return
        

class Shadow_hero(Hero):
    def __init__(self):
        self.char = "robin0"
        self.cur_img = 1
        self.img = pg.image.load("code/assets/images/"+self.char+"/"+str(self.cur_img)+".png")
        self.x_pos = 100
        # self.x_pos = random.randrange(30, 200)
        self.y_pos = random.randrange(gamestate.height/4, gamestate.height)
        self.direction = 1  # random.choice([-1, 1])
        self.speed = 10
        self.arrow_state = "ready"
        self.timelimit = 10
        self.seconds = 0
        self.creation_time = 0  # time since shadow hero has been created, can be set to disappear after certain secs

    def move(self):
        if self.y_pos <= gamestate.height/4:
            self.direction = +1

        elif self.y_pos >= (gamestate.height-gamestate.border):
            self.direction = -1

        self.y_pos += self.direction * self.speed

    def img(self):
        return



class Opponent:
    def __init__(self):
        self.img = random.choice([pg.image.load('code/assets/images/bezos.png'), pg.image.load('code/assets/images/musk.png'), pg.image.load('code/assets/images/branson.png')])
        self.x_pos = random.randrange(gamestate.width-200, gamestate.width-gamestate.border)
        self.y_pos = random.randrange(0,gamestate.height)
        self.direction = 1#random.choice([-1, 1])
        self.speed = 10
        
    def move(self):
        if self.y_pos <= (gamestate.height/4):
            self.direction = +1

        elif self.y_pos >= (gamestate.height-gamestate.border):
            self.direction = -1
        
        self.y_pos += self.direction * self.speed
        

class Arrow:
    def __init__(self,x_pos, y_pos):
        self.img = pg.image.load('code/assets/images/arrow.png')
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.arrow_speed = 50
        #self.timer = 1000
        
        
    def move(self):
        self.x_pos += self.arrow_speed
        


    def checkCollision(self, opponent_x_pos, opponent_y_pos):
        #checkCollision for arrow and enemy
        mid_x = self.x_pos + 16
        mid_y = self.y_pos + 16

        opponent_mid_x = opponent_x_pos + 60
        opponent_mid_y = opponent_y_pos + 60

        distance = math.sqrt(math.pow(opponent_mid_x - mid_x, 2) + (math.pow(opponent_mid_y - mid_y, 2)))
        if distance < 60:
            return True
        else:
            return False


    
    
class Obstacle():
    def move(self):
        self.x_pos -= self.speed

    def checkCollision(self):
        mid_x = self.x_pos + 16
        mid_y = self.y_pos + 16

        hero_mid_x = hero.x_pos + 60
        hero_mid_y = hero.y_pos + 60
        

        distance = math.sqrt(math.pow(hero_mid_x - mid_x, 2) + (math.pow(hero_mid_y - mid_y, 2)))
        if distance < 60:
            return True
        else:
            return False


class Money(Obstacle):
    def __init__(self,x_pos,y_pos):
        self.img = pg.image.load('code/assets/images/money.png') ## CAN BE IMPOROVED
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = 10
        self.type = "Money"
        self.worth = random.randrange(50000,100000)
        #self.music_ticker = None


class LawSuit(Obstacle):
    def __init__(self,x_pos,y_pos):
        self.img = pg.image.load('code/assets/images/lawsuit.png') ## CAN BE IMPROVED
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = 10
        self.type = "LawSuit"
        self.worth = random.randrange(80000,100000)
        #self.music_ticker = None

class GoldenArrow(Obstacle):
    def __init__(self,x_pos,y_pos):
        self.img = pg.image.load('code/assets/images/gold_arrow.png') ## CAN BE IMPROVED
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = 10
        self.type = "GoldenArrow"
        self.worth = 0 
        #self.music_ticker = None


        
class Subtitle:
    def __init__(self,message,timer = 5):
        self.message = message
        self.timer = timer 


    
def update():

    

    global arrow, goldenArrows ,frames_elapsed, shadow_hero
    # arrow = None
    #get the gamestate  

    ## Get and change the hero's state
    hero.y_pos += hero.change_y_by
    # Edge cases for hero's state
    if hero.y_pos <= hero.y_lower_limit:
        hero.y_pos = hero.y_lower_limit
    elif hero.y_pos >= hero.y_upper_limit:
        hero.y_pos = hero.y_upper_limit


    # Next step image
    hero.imgChanger()

    # Adding hero's state to the screen
    screen.blit(hero.img, (hero.x_pos, hero.y_pos))
    
    # Check events (check if arrow is being shot)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
            hero.move(event.type, event.key)

            if event.key == pg.K_SPACE:
                if hero.arrow_state == "ready":
                    # print("here")
                    # global arrow
                    hero.arrow = Arrow(hero.x_pos,hero.y_pos)
                    # print("arrow's pos: ",arrow.x_pos,arrow.y_pos)
                    hero.arrow_state = "fire"

            if event.key == pg.K_m:
                if shadow_hero == None and hero.shadow_hero_left > 0:
                    shadow_hero = Shadow_hero()
                    shadow_sound = mixer.Sound("code/assets/sounds/merrymen.wav")
                    #shadow_sound.set_volume(levelSFX) #KARLO
                    shadow_sound.play(loops=5)
                    shadow_sound.stop()
                    hero.shadow_hero_left -= 1
                    shadow_hero.creation_time = pg.time.get_ticks()
                    if shadow_hero.arrow_state == "ready":
                        shadow_hero.arrow = Arrow(shadow_hero.x_pos, shadow_hero.y_pos)
                        shadow_hero.arrow_state = "fire"


    if shadow_hero != None:
        shadow_hero.imgChanger()
        if shadow_hero.arrow_state == "ready":
            shadow_hero.arrow = Arrow(shadow_hero.x_pos, shadow_hero.y_pos)
            shadow_hero.arrow_state = "fire"

    # arrow state
    if hero.arrow_state == "fire":
        hero.fired_arrow()

                
    if hero.arrow_state == "rapid":
        # time elapsed since power up was collected
        time_elapsed = pg.time.get_ticks() - hero.rapid_time 
        frames_elapsed = frames_elapsed + 1        
        if time_elapsed < golden_arrow_time_limit:
            if frames_elapsed == frames_per_arrow:
                # append an arrow to the goldenArrows list if it is time to shoot another arrow
                goldenArrows.append(Arrow(hero.x_pos, hero.y_pos))
                
                # reset the frames elapsed var to 0 
                frames_elapsed = 0 
        else:
            hero.arrow_state = "ready"
            hero.rapid_timer = None#pg.time.get_ticks()
            frames_elapsed = 0
    
    if goldenArrows != []:
        for arr in goldenArrows:
            if arr.x_pos > gamestate.width: # if any arrow goes out of bounds
                goldenArrows.remove(arr)
                #arr = None
            else:
                for opp in opponents: # check collision of each arrow with each opponent
                    if arr.checkCollision(opp.x_pos, opp.y_pos):
                        # Remove golden arrow from array 
                        #arr = None
                        goldenArrows.remove(arr)
                        # create Obstacle
                        x, y = opp.x_pos, opp.y_pos
                        #obstacle.append(random.choice([GoldenArrow(x,y)]))
                        obstacle.append(random.choice([Money(x,y),Money(x,y),Money(x,y),LawSuit(x,y)]))
                        coindropsound = mixer.Sound("code/assets/sounds/coindrop.wav")
                        coindropsound.set_volume(levelSFX) #KARLO
                        coindropsound.play(loops=0)
                        coindropsound.stop()
                # move each golden arrow        
                arr.move()
                # render each golden arrow to screeb
                screen.blit(arr.img, (arr.x_pos, arr.y_pos))

    # shadow hero's controller
    if shadow_hero != None:
        if shadow_hero.arrow_state == "fire":
            shadow_hero.fired_arrow()

    if shadow_hero != None and shadow_hero.arrow != None:
        shadow_hero.arrow.move()
        screen.blit(shadow_hero.arrow.img, (shadow_hero.arrow.x_pos, shadow_hero.arrow.y_pos))



    # if arrow object isn't none
    if hero.arrow != None:   
        hero.arrow.move()         
        screen.blit(hero.arrow.img, (hero.arrow.x_pos, hero.arrow.y_pos))

    #check if hero collided with obstacle
    for each in obstacle:
        if each.checkCollision():
            
            if each.type == "Money":
                # Call Subtitle here
                #each.music_ticker = pg.time.get_ticks()
                coinSound = mixer.Sound("code/assets/sounds/coincollect.wav")
                coinSound.set_volume(levelSFX) #KARLO
                coinSound.play(loops=0)
                coinSound.stop()
                subtitles.append(Subtitle("You robbed Elon ;)"))
                hero.money += each.worth
                each.worth = 0

            elif each.type == "LawSuit":
                #each.music_ticker = pg.time.get_ticks()
                lawSound = mixer.Sound("code/assets/sounds/lawsuitcollect.wav")
                lawSound.set_volume(levelSFX) #KARLO
                lawSound.play(loops=0)
                lawSound.stop()
                # Call Subtitle here
                subtitles.append(Subtitle("Jeff put a lawsuit on you, it costed a lot :/"))
                hero.money -= each.worth
                each.worth = 0
            
            elif each.type == "GoldenArrow":
                # Trigger rapid fire
                hero.arrow_state = "rapid"
                hero.rapid_time = pg.time.get_ticks()
        
        else: 
            ## movement of each obstacle
            each.move()
            if each.x_pos >= 0:
                # print("getting here")
                screen.blit(each.img, (each.x_pos, each.y_pos))
            else:
                #each = None
                # print(obstacle)
                obstacle.remove(each)
            ## stop music if 
            #pg.mixer.Channel

    # move the opponent
    for each in opponents:
        each.move()
        screen.blit(each.img, (each.x_pos, each.y_pos))


    # Shadow Hero firing controller
    if shadow_hero != None:
        shadow_hero.move()
        s = pg.time.get_ticks()
        shadow_hero.seconds = (s - shadow_hero.creation_time) / 1000
        #print(shadow_hero.seconds)
        Arrow(shadow_hero.x_pos, shadow_hero.y_pos)

        screen.blit(shadow_hero.img, (shadow_hero.x_pos, shadow_hero.y_pos))
        if shadow_hero.seconds >= shadow_hero.timelimit:
            shadow_hero.seconds = 0
            shadow_hero = None



    # subtitle
    for each in subtitles:
        if each.timer <= 0:
            subtitles.remove(each)
        else:
            font = pg.font.Font('freesansbold.ttf', 12)
            screen.blit(font.render(str(each.message), True, (255,255,255)), (gamestate.width/2, gamestate.height - 20))
            each.timer -= 1 
     

    # score
    font = pg.font.Font('freesansbold.ttf', 32)
    screen.blit(gamestate.foreground, (gamestate.background_x,gamestate.background_y))
    score = font.render("Score : £" + str(hero.money), True, (255, 255, 255))
    screen.blit(score, (10, 10))
    targ = font.render("Target : £" + str(gamestate.target), True, (255, 255, 255))
    screen.blit(targ, (10, 50))
    MerryMen = font.render("Merry Men left : " + str(hero.shadow_hero_left), True, (255, 255, 255))
    screen.blit(MerryMen, (10, 90))

    time_left = font.render("time left in level: "+str((4000 + (gamestate.background_x-gamestate.width))//fps)+" sec", True, (255,255, 255))
    screen.blit(time_left, (gamestate.width-390,10))

    


def inGame(level, volume, volume_sfx, levelDifficulty, selectedCharacter):
    #update level, player, opponents etc
    #gamestate.level = level

    global fps, gamestate, screen, opponents, obstacle, hero, shadow_hero, clock, goldenArrows, golden_arrow_time_limit, frames_per_arrow, frames_elapsed, subtitles, levelSFX
    levelSFX = volume_sfx
    gamestate = GameState(level, levelDifficulty)

    
    #creating screen
    screen = pg.display.set_mode((gamestate.width,gamestate.height))
    


    opponents= []
    for i in range(gamestate.level):
        opponents.append(Opponent())
    
    # Obstacles list
    obstacle = []
    # global hero

    hero = Hero(selectedCharacter)
    shadow_hero = None
    
    #arrow = None

    ## Rapid fire
    clock = pg.time.Clock()
    goldenArrows = []
    if levelDifficulty == 0:
        fps = 30#100
    elif levelDifficulty == 1:
        fps = 60
    else:
        fps = 90

    golden_arrow_time_limit = 5000 #ms # the number of ms the power up will last
    APS  = 10 # to shoot 10 arrows per second
    frames_per_arrow = fps//APS # no of frames elapsed before the next arrow is shot
    frames_elapsed = 0 # counter of frames elapsed

    # background = pg.image.load('background.jpeg')
    pg.mixer.init()
    mixer.music.load("code/assets/sounds/background.mp3")
    pg.mixer.music.set_volume(volume)
    mixer.music.play(-1)

    subtitles = []

    running = True
    while running == True: #in level loop
        # making the ticks in order of fps
        clock.tick(fps)

        screen.fill((0, 0, 0))
        gamestate.background_x -= 1
        screen.blit(gamestate.background, (gamestate.background_x,gamestate.background_y))

        for event in pg.event.get():
            # QUIT THE GAME
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                hero.move(event.type, event.key)
                if event.key == pg.K_SPACE:
                    if hero.arrow_state == "ready":
                        # global arrow
                        hero.arrow = Arrow(hero.x_pos,hero.y_pos)
                        hero.arrow_state = "fire"
                
                if event.key == pg.K_m:
                    if shadow_hero == None and hero.shadow_hero_left > 0:
                        shadow_hero = Shadow_hero()
                        hero.shadow_hero_left -= 1
                        shadow_hero.creation_time = pg.time.get_ticks()
                        if shadow_hero.arrow_state == "ready":
                            shadow_hero.arrow = Arrow(shadow_hero.x_pos, shadow_hero.y_pos)
                            shadow_hero.arrow_state = "fire"

        

        # end level condition  
        if (hero.money > gamestate.target) or ((gamestate.background_x-gamestate.width) < -4000):
            
            return hero, gamestate
        update()

        ## add fade to black
        #gamestate.background_x-gamestate.width
        screen.set_alpha(50)

        pg.display.update()





