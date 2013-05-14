import sys
import random
import math
import getopt
import pygame
from socket import *
from pygame.locals import *
from input import Input
from ship import Ship
from observer import Signal
from spaceactionstate import SpaceActionState
from gamestartstate import GameStartState
import util


class Game():
    def __init__(self):
        
        self.SPACE_ACTION_STATE = "space_action_state"
        self.GAME_START_STATE = "game_start_state"
        
        self.screen = pygame.display.set_mode((640, 480))
        
        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        
        # Blit everything to the screen
        self.resetBackground()
        
        self.initGameState(self.GAME_START_STATE)
        
        # Initialise clock
        self.clock = pygame.time.Clock()
    
    def start(self):
        # Event loop
        input = Input()
        while True:
            # Make sure game doesn't run at more than 60 frames per second
            self.clock.tick(40)
            pygame.time.wait(5)
    
            input.add_events(pygame.event.get())
            
            if input.isset(QUIT):
                return
                
            self.gameState.handleEvent(input)
            self.gameState.update()
        
    def resetBackground(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        
    def onEndState(self):
        self.gameState.killAllSprites()
        self.resetBackground()
        self.initGameState(self.SPACE_ACTION_STATE)
    
    def initGameState(self,  state):
        if state == self.SPACE_ACTION_STATE:
            self.gameState = SpaceActionState(self.screen,  self.background)
        elif state == self.GAME_START_STATE:
            self.gameState = GameStartState(self.screen,  self.background)
            
        self.gameState.endState.connect(self.onEndState)
        
def main():
    # Initialise screen
    pygame.mixer.pre_init(44100,-16,2, 1024)
    
    pygame.init()
    
    pygame.mixer.init()
    
    #this is dumb but i'm too lazy to fix it
    util.HUD_FONT = pygame.font.Font("freesansbold.ttf",12)
    
    pygame.display.set_caption('Space Adventure!!!!')
    
    game = Game()
    game.start()

    #explosionSound = util.load_sound('explosion.wav')


main()
pygame.quit ()
