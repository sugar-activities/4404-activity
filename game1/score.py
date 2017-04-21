#Actividad Esquiador
#Archivo: score.py
#Descripcion: Clase que maneja el puntaje del juego
#

import pygame
from pygame import *
from pygame.locals import *
from constants import *
from gettext import gettext as _
#fuente = pygame.font.Font("./media/fuentes/space age.ttf", 25)

class Score():
    
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont(None, 80)
    
    def draw(self, screen):
        score = _("SCORE: %05d") % self.player.score
        surface = self.font.render(score, 1, (0,0,0))
        rect = surface.get_rect()
        screen.blit(surface, rect)

