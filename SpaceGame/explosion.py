import pygame
import math
import util
from observer import Signal
from combocounter import comboCounter

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, vector,  comboId = None):
        pygame.sprite.Sprite.__init__(self)
        
        #explosionSound.play()
        self.image, self.rect = util.load_png('explosion.png')
        self.area = pygame.display.get_surface().get_rect()
        self.x, self.y = pos
        self.rect.centerx, self.rect.centery = pos
        self.vector = vector

        self.lifespan = 45
        self.countdown = self.lifespan
        
        self.comboId = comboId
        
        if self.comboId is not None:
            comboCounter.addCount(self.comboId,  True,  True)
        

    def update(self):
        self.countdown -= 1
        if (self.countdown == 0):
            self.kill()

        alpha = self.countdown*255/self.lifespan
        pixels_alpha = pygame.surfarray.pixels_alpha(self.image)
        pixels_alpha[:,:] = alpha


        theta,z = self.vector
        z -= .1
        if (z < 0):
            z = 0

        self.x, self.y = self.calcnewpos((theta, z))
        self.rect.centerx, self.rect.centery = self.x, self.y

        self.vector = (theta, z)

    def calcnewpos(self,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return (self.x+dx, self.y+dy)
        
    def kill(self):
        pygame.sprite.Sprite.kill(self)
        
        if self.comboId is not None:
            comboCounter.dropObjectCount(self.comboId)
