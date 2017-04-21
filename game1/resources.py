#!/usr/bin/python
# -*- coding: utf-8 -*-

from pygame import *
from constants import *

# Images used for the player
player_image_normal = transform.scale( image.load("data/quwy.png"), sprite_size)
player_image_happy  = transform.scale( image.load("data/quwy_happy.png"), sprite_size)
player_image_sad    = transform.scale( image.load("data/quwy_sad.png"), sprite_size)
player_image_impact = transform.scale( image.load("data/quwy_impact.png"), sprite_size)
player_image_impact_hard = transform.scale( image.load("data/quwy_impact_hard.png"), sprite_size)

# Sounds
music_background = None
sound_good_choice = mixer.Sound('./data/sounds/yujui_short.ogg')
sound_bad_choice = mixer.Sound('./data/sounds/oops.ogg')
sound_danger = mixer.Sound('./data/sounds/ohoo.ogg')
sound_collide = mixer.Sound('./media/sounds/gameover.wav')
#music_background = mixer.Sound('./media/sounds/menumusic.ogg')
#sound_good_choice = mixer.Sound('./media/sounds/aplause.ogg')
#sound_bad_choice = mixer.Sound('./media/sounds/gameover.wav')
#sound_danger = mixer.Sound('./media/sounds/gameover.wav')
#sound_collide = mixer.Sound('./media/sounds/gameover.wav')
sound_game_over = mixer.Sound('./media/sounds/gameover.wav')
