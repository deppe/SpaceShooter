import pygame

from bouncyobject import GenericBouncyObject

class Enemy(GenericBouncyObject):
    def __init__(self, side, vector, color):
        GenericBouncyObject.__init__(self, side, vector, "enemy.png")

        pixelArray = pygame.PixelArray(self.image)
        pixelArray.replace((255,255,255), color) 
        
        self.alive = True
