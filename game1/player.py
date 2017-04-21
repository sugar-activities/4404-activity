#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# kinds of  tiles
# - navigable
# - flags: even / odd
# - obstacle
# - enemy

from pygame import *
from pygame.locals import *
from constants import *
from resources import *

class Player(sprite.Sprite):
    
    def __init__(self, game_mode):
        sprite.Sprite.__init__(self)
        self.pos_wc = [screen_size[0] / 2, 0]
        self.speed = [0, min_speed_y]
        self.image = player_image_normal
        self.image_ticks = 0
        self.rect_sc = self.image.get_rect()
        self.rect_sc.topleft = [self.pos_wc[0], horizon_y]
        self.score = 0
        self.game_mode = game_mode
        self.num_ok = 0
        self.num_error = 0
                    
    def update(self, milliseconds):
        self.speed[1] -= friction_y
        if (self.speed[1] < min_speed_y):
            self.speed[1] = min_speed_y
        self.pos_wc[0] += self.speed[0] * (milliseconds / 1000.0)
        self.pos_wc[1] += self.speed[1] * (milliseconds / 1000.0)
        if self.pos_wc[0] < 0:
            self.pos_wc[0] = 0
        elif self.pos_wc[0] > screen_size[0] - sprite_size[0]:
            self.pos_wc[0] = screen_size[0] - sprite_size[0]
        self.rect_sc.topleft = [self.pos_wc[0], horizon_y]

    def moveLeft(self):
        self.speed[0] -= accel[0]
        self.speed[0] = min(self.speed[0], max_speed[0]) 

    def moveRight(self):
        self.speed[0] += accel[0]
        self.speed[0] = min(self.speed[0], max_speed[0])

    def moveForward(self):
        self.speed[1] += accel[1]
        self.speed[1] = min(self.speed[1], max_speed[1])
        
    def moveBack(self):
        self.speed[1] -= accel[1]
        self.speed[1] = min(-self.speed[1], -max_speed[1])

    def getPos(self):
        return self.pos_wc
    
    def getOffsetY(self):
        return self.pos_wc[1] 
    
    def getRectWC(self):
        return Rect(self.pos_wc, sprite_size)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect_sc)

    def checkCollision(self, track):

        rect_wc = self.getRectWC()

        collisionTile = track.collidesWith(rect_wc)
        if track.isNotNavigable(collisionTile) :
            """ frena mas """
            self.speed[1] = 0
            self.speed[0] = 0
            self.image = player_image_impact
            self.image_ticks = 25
            #sound_collide.play()
        elif track.isDanger(collisionTile) :
            self.speed[1] = 0
            self.speed[0] = 0
            self.score -= 10
            self.image = player_image_impact_hard
            self.image_ticks = 25
            sound_danger.play()
        elif track.isNavigable(collisionTile) :
            if (self.image_ticks > 0):
                self.image_ticks -= 1
            else:
                self.image = player_image_normal
        elif type(collisionTile) == int:
            num = collisionTile
            if(self.game_mode =='impares'):
                if (num % 2) == 1 :
                    self.score += 20
                    self.image = player_image_happy
                    self.image_ticks = 15
                    self.num_ok = self.num_ok + 1
                    sound_good_choice.play()
                else:
                    self.score -= 5
                    self.image = player_image_sad
                    self.image_ticks = 25
                    self.num_error = self.num_error + 1
                    sound_bad_choice.play()
            elif self.game_mode =='pares':
                if (num % 2) == 0 :
                    self.score += 20
                    self.image = player_image_happy
                    self.image_ticks = 15
                    self.num_ok = self.num_ok + 1
                    sound_good_choice.play()
                else:
                    self.score -= 5
                    self.image = player_image_sad          
                    self.image_ticks = 15
                    self.num_error = self.num_error + 1
                    sound_bad_choice.play()

        if self.score <=0:
            self.score=0

    def number_of_errors(self):
        self.num_error
        
    def number_of_correct(self):
        self.num_ok      
        
    def game_over_message(self, track):
        if self.game_mode == "pares":
            total_ok = track.num_odd
            total_error = track.num_even
        elif self.game_mode == "impares":            
            total_ok = track.num_odd
            total_error = track_error
            
            
            