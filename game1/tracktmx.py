#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

There are 4 types of tiles:

1) Navigable materials (lowercase letter) like grass, dirt
2) Non-navigable materials (uppercase letter) like Water, Plant, Rock, Tree, trunK
3) Dangerous materials (numbers) like black cuy (2) and owl (1)
4) Goals (symbols) like apples (#), oranges ($)

"""

import sys
import random
import pygame
import glob
import os.path
from pygame import *
from pygame.locals import *
from constants import *
from resources import *
from tiledtmxloader import *

class Track():
    
    def __init__(self):
        self.numbers_image = {}
        self.numbers_number = {}
        self.touched = {}
        self.load()
        self.num_odd = 0
        self.num_even = 0
        self.cached_surface = None
        self.cached_offset = 0
        self.cached_height = 0

    def load(self, filename = "./tracks/track1.tmx"):
        self.world_map = TileMapParser().parse_decode(filename)
        self.world_map.load(ImageLoaderPygame())
        assert self.world_map.orientation == "orthogonal"

    def endOfTrack(self, offset = 0):
        return (offset + 200 >= self.world_map.height * self.world_map.tileheight)

    def drawFast(self, screen, offset = 0):
        if self.cached_surface is None:
            self.cached_surface = pygame.Surface(screen_size)
            self.cached_offset = 0
            self.cached_height = 0
        else:
            # scroll offset difference      
            # self.cached_surface.scroll(0, -int(offset - self.cached_offset))
	    yoff = int(offset - self.cached_offset)
	    area = pygame.Rect(0, yoff, self.cached_surface.get_width(), self.cached_surface.get_height() - yoff )
	    self.cached_surface.blit(self.cached_surface, (0, 0), area)
            self.cached_height -= int(offset - self.cached_offset)
            if self.cached_height < 0:
                self.cached_height = 0
                
        # draw new tiles
        height = screen_size[1] - self.cached_height
        #print "offset = ", offset + self.cached_height, "height=", height, "horizon_y=", self.cached_height
        self.draw(self.cached_surface, offset + self.cached_height, height, self.cached_height)
        self.cached_offset = offset
        self.cached_height = screen_size[1]
        
        # draw whole thing to screen
        screen.blit(self.cached_surface, (0,0))

    def draw(self,  screen,  offset = 0, height = 0, horizon_y = 0): 
        # cam_offset is for scrolling
        cam_offset_x = 0
        cam_offset_y = offset
        screen_width = screen_size[0]
        if height == 0:
            screen_height = screen_size[1]
        else:
            screen_height = height
        #horizon_y = 0
        # draw the map
        for layer in self.world_map.layers[:]:
            if layer.visible:
                idx = 0
                numtilex = 0
                num = 0
                # loop over all tiles
                starty = int ( offset / self.world_map.tileheight )
                numtilesy = int (height + self.world_map.tileheight - 1) / self.world_map.tileheight
                #print "starty = ", starty, "numtilesy= ", numtilesy                
                
                totalrect_sc = pygame.Rect((0, horizon_y), (screen_width, height))
                
                #for ypos in xrange(0, layer.height):
                for ypos in xrange(starty, starty + numtilesy):
                    for xpos in xrange(0, layer.width):
                        # add offset in number of tiles
                        x = (xpos + layer.x) * self.world_map.tilewidth
                        y = (ypos + layer.y) * self.world_map.tileheight
                        # get the gid at this position
                        ypos_safe = ypos
                        if ypos_safe >= layer.height:
                            ypos_safe = layer.height - 1
                        img_idx = layer.content2D[xpos][ypos_safe]
                        material = self.world_map.indexed_tiles_tileset[img_idx]
                        idx += 1
                        if img_idx:
                            
                            # get the actual image and its offset
                            offx, offy, screen_img = self.world_map.indexed_tiles[img_idx]
                            tile_sc = pygame.Rect((x - cam_offset_x + offx, y - cam_offset_y + horizon_y + offy), (self.world_map.tilewidth, self.world_map.tileheight))
                            # only draw the tiles that are relly visible (speed up)
                            #print "y=", y - cam_offset_y + horizon_y + offy, "miny=", horizon_y, "maxy", horizon_y + screen_height
                            if totalrect_sc.colliderect(tile_sc):
                            #if x >= cam_offset_x - 3 * self.world_map.tilewidth and x + cam_offset_x <= screen_width + self.world_map.tilewidth\
                            #   and y >= cam_offset_y - 3 * self.world_map.tileheight and y + cam_offset_y <= screen_height + 3 * self.world_map.tileheight:
                                """
                                if screen_img.get_alpha():
                                    screen_img = screen_img.convert_alpha()
                                else:
                                    screen_img = screen_img.convert()
                                    if layer.opacity > -1:
                                        #print 'per surf alpha', layer.opacity
                                        screen_img.set_alpha(None)
                                        alpha_value = int(255. * float(layer.opacity))
                                        screen_img.set_alpha(alpha_value)
                                screen_img = screen_img.convert_alpha()
                                """
                                # draw image at right position using its offset
                                screen.blit(screen_img, (x - cam_offset_x + offx, y - cam_offset_y + offy + horizon_y))
                                #num = num + 1
                                if material == "goals":
                                    surface = self.getTextSurface(xpos, ypos_safe, img_idx)
                                    screen.blit(surface, (x - cam_offset_x + offx + 10, y - cam_offset_y + offy + horizon_y + 10))
                                    
        """
        # map objects
        for obj_group in world_map.object_groups:
            goffx = obj_group.x
            goffy = obj_group.y
            if goffx >= cam_offset_x - 3 * world_map.tilewidth and goffx + cam_offset_x <= screen_width + world_map.tilewidth \
               and goffy >= cam_offset_y - 3 * world_map.tileheight and goffy + cam_offset_y <= screen_height + 3 * world_map.tileheight:
                for map_obj in obj_group.objects:
                    size = (map_obj.width, map_obj.height)
                    if map_obj.image_source:
                        surf = pygame.image.load(map_obj.image_source)
                        surf = pygame.transform.scale(surf, size)
                        screen.blit(surf, (goffx + map_obj.x + cam_offset_x, goffy + map_obj.y + cam_offset_y))
                    else:
                        r = pygame.Rect((goffx + map_obj.x + cam_offset_x, goffy + map_obj.y + cam_offset_y), size)
                        pygame.draw.rect(screen, (255, 255, 0), r, 1)
        """

    def getTextSurface(self, xtile, ytile, object):
        if self.numbers_image.has_key( (xtile, ytile) ):
            return self.numbers_image[(xtile, ytile)]
        #if (object % 2) == 1:        
        #    number = random.randint(0,49) * 2 + 1
        #    self.num_odd = self.num_odd + 1
        #elif  (object % 2) == 0:
        #    number = random.randint(0,49) * 2
        #    self.num_even = self.num_even + 1

        number = random.randint(0,99) 
	if (number % 2) == 1:
            self.num_odd = self.num_odd + 1
	else:
            self.num_even = self.num_even + 1

        afont = pygame.font.SysFont("droidsans", 44)
        text = afont.render(str(number), 1, (255,255,255))
	self.numbers_number[(xtile, ytile)] = number
	self.numbers_image[(xtile, ytile)] = text
        return text
   
    def getTileNumberWC(self, x_wc, y_wc):
        return [x_wc / tile_size[0], y_wc / tile_size[1]]
   
    def getTileRectWC(self, x_wc, y_wc):
        tile_rect = Rect()
        tile_rect.top = y_wc / tile_size[1]
        tile_rect.left = x_wc / tile_size[0]
        tile_rect.width = tile_size[0]
        tile_rect.height = tile_size[1]
   
    def getTileType(self, tilex, tiley):
        return self.lines[tiley][tilex]
   
    def collidesWith(self, rect, justCheck = False):
        """ check collision """
        xtilemin, ytilemin = self.getTileNumberWC(rect.left, rect.top)
        xtilemax, ytilemax = self.getTileNumberWC(rect.right, rect.bottom)
        retmaterial = "navegable"
        for layer in self.world_map.layers[:]:
            for tiley in range(ytilemin, ytilemax + 1):
                for tilex in range(xtilemin, xtilemax + 1):
                    if tilex < 0 :
                        tilex = 0
                    if tilex >= self.world_map.width :
                        tilex = self.world_map.width - 1
                    if tiley < 0 :
                        tiley = 0
                    if tiley >= self.world_map.height :
                        tiley = self.world_map.height - 1
                    img_idx = layer.content2D[tilex][tiley]
                    material = self.world_map.indexed_tiles_tileset[img_idx]
                    if self.isGoal(material):
                        if not self.touched.has_key ( (tilex, tiley) ):
                            if not justCheck:
                                self.touched[ (tilex,tiley) ] = True
                            return self.numbers_number[(tilex, tiley)]
                    if self.isDanger(material):
                        if not self.touched.has_key ( (tilex, tiley) ):
                            if not justCheck:
                                self.touched[ (tilex,tiley) ] = True
                            return material                      
                    if self.isNotNavigable(material):
                        retmaterial = material
        return retmaterial 

    def isNavigable(self, tile):
        return tile == "navegable"

    def isNotNavigable(self, tile):
        return tile == "nonavegable"

    def isDanger(self, tile):
        return tile == "enemies"

    def isGoal(self, tile):
        return tile == "goals"

    def number_of_odd(self):
        return self.num_odd
        
    def number_of_even(self):
        return self.num_even        
        
