# -*- coding: utf-8 -*-

import pygame, jmenu, sys
from applicationstate import *
from application import *
from infostate import *

class MenuState(InfoState):
    
    def __init__(self, background = None, cookie = None):
        InfoState.__init__(self,  None,  background, cookie)
        self._menu_options = []
        self._menu_states = []
        self.pos = ('center', 'center')
        self.font = None
        self.light = 10
        self.fontSize = 32
        self.color = (0, 0, 0)
        self.justify = True
        
    def add_menu_option(self,  option,  state):
        self._menu_options.append( option )
        self._menu_states.append( state )

    def render(self,  ms):
	InfoState.render(self, ms)
        selection = jmenu.run(
            self._menu_options,
            color = self.color, 
            size = self.fontSize, 
            font = self.font,
            light = self.light,
            justify = self.justify,
            pos = self.pos)
        try:
            index = self._menu_options.index( selection )
            Application.instance().push_state( self._menu_states[index] )
        except:
            Application.instance().pop_state()

    def input(self,  ms):
	pass

    def entering_state(self, fromStack, cookie):
	ApplicationState.entering_state(self, fromStack, cookie)	
