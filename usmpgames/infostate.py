#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import jmenu
import sys
import txtlib
from applicationstate import *
from application import *
from ktextsurfacewriter import KTextSurfaceWriter
from pygame.locals import *
import pygame.font

class InfoState(ApplicationState):
    
    def __init__(self, next_state,  background = None, next_cookie = None):
        ApplicationState.__init__(self,  next_state,  background, next_cookie)
        self._images = []
        self._ktexts = []
        
    def clear_all(self):
        self._images = []
        self._ktexts = []
 
    def add_text(self,  text,  color,  pos,  rectsize,  fontsize,  font = None):
        textobj = txtlib.Text(rectsize, font,  fontsize,  text)
        textobj.background_color = (255, 255,  255,  0)
        textobj.update()
        self.add_image( textobj.area,  pos )
 
    def add_htmltext(self,  html_text,  color,  pos,  rectsize,  fontsize,  font = None):
        textobj = txtlib.Text(rectsize, font,  fontsize)
        textobj.background_color = (255, 255,  255,  0)
        textobj.html(html_text)
        textobj.update()
        self.add_image( textobj.area,  pos )

    def add_text2(self,  text,  color,  pos,  rectsize, font = None):
        text_rect = pygame.Rect( pos, rectsize )
        fillcolor = (231,178,66,0)
        textobj = KTextSurfaceWriter(text_rect, font, color, fillcolor)
        textobj.text = (text)
        textobj.invalidate()
        self._ktexts.append(textobj)

    def add_image(self,  surface,  pos):
        info = {}
        info["surface"] = surface
        info["pos"] = pos
        self._images.append(info)

    def input(self,  ms):
        events = pygame.event.get()
        if events:
            for event in events:
                if event.type == pygame.QUIT:
                    self.set_running( False )
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.set_running( False )
                    else:
                        self.go_to_next_state()

    def render(self,  ms):
        for info in self._images:
            self.screen().blit(info["surface"],  info["pos"])
        for info in self._ktexts:
            info.draw(self.screen())            

    def entering_state(self, fromStack, cookie):
        ApplicationState.entering_state(self, fromStack, cookie)	
	pygame.time.wait(500)
	pygame.event.clear()
