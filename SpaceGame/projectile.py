import pygame
import math
import util

from combocounter import comboCounter


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, theta, speed = 5,  comboId = None,   size = 1,  life = 1):
        pygame.sprite.Sprite.__init__(self)
        
        #laserSound = util.load_sound('gunshot.wav')
        #laserSound.play()
        
        self.image, self.rect = util.load_png('missile.png')
        self.area = pygame.display.get_surface().get_rect()
        self.vector = (theta,  speed)
        
        self.image = pygame.transform.scale(self.image, (self.rect.w*size,  self.rect.h*size))
        self.rect = self.image.get_rect()

        self.pos = pos
        self.center = pos
        
        self.life = life
        
        self.comboId = comboId
        
        if self.comboId is not None:
            comboCounter.addCount(self.comboId,  False,  True)

    def update(self):
        self.pos = self.calcnewpos(self.vector)
        self.rect.center = self.pos
        if not self.area.contains(self.rect):
            self.kill()

    def calcnewpos(self,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return (self.pos[0]+dx, self.pos[1]+dy)
        
    def isDestroyed(self):
        return self.life == 0
        
    def takeDamage(self):
        self.life -= 1
        
    def kill(self):
        pygame.sprite.Sprite.kill(self)
        
        if self.comboId is not None:
            comboCounter.dropObjectCount(self.comboId)
