#!/usr/bin/python
# -*- coding: utf-8 -*-

from pygame import *

# Screen size, by default the XO screen size resolution
screen_size = [1200, 900]
# Size of the tile
tile_size = [screen_size[0]/16, screen_size[0]/16]
# Size of the sprite (player)
sprite_size = tile_size

# Maximum speed for the player
max_speed = (screen_size[0] / 3, screen_size[1] / 8)

horizon_y = screen_size[0]/18
horizon_x = horizon_y

# Acceleration to use when changing speed
accel = (max_speed[0] / 3, max_speed[1] / 8)

# Number of tiles in the screen
num_tiles_sc = [screen_size[0] / tile_size[0], (screen_size[1] - horizon_y) / tile_size[1]]

# Friction value in y axis
friction_y = max_speed[1] / 100

# Friction value in x axis
friction_x = max_speed[0] / 1

# Minimum speed value in y axis
min_speed_y = max_speed[1] / 2 

# Minimum speed value in x axis
min_speed_x = max_speed[0] / 20 
