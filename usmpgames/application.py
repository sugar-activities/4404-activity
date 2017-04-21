#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame
import olpcgames
import constants

class Application():

    _instance = None
    _resources = {}

    @staticmethod
    def instance():
        return Application._instance

    @staticmethod
    def get_resource_background(name):
        if name is None:
            return None
        if not Application._resources.has_key(name) :
            size = constants.screen_size
            if olpcgames.ACTIVITY:
                size = olpcgames.ACTIVITY.game_size
            Application._resources[name] = pygame.transform.scale( pygame.image.load(name), size)
        return Application._resources[name]

    def __init__(self):
        self._state_stack = []
        self._cookie_stack = []
        self._current_state = None
        self._current_cookie = None
        self._running = True
        self._fps = 25
        if Application._instance is None:
            Application._instance = self
            
    def set_screen(self,  screen):
        self._screen = screen
        
    def screen(self):
        return self._screen
            
    def push_state(self,  new_state, new_cookie = None):
        # exit from current state
        if self._current_state is not None:
                self._current_state.exiting_state( True )
                if new_state is not None:
                    self._state_stack.append(self._current_state)
                    self._cookie_stack.append(self._current_state.cookie())
        
        # process new state
        fromStack = False
        if new_state is None:
            if len(self._state_stack) == 0 :
                self.set_running( False )
                return
            else :
                self._current_state = self.pop_state()
                self._current_cookie = self._current_state.cookie()
                fromStack = True
        else:
            self._current_state = new_state
            self._current_cookie = new_cookie

        # entering new state    
        if self._current_state is None:
            self.set_running(False)
        else:
            self._current_state.set_screen(self.screen())
            self._current_state.entering_state(fromStack, self._current_cookie)
    
    def change_state(self,  new_state, new_cookie):
        # exit from current state
        if self._current_state is not None:        
            self._current_state.exiting_state(False)
            
        # process current state
        if new_state is None:
            if len(self._state_stack) == 0 :
                self.set_running( False )
                return
            else :
                self.pop_state()
		return
        else:
            self._current_state = new_state
            self._current_cookie = new_cookie
        
        # entering new state
        if self._current_state is not None:        
            self._current_state.set_screen(self.screen())
            self._current_state.entering_state( False, self._current_cookie )
        else:
            self.set_running(False)
            
        # entering new state    
        
    def pop_state(self):
        if self._current_state is not None:        
            self._current_state.exiting_state( False )
        if len(self._state_stack) >= 1:
            self._current_state = self._state_stack.pop()
            self._current_cookie = self._current_state.cookie()
        else:
            self._current_state = None
            self._current_cookie = None
        if self._current_state is not None:
            self._current_state.set_screen(self.screen())
            self._current_state.entering_state( True, self._current_cookie )

    def current_state(self):
        return self._current_state
        
    def running(self):
        if not self._running:
           return False
        if self.current_state() is None:
            return False
        state_running = self.current_state().running()
        if not state_running:
            self.pop_state()
            return self.running()
        return True
        
    def set_running(self,  new_value):
        self._running = new_value
        
    def set_fps(self,  new_value):
        self._fps = new_value
        
    def fps(self):
        return self._fps

    def initialize(self):
        pygame.init()
        
    def shutdown(self):
        pygame.quit()
        
    def runLoop(self):
        self.initialize()
        clock = pygame.time.Clock()
        while self.running() :
            ms = clock.tick( self.fps() )
            #try:
            self.current_state().loop(ms)
            #except:
            #    print "Unexpected error:", sys.exc_info()[0]
        self.shutdown()
