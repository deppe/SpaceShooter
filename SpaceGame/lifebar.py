import pygame
import util

from observer import Signal

class Lifebar():
    def __init__(self,  life):
        
        #signals
        self.newSprite = Signal()
        self.life = life
        self.hearts = []
        
        self.topleft = pygame.display.get_surface().get_rect().topleft

    def init(self,):
        
        startx = 130
        text = util.Text("Life", util.HUD_FONT,  util.HUD_RED,  (startx,  0))
        self.newSprite(text)
        
        for i in range(self.life):
            x = i*10 + startx
            heart = Heart((x,12))
            self.hearts.append(heart)
            self.newSprite(heart)
            
    def loseLife(self):
        heart = self.hearts.pop()
        heart.kill()



class Heart(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = util.load_png('heart.png')
        self.rect.x, self.rect.y = pos
