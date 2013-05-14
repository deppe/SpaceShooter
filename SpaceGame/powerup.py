import util
import random
import pygame
from bouncyobject import GenericBouncyObject
from observer import Signal

class Powerup(GenericBouncyObject):
    def __init__(self, side, vector, type):
        GenericBouncyObject.__init__(self, side, vector, "powerup.png")
                               
        self.type = self.getRandomPowerup()
        
        self.life = 500
        
    def update(self):
        GenericBouncyObject.update(self)
        
        self.life -= 1
        
        if self.life == 0:
            self.kill()
            
    def getRandomPowerup(self):
        powerup = [util.POWERUP_MULTISHOT, 
                         util.POWERUP_BIGSHOT, 
                         util.POWERUP_BUTTBOMB][random.randint(0,  2)]

        return powerup

class PowerupDash():
    def __init__(self):
                
        #signals
        self.newSprite = Signal()
        self.currentPowerup = None
        
        self.text = pygame.sprite.GroupSingle()
        
    def init(self,):
        
        x, y = pygame.display.get_surface().get_rect().topright
        x = x - 100
        
        self.text = util.Text("",  util.HUD_FONT,   util.HUD_RED, (x, y))
        self.newSprite(self.text)
        
    def changePowerup(self,  text):
        self.text.changeText(text)
