import pygame, highScores,pares,impares,logging,os
from highScores import *
from pygame.locals import *
h = HighScore()

class newhighscore():
	

	def __init__(self):
		newScore = 0
		global item
		item = h.loadscores()
		global scorew 
		scorew = []
		i=0		
		for i in range(len(item)):
			scorew.append(item[i][0])
		print scorew			
	def main(self,newscore):
		newenter = False		
		for score in scorew[:len(item)]:			
			if score < newscore :
				newenter = True
		if newenter == True:	
			item.append((newscore,os.getlogin()))
			h.savescores(item)
		else:
			print "nooooo"
			
	LOG_FILENAME='Esquiador.log'

	log = logging.getLogger( 'EsquiadorRun' )
	#log.setLevel( logging.DEBUG )
	if __name__=="__main__":
		logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
		main()
