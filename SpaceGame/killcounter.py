import pygame
import util
from observer import Signal

class KillCounter():
    def __init__(self):
        #signals
        self.newSprite = Signal()
        
        self.killCount = 0
        
        self.killPos = (0, 10)
        
        self.killText = pygame.sprite.GroupSingle()
        

    def init(self):
        
        pos = (0, 0)
        text = util.Text("Kills", util.HUD_FONT,  util.HUD_RED,  pos)
        self.newSprite(text)
        
        text = util.Text(str(self.killCount),  util.HUD_FONT,   util.HUD_RED, self.killPos)
        self.killText.add(text)
        self.newSprite(text)
        
    def addKill(self):
        text = self.killText.sprites()[0]
        text.kill()
        
        self.killCount += 1
        
        text = util.Text(str(self.killCount),  util.HUD_FONT,  util.HUD_RED, self.killPos)
        self.killText.add(text)
        self.newSprite(text)
        
