import pygame
import util
from observer import Signal
from pygame.locals import *

class GameStartState:
    def __init__(self, screen,  background):
        
        #signals
        self.endState = Signal()
        
        self.screen = screen
        self.background = background
        
        msg = "Press enter to start game"
        font = pygame.font.Font("freesansbold.ttf",40)
        color = (50,50,50)
        pos = (self.background.get_rect().midleft)
        text = util.Text(msg, font,  color,  pos)
        
        self.allsprites =  pygame.sprite.RenderUpdates()
        self.allsprites.add(text)
                        
    def handleEvent(self,  input):
        if input.isactive(K_RETURN):
            self.endState()
        
    def update(self):
        self.allsprites.update()
        self.allsprites.clear(self.screen, self.background)
        changes = self.allsprites.draw(self.screen)
        pygame.display.update(changes)
        
    def killAllSprites(self):
        for sprite in self.allsprites.sprites():
            sprite.kill()
