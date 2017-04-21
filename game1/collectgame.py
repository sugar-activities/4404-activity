#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import pygame
import usmpgames
from player import *
from tracktmx import *
from score import *
from resources import *
from gettext import gettext as _

class CollectGame(usmpgames.ApplicationState):

    def __init__(self,  game_mode,  next_state = None,  background = None, next_cookie = None):
        usmpgames.ApplicationState.__init__(self,  next_state,  background, next_cookie)
        self.game_mode = game_mode
        self.font = pygame.font.SysFont(None, 80)

    def entering_state(self, fromStack, cookie):
        usmpgames.ApplicationState.entering_state(self, fromStack, cookie)
        self.game_mode = cookie
        if (not fromStack) :
            self.track = Track()
            self.player = Player(self.game_mode)
            self.score = Score(self.player)
            #music_background.play(-1)

    def exiting_state(self, fromStack):
        #music_background.stop()
        self.next_state().clear_all()
        total = self.track.num_odd + self.track.num_even
        self.next_state().add_text2(
            _(""" %s\n\nYou have %d points.\n\nCorrect answers: %d time(s).\n\nBad answers: %d time(s).""") % 
            (self.game_over_message(), self.player.score, self.player.num_ok, self.player.num_error),
            color = (0, 0, 0, 0),
            pos = (660, 260),
            rectsize = (380, 390));
        usmpgames.ApplicationState.exiting_state(self, fromStack)
        
    def input(self,  ms):
        events = pygame.event.get()
        # Now the main event-processing loop
        if events:
            for event in events:
                if event.type == pygame.QUIT:
                    self.set_running( False ) 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.set_running( False ) 
                    elif event.key == pygame.K_LEFT or event.key == ord('a') or event.key == K_KP4 or event.key== K_KP7:
                        self.player.moveLeft()
                    elif event.key == pygame.K_RIGHT or event.key == ord('d') or event.key == K_KP6 or event.key== K_KP1:
                        self.player.moveRight()
                    elif event.key == pygame.K_DOWN  or event.key == ord('s') or event.key == K_KP2 or event.key== K_KP3:
                        self.player.moveForward()
                    elif event.key == pygame.K_UP or event.key == ord('w') or event.key == K_KP8 or event.key== K_KP9:
                        self.player.moveBack()
        
    def simulation(self,  ms):
        self.player.update(ms)
        offsety = self.player.getOffsetY()
        if self.track.endOfTrack(offsety) :
            self.go_to_next_state()
        self.player.checkCollision(self.track)
        
    def pre_render(self,  ms):
        self.screen().fill( (110,183,251))
        usmpgames.ApplicationState.pre_render(self, ms)

    def render(self,  ms):
        offsety = self.player.getOffsetY()
        if not self.track.endOfTrack(offsety) :
            self.track.drawFast(self.screen(), offsety)
            self.player.draw(self.screen())
        self.score.draw(self.screen())
	if self.game_mode == "pares":
            self.drawText("EVEN NUMBERS", screen_size[0] / 2, 0, (0,0,0))
	else:
            self.drawText("ODD NUMBERS", screen_size[0] / 2, 0, (0,0,0))

    def drawText(self, text, x, y, color):
        text = self.font.render(text, 1, color)
        rectText = text.get_rect()
        rectText.topleft = (x, y)
        self.screen().blit(text, rectText)

    def game_over_message(self):
        if self.game_mode == "pares":
            total_ok = self.track.num_odd
            total_error = self.track.num_even
        elif self.game_mode == "impares":            
            total_ok = self.track.num_odd
            total_error = self.track.num_even
        percent_ok_taken = self.player.num_ok * 100 / total_ok
        percent_error_taken = self.player.num_error * 100 / total_error
		
        if percent_error_taken >= percent_ok_taken:
            if self.game_mode == "pares":
                return _("You should pay more attention.\n\nYou picked more odd numbers instead even numbers.")
            else:                
                return _("You should pay more attention.\n\nYou picked more even numbers instead odd numbers.")
        else:
            if percent_ok_taken >= 75:
                if self.game_mode == "pares":
                    return _("Great!\n\nYou almost picked all the odd numbers.")
                else:
                    return _("Great!\n\nYou almost picked all the odd numbers.")
            elif percent_ok_taken >= 50:
                if self.game_mode == "pares":
                    return _("Very good.\n\nYou picked many even numbers.\n\nBut you can do it better!")
                else:
                    return _("Very good.\n\nYou picked many even numbers.\n\nBut you can do it better!")
            else:
                if self.game_mode == "pares":
                    return _("It's okay.\n\nKeep practicing and you will do it better.\n\nDo it againt!")
                else:
                    return _("It's okay.\n\nKeep practicing and you will do it better.\n\nDo it again!")
