#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import usmpgames
import olpcgames
import game1
import game2
import constants
from gettext import gettext as _

# \xe1 á \xe9 é \xed í \xf3 ó \xfa ú \xc1 Á \xc9 É \xcd Í \xd3 Ó \xda Ú 

class MathQuwy(usmpgames.Application):
    
    def initialize(self):
        usmpgames.Application.initialize(self)
        size = constants.screen_size
        if olpcgames.ACTIVITY:
            size = olpcgames.ACTIVITY.game_size
        self.set_screen( pygame.display.set_mode( size )) 
        pygame.mouse.set_visible(False)

        # even numbers congratulations message
        background_congrats = "data/backgrounds/congrats.jpg"
        congrats = usmpgames.InfoState( None,  background_congrats )

        # even numbers game
        #even_numbers_game = game1.collectgame.CollectGame( "pares",  congrats )
        #odd_numbers_game = game1.collectgame.CollectGame( "impares",  congrats )
        evenodd_game = game1.collectgame.CollectGame( "",  congrats )

        # even numbers game state (tutorial)
        background_tutorial = "data/backgrounds/tutorial.jpg"
        even_numbers_tutorial = usmpgames.InfoState( evenodd_game,  background_tutorial, "pares" )
	even_numbers_tutorial.add_text2(
            _("""Even Numbers Instructions\n\n\nAdd points picking the fruits\nwith  even numbers.\n\nAvoid touching the fruits with odd numbers or your points will be deducted.\n\nMove Quwy with arrow keys. Try to avoid water and other animals on the map too.\n\nPress any key to continue."""),
            color = (0, 0, 0, 0), 
            pos = (660, 260), 
            rectsize = (380, 390));
            
        # odd numbers game state (tutorial)
        odd_numbers_tutorial = usmpgames.InfoState( evenodd_game,  background_tutorial, "impares" )
        odd_numbers_tutorial.add_text2(
            _(""" Odd Numbers Instructions\n\n\nAdd points picking the fruits\nwith  odd numbers.\n\nAvoid touching the fruits with even numbers or your points will be deducted.\n\nMove Quwy with arrow keys. Try to avoid water and other animals on the map too.\n\nPress any key to continue."""),
            color = (0, 0, 0, 0), 
            pos = (660, 260), 
            rectsize = (380, 390));
              
        # add game
        #add_game = game2.Game2( 1, congrats )
        #substract_game = game2.Game2( 2, congrats )
        #multiply_game = game2.Game2( 3, congrats )
        #count_game = game2.Game2( 4, congrats )
        allgame2 = game2.Game2( 0, congrats )
        
        # add numbers game state (tutorial)
        add_tutorial = usmpgames.InfoState( allgame2,  background_tutorial, 1 )
        add_tutorial.add_text2(
            _(""" Add Game Instructions\n\n\nCalcute the add result.\n\nAdd points picking the fruits\nwith the correct answer of the operation.\n\nTry to avoid the fruits with\nincorrect answers or your points will be deducted.\n\nMove Quwy with the left and right arrow keys.\n\nPress any key to continue."""),
            color = (0, 0, 0, 0), 
            pos = (660, 260), 
            rectsize = (380, 390));

        # substract numbers game state (tutorial)
        substract_tutorial = usmpgames.InfoState( allgame2,  background_tutorial, 2 )
        substract_tutorial.add_text2(
            _(""" Substract Game Instructions\n\n\nCalcute the substract result.\n\nAdd points picking the fruits\nwith the correct answer of the operation.\n\nTry to avoid the fruits with\nincorrect answers or your points will be deducted.\n\nMove Quwy with the left and right arrow keys.\n\nPress any key to continue."""),
            color = (0, 0, 0, 0), 
            pos = (660, 260), 
            rectsize = (380, 390));

        # multiply numbers game state (tutorial)
        multiply_tutorial = usmpgames.InfoState( allgame2, background_tutorial, 3 )
        multiply_tutorial.add_text2(
            _(""" Multiply Game Instructions\n\n\nCalcute the multiply result.\n\nAdd points picking the fruits\nwith the correct answer of the operation.\n\nTry to avoid the fruits with\nincorrect answers or your points will be deducted.\n\nMove Quwy with the left and right arrow keys.\n\nPress any key to continue."""),
            color = (0, 0, 0, 0), 
            pos = (660, 260), 
            rectsize = (380, 390));

        # count game state (tutorial)
        count_tutorial = usmpgames.InfoState( allgame2,  background_tutorial, 4 )
        count_tutorial.add_text2(
            _(""" Count Game Instructions\n\n\nCalcute the count result.\n\nAdd points picking the fruits\nwith the correct answer of the operation.\n\nTry to avoid the fruits with\nincorrect answers or your points will be deducted.\n\nMove Quwy with the left and right arrow keys.\n\nPress any key to continue."""),
             color = (0, 0, 0, 0), 
            pos = (660, 260), 
            rectsize = (380, 390));

        # credits
        credits = usmpgames.InfoState( None, background_tutorial )
        credits.add_text2(
            _("""Credits\n\nProgramming:\n\nMateu Batle Sastre\nRicardo Flores S\xe1nchez\n\nTaller de Investigaci\xf3n Aplicada - Escuela Profesional de Ingenier\xeda\nde Computaci\xf3n y Sistemas\n\nDesign:\n\nGrafimedia - FIA-DATA\n\nUniversidad de San Mart\xedn de Porres"""),
            color = (0, 0, 0, 0), 
            pos = (660, 260), 
            rectsize = (380, 390));

        # menu state
        background_menu = "data/backgrounds/menu.jpg"
        main_menu = usmpgames.MenuState( background_menu )
        main_menu.add_menu_option(_("Even Numbers"),  even_numbers_tutorial )
        main_menu.add_menu_option(_("Odd Numbers"),  odd_numbers_tutorial )
        main_menu.add_menu_option(_("Add Game"),  add_tutorial )
        main_menu.add_menu_option(_("Substract Game"),  substract_tutorial )
        main_menu.add_menu_option(_("Multiply Game"),  multiply_tutorial )
        main_menu.add_menu_option(_("Count Game"),  count_tutorial )
        main_menu.add_menu_option(_("Credits"),  credits )
        main_menu.add_menu_option(_("Exit Game"),  None )
        main_menu.pos = (685, 300)
        
	fonttitle = pygame.font.Font(None, 50)
        main_menu.add_text2(
            _("""               Quwy\n           Math Cuy"""),
            color = (255, 25, 34, 0), 
            pos = (700, 190), 
            rectsize = (380, 390),
	    font = fonttitle);
        
        self.push_state( main_menu )
 
    def shutdown(self):
        pass

# game application
def main():
    game = MathQuwy()
    game.runLoop()

if __name__ == "__main__":
    main()
