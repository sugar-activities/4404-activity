#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from  application import *

class ApplicationState():

    def __init__(self,  next_state = None, background_name = None, next_cookie = None):
        self._running = True
        self._screen = None
        self._next_state = next_state
        self._next_cookie = next_cookie
        self._background_name = background_name
        self._background = None
	self._cookie = None
            
    def input(self,  ms):
        pass
        
    def simulation(self,  ms):
        pass
        
    def pre_render(self,  ms):
        if self.background() is not None and self.screen() is not None :
            self.screen().blit( self.background(),  (0, 0) )

    def render(self,  ms):
        pass
        
    def post_render(self,  ms):
        pygame.display.flip()

    def set_background(self,  background_name):
        self._background_name = background
        self._background = None
        
    def background(self):
        self._background = Application.get_resource_background(self._background_name)
        return self._background

    def set_running(self,  newValue):
        self._running = newValue

    def running(self):
        return self._running

    def set_screen(self,  screen):
        self._screen = screen
        
    def screen(self):        
        return self._screen
        
    def loop(self,  ms):
        self.input(ms)
        self.simulation(ms)
        self.pre_render(ms)
        self.render(ms)
        self.post_render(ms)

    def entering_state(self,  fromStack, cookie):
	print "Entering state ", self
        self.set_running(True)
	self._cookie = cookie
        
    def exiting_state(self,  toStack):
	print "Exiting state ", self
	#self._cookie = None
        pass
        
    def go_to_next_state(self):
        Application.instance().change_state( self._next_state, self._next_cookie )

    def next_state(self):
        return self._next_state

    def cookie(self):
        return self._cookie

