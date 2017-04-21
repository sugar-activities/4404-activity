#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import usmpgames
from gettext import gettext as _
import sys
import random
import time
from usmpgames import *
#from constants import *
#from classes import *
#from methods import *

######################################## constants

GAMEMODE=4

#GAME TIME:

#CARROT SIZE
CARROTMINSIZE = 80
CARROTMAXSIZE = 90

#IMAGES SIZE
bunnySize=175

#Screen Size
WINDOWWIDTH = 1200
WINDOWHEIGHT = 900

#Text Color
TEXTCOLOR = (0, 0, 0)
TITLECOLOR = (173, 255, 47)
      
#Background Color
BACKGROUNDCOLOR = (0, 0, 0)

#FPS (Fames per Second):
FPS = 15


#CARROT VELOCITY
CARROTMINVEL= 4
CARROTMAXVEL = 8

#CARROT VELOCITY FRECUENCY
CARROTVELFREC = 20

#BUNNY MOVING VELOCITY
BUNNYMOVEVEL = 35

#SCORES
maxScore = 0
score =0
#OPERATION RESUlT
result=0


# IMAGES


fruit1Image = pygame.image.load('./media/images/fruit1.png')
fruit2Image = pygame.image.load('./media/images/fruit2.png')

happy=pygame.image.load('./media/images/happycuy.png')
happy=pygame.transform.scale(happy, (bunnySize+25, bunnySize))

sad=pygame.image.load('./media/images/sadcuy.png')
sad=pygame.transform.scale(sad, (bunnySize-25, bunnySize))

invisible=pygame.image.load('./media/images/invisible.png')
invisible=pygame.transform.scale(sad, (bunnySize-25, bunnySize))

looking=pygame.image.load('./media/images/looking.png')
looking=pygame.transform.scale(looking, (bunnySize-45, bunnySize))

message_ok = pygame.image.load('./media/images/bien.png')
message_bad = pygame.image.load('./media/images/mal.png')
rect_ok = message_ok.get_rect()
rect_bad = message_bad.get_rect()

#NUMBERS
number1=0
number2=0
result=0

resultChosen=0

gameOverSound = pygame.mixer.Sound('./media/sounds/gameover.wav')
correctAnswerSound = pygame.mixer.Sound('./media/sounds/aplause.ogg')
musicSound = pygame.mixer.Sound('./media/sounds/menumusic.ogg')

font = pygame.font.SysFont(None, 80)
        
imageList = []
imageList2 = []
        
background = None
bunnyImage = None
bunnyImage = None

bunnyImageF = None
rectBunny = None

n = 0

class Game2(usmpgames.ApplicationState):

    def __init__(self,  game_mode,  next_state = None,  background_image = None, next_cookie = None):
        usmpgames.ApplicationState.__init__(self,  next_state,  background_image, next_cookie)
        self.game_mode = game_mode
        
        global gameOverSound, correctAnswerSound, musicSound
        gameOverSound = pygame.mixer.Sound('./media/sounds/gameover.wav')
        correctAnswerSound = pygame.mixer.Sound('./media/sounds/aplause.ogg')
        musicSound=pygame.mixer.Sound('./media/sounds/menumusic.ogg')
        
        image1= load_image('./media/images/reduced/cuya.gif');
        image2 = load_image('./media/images/reduced/enemy.gif');
        image3 = load_image('./media/images/reduced/enemy1.gif');   
        
        global imageList, imageList2
        imageList = [image1,image2,image3]
        imageList2 = []
        
        global bunnyImage, bunnyImage
        bunnyImage = pygame.image.load('./media/images/cuy.png')
        bunnyImage = pygame.transform.scale(bunnyImage, (bunnySize-45, bunnySize))

        global bunnyImageF, rectBunny
        bunnyImageF=MBSprite(bunnyImage)
        rectBunny = bunnyImageF.rect
        self.new_operation = True

        global background
        background = load_image('./media/images/yard.jpg')


    def entering_state(self, fromStack, cookie):
        usmpgames.ApplicationState.entering_state(self, fromStack, cookie)
        global n
        global GAMEMODE
        n = 0
        GAMEMODE = cookie
        #Get initial time
        global TIMESTART
        TIMESTART= round(time.time(),0)
	global score, a
	score = 0
	a = 0
	self.new_operation = True

    def exiting_state(self, fromStack):
        global score
        self.next_state().clear_all()
        self.next_state().add_text2(
            _(""" Congratulations\n\nYou have got %d points!""") % score,
            color = (0, 0, 0, 0),
            pos = (660, 260),
            rectsize = (380, 390) );
        global gameOverSound, correctAnswerSound, musicSound
        gameOverSound.stop()
        musicSound.stop()
        correctAnswerSound.stop()
        pygame.mixer.music.stop()
        usmpgames.ApplicationState.exiting_state(self, fromStack)

    def input(self,  ms):
        global carrotsBack, carrotsSlow, carrotsQuick, moveRight, moveLeft, score, rectBunny, moveUp
      
        for event in pygame.event.get():
            if event.type == QUIT:
                self.set_running( False ) 
            # KEYDOWN EVENTS 
            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    carrotsBack = True
                if event.key == ord('x'):
                    carrotsSlow = True
                if event.key == ord('c'):
                    carrotsQuick = True
                if event.key == K_LEFT or event.key == ord('a') or event.key == K_KP4 or event.key== K_KP7:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d') or event.key == K_KP6 or event.key== K_KP1:
                    moveLeft = False
                    moveRight = True
                #Up and Down moves disabled
                #if event.key == K_UP or event.key == ord('w') or event.key == K_KP8 or event.key== K_KP9:
                    #moveDown = False
                    #moveUp = True    while(i<number1):

                #if event.key == K_DOWN or event.key == ord('s') or event.key == K_KP2 or event.key== K_KP3:
                    #moveUp = False
                    #moveDown = True
            # KEYUP EVENTS
            if event.type == KEYUP:
                if event.key == ord('z'):
                    carrotsBack = False
                    score = 0
                if event.key == ord('x'):
                    carrotsSlow = False
                    score = 0
                if event.key == ord('c'):
                    carrotsQuick = False
                    score= 0
                if event.key == K_ESCAPE:
                    self.set_running( False ) 
                if event.key == K_LEFT or event.key == ord('a') or event.key == K_KP4 or event.key== K_KP7:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d') or event.key == K_KP6 or event.key== K_KP1:
                    moveRight = False
                #Up and Down moves disabled
                #if event.key == K_UP or event.key == ord('w') or event.key == K_KP8 or event.key== K_KP9:
                    #moveDown = False
                    #moveUp = True
                #if event.key == K_DOWN or event.key == ord('s') or event.key == K_KP2 or event.key== K_KP3:
                    #moveUp = False
                    #moveDown = True
              # MOUSEMOTION EVENTS
            if event.type == MOUSEMOTION:
                # Follow mouse pointer
                #rectBunny.move_ip(event.pos[0] - rectBunny.centerx, event.pos[1] - rectBunny.centery)                
                rectBunny.move_ip(event.pos[0] - rectBunny.centerx, 0)
      

    def render(self,  ms):        
        global carrotsBack, carrotsSlow, carrotsQuick, moveRight, moveLeft, score, rectBunny, moveUp, moveDown
        global carrots, surface
        global gameOverSound, correctAnswerSound, musicSound
        global imageList, imageList2        
        global background, bunnyImage, bunnyImage
        global bunnyImageF, rectBunny
        global result
        global n
        global newCarrotCounter

        a= round(time.time(),0)
        if compareTime(a, self):
            return

        if self.new_operation:
            self.new_operation = False
            #print ('loopTime: '+str(a))
            self.screen().blit(background, (0,0) )
            surface = self.screen()

            #pygame.display.flip()

            # Initialize game start
            carrots = []

            rectBunny.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 250)
            moveLeft = moveRight = moveUp = moveDown = False
            #Game Cheat
            carrotsBack = carrotsSlow = carrotsQuick = False
            newCarrotCounter = 0
            #pygame.mixer.music.play(-1, 0.0)
            musicSound.play(-1)

            global number1
            global number2
            global GAMEMODE
            if(GAMEMODE==1):
                #print('n: '+str(n))
                #random.randint(max(result-4,1), min(99,result+4))
                number1 = random.randint(max(n-5,0),n) + 1
                number2 = random.randint(max(n-5,0),n)
                #result=number1+number2
                result=100
                while (result>=100):
                    number1 = random.randint(max(n-5,0),n) + 1
                    number2 = random.randint(max(n-5,0),n)
                    result=number1+number2
                    
            elif(GAMEMODE==2):
                #print('n: '+str(n))
                #random.randint(max(result-4,1), min(99,result+4))
                number1 = random.randint(max(n-15,0),n) + 1
                number2 = random.randint(max(n-15,0),n)
                z=min(number1,number2)
                number1=max(number1,number2)
                number2=z   
                while (number1==number2):
                    number1 = random.randint(max(n-15,0),n) + 1
                    number2 = random.randint(max(n-15,0),n)
                    z=min(number1,number2)
                    number1=max(number1,number2)
                    number2=z
                    result=number1-number2
                result=number1-number2
            elif(GAMEMODE==3):
                #print('n: '+str(n))
                #random.randint(max(result-4,1), min(99,result+4))
                number1 = random.randint(max(n-5,0),n+1)+1
                number2 = random.randint(max(n-5,0),n+1)+1
                while (number1>9 or number2 >9):
                    number1 = random.randint(max(n-5,0),n+1)+1
                    number2 = random.randint(max(n-5,0),n+1)+1
                    result=number1*number2    
                result=number1*number2
            elif(GAMEMODE==4):
                #print('n: '+str(n))
                #random.randint(max(result-4,1), min(99,result+4))
                number1 = random.randint(1,9)
                #number1=9
                #number2 = random.randint(max(0,n-1),n)+1
                #result=number1+result2
                result=number1
                putImagesToList()


        # Add new carrots on the screen
        if not carrotsBack and not carrotsSlow and not carrotsQuick:
            newCarrotCounter += 1
        if newCarrotCounter == CARROTVELFREC:
            newCarrotCounter = 0
        #carrotSize = random.randint(CARROTMINSIZE, CARROTMAXSIZE)  
            a=random.randint(0, 1)  
            if(a==0):
                newCarrot=Carrots(fruit1Image,result)
            else:
                newCarrot=Carrots(fruit2Image,result)
            carrots.append(newCarrot)
            
        # Moves player
        if moveLeft and rectBunny.left > 0:
            rectBunny.move_ip(-1 * BUNNYMOVEVEL, 0)
        if moveRight and rectBunny.right < WINDOWWIDTH:
            rectBunny.move_ip(BUNNYMOVEVEL, 0)
        if moveUp and rectBunny.top > 0:
            rectBunny.move_ip(0, -1 * BUNNYMOVEVEL)
        if moveDown and rectBunny.bottom < WINDOWHEIGHT:
            rectBunny.move_ip(0, BUNNYMOVEVEL)

        # Puts Bunny on the mouse pointer
        pygame.mouse.set_pos(rectBunny.centerx, rectBunny.centery)

        # Move carrots down
        for b in carrots:
            if not carrotsBack and not carrotsSlow and not carrotsQuick:
                b.rect.move_ip(0, b.velocity)
            elif carrotsBack:
                b.rect.move_ip(0, -5)
            elif carrotsSlow:
                b.rect.move_ip(0, 1)
            elif carrotsQuick:
                b.rect.move_ip(0, 5)

        # Delete carrots when you can't see it on the screen
        for b in carrots[:]:
            if b.rect.top > WINDOWHEIGHT-150:
                carrots.remove(b)

        # Draw background on game
        self.screen().blit(background, (0,0) )
        #surface.fill(BACKGROUNDCOLOR)

        # Draw enemies
        for b in carrots:                
            surface.blit(b.image, b.rect)
            drawText(str(b.number), font, b.image, 15, 25, (255,255,255))

        # Show score and maximum score
        global maxScore
        global score
        drawText(_('SCORE: %s') % (score), font, surface, 700, 0, TEXTCOLOR)
        drawText(_('MAX. SCORE: %s') % (maxScore), font, surface, 700, 60, TEXTCOLOR)

        if(GAMEMODE==1):
            #This draw the operation
            drawText(_('ADD: %d + %d') % (number1,number2), font, surface, 10, 0, TEXTCOLOR)

        elif(GAMEMODE==2):
            #This draw the operation
            drawText(_('SUBSTRACT: %d - %d') % (number1,number2), font, surface, 10, 0, TEXTCOLOR)

        elif(GAMEMODE==3):
            #This draw the operation
            drawText(_('MULTIPLY: %d x %d') % (number1,number2), font, surface, 10, 0, TEXTCOLOR)

        elif(GAMEMODE==4):
            #This draw the operation
            drawText(_('COUNT: '), font, surface, 10, 0, TEXTCOLOR)
            medC=0
            i=0
            while(i<number1):            
                #print('Iteracion: '+str(i))
                surface.blit(imageList2[i], (10+medC,60) )
                medC=medC+65
                i=i+1

        # Verify if Bunny eat carrot
        #if bunnyEatsC                    pygame.time.delay(2000)arrot(rectBunny, carrots):
        bunnyImageF.rect=rectBunny

        if bunnyEatsCarrot(bunnyImage, carrots):  
            #print ('bunnyEatsCarrot(before): MaxScore'+str(maxScore)+' score: '+str(maxScore))
            #print 'if bunnyEatsCarrot(bunnyImage, carrots): score: '+str(score)

            self.new_operation = True
            if checkResult(result):
                rectBunny.move_ip(-35, 0)
                #surface.blit(happy, rectBunny)
                surface.blit(happy, rectBunny)
                rect_ok.center = ( WINDOWWIDTH / 2, WINDOWHEIGHT / 2 )
                global rect_ok, message_ok
                surface.blit(message_ok, rect_ok)
                drawText(_("GOOD!"), font, surface, rect_ok.left + 125, rect_ok.top + 125, TEXTCOLOR)
                #drawText(_('RESPUESTA CORRECTA!'), font, surface, (WINDOWWIDTH / 3.5), (WINDOWHEIGHT / 2.25), TEXTCOLOR)
                if(GAMEMODE==3):
                    n=n+1
                    n=min(10,n)
                else:
                    n=n+2 
                    n=min(49,n)
                #print ('n cambio a :'+str(n))

                #drawText(_('PULSA UNA TECLA'), font, surface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 2.25) + 50,TEXTCOLOR)
                musicSound.stop()
                correctAnswerSound.play()
                score=returnScore()           
                if score> maxScore:
                    maxScore = score # Puts new score
                #print ('bunnyEatsCarrot(after): MaxScore'+str(maxScore)+' score: '+str(maxScore))
                pygame.display.update()
                waitPlayerPressKey(self)
            else:
                surface.blit(sad, rectBunny)
                #surface.blit(sad, rectBunny)
                score=returnScore() 
                #drawText(_('RESPUESTA INCORRECTA!'), font, surface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 2.25), TEXTCOLOR)
                #drawText(_('RESPUESTA CORRECTA: '+str(result)), font, surface, (WINDOWWIDTH / 3.8), (WINDOWHEIGHT / 2.25)+50, TEXTCOLOR)
                #drawText(_('PULSA UNA TECLA'), font, surface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 2.25) + 100, TEXTCOLOR)
                global rect_bad, message_bad
                rect_bad.center = ( WINDOWWIDTH / 2, WINDOWHEIGHT / 2 )
                rect_bad.left = rectBunny.left - 150
                if rect_bad.left < 0:
                    rect_bad.left = 0
                if rect_bad.right > WINDOWWIDTH:
                    rect_bad.right = WINDOWWIDTH
                surface.blit(message_bad, rect_bad)
                drawText(_("INCORRECT"), font, surface, rect_bad.left + 30, rect_bad.top + 70, TEXTCOLOR)                
                text = ""
                if(GAMEMODE==1):
                    #This draw the operation
                    text = _('%d+%d') % (number1,number2)
                elif(GAMEMODE==2):
                    #This draw the operation
                    text = _('%d-%d') % (number1,number2)
                elif(GAMEMODE==3):
                    #This draw the operation
                    text = _('%dx%d') % (number1,number2)
                elif(GAMEMODE==4):
                    #This draw the operation
                    text = ""
                drawText(text, font, surface, rect_bad.left + 50, rect_bad.top + 170, TEXTCOLOR)                
                drawText(str(result), font, surface, rect_bad.left + 260, rect_bad.top + 170, TEXTCOLOR)
                musicSound.stop()
                gameOverSound.play()   
                pygame.display.update()
                waitPlayerPressKey(self)
                #print ('bunnyEatsCarrot(after): MaxScore'+str(maxScore)+' score: '+str(maxScore))
        else:
            # Draw playerpygame.time.wait(2000) rectangle
            surface.blit(bunnyImage, rectBunny)
        
######################################## methods                

#Time Limit
TIMELIMIT=240.0
#TIMELIMIT=10.0
#print ('time: '+str(TIMESTART))

def compareTime(playTime, gamestate):
    global TIMELIMIT, TIMESTART
    c=playTime-TIMESTART
    #print('c time: '+str(c))
    if(c>TIMELIMIT):
        #print ('Time Limit!')
        #gamestate.set_running( False ) 
        gamestate.go_to_next_state()
        return True
    return False

#Loading Image Method
def load_image(fileName):
        try: image = pygame.image.load(fileName)
        except pygame.error:
                raise SystemExit
        image = image.convert()
        return image


#Wait Player to Press Key Method
def waitPlayerPressKey(gamestate):
    pygame.time.wait(300)
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                gamestate.set_running( False ) 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Close game if user press scape key
                    gamestate.set_running( False ) 
                return
            if event.type == MOUSEBUTTONDOWN:
                return
            if event.type == JOYBUTTONDOWN:            
                return
                
def waitPlayerPressKeyNoWait(gamestate):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.set_running( False ) 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Close game if user press scape key
                    gamestate.set_running( False ) 
                return
            if event.type == MOUSEBUTTONDOWN:
                return
            if event.type == JOYBUTTONDOWN:            
                return
            
#Bunny Eats a Carrot Method
def bunnyEatsCarrot(bunnyImage, carrots):
    global resultChosen, bunnyImageF
    for b in carrots:
        #if bunnyImageF.rect.colliderect(b.rect):py" -> Check collisions if use rect
        if pygame.sprite.collide_mask(bunnyImageF,b):
            #print ('b.number: '+str(b.number))
            resultChosen=b.number
            #print ('resultChosen: '+str(resultChosen))
            return True
    return False

a=0

def checkResult(result): 
    global resultChosen
    global score
    global a
    #print ('resultChosen: '+str(resultChosen)+ ' and result: '+str(result))
    if result==resultChosen:
        score=score+20
        #print('score: '+str(score))
        a=score
        #print ('a::::check result::: '+str(a))
        return True
    if score>0:
        score=score-5
        a=score    
        #print('score: '+str(score))
    return False


def returnScore():
    global a
    #print ('a::::::: '+str(a))
    return a
    

#Draw text on the screen
def drawText(text, font, surface, x, y, color):
    text = font.render(text, 1, color)
    rectText = text.get_rect()
    rectText.topleft = (x, y)
    surface.blit(text, rectText)

def putImagesToList():
    global imageList
    global imageList2
    i=0
    imageList2=[]
    while(i<number1):
        randomImage=imageList[random.randint(0,len(imageList)-1)]
        imageList2.append(randomImage)
        #print(imageList2[i])
        i=i+1

########################################## classes


class MBSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        self.image = image
        #Images.__init__(self)
        self.mask = pygame.mask.from_surface(self.image) # pixelmask
        #self.mask.invert()
        self.rect=image.get_rect()

class Carrots(MBSprite) :

    def __init__(self, image,result):
        carrotSize = random.randint(CARROTMINSIZE, CARROTMAXSIZE)        
        image=pygame.transform.scale(image, (carrotSize, carrotSize))
        MBSprite.__init__(self,image)
        self.rect = pygame.Rect(random.randint(0, WINDOWWIDTH-carrotSize), 0 - carrotSize, carrotSize, carrotSize)
        self.velocity = random.randint(CARROTMINVEL, CARROTMAXVEL)

        self.number =random.randint(max(result-3,1), min(99,result+3))
        #print ('fruit result: '+str(self.number))

class Cuy(MBSprite) :
    def __init__(self, image):
        self.image = image
        self.state=image
        
