import pygame
import util
import random
import math
from projectile import Projectile
from bouncyobject import RandomBouncyObject
from observer import Signal

class Mothership(RandomBouncyObject):
    def __init__(self,  side,  vector):
        RandomBouncyObject.__init__(self, side, vector, "mothership.png")
        
        self.newMissile = Signal()
        
        self.newMissileCountdown()
        
        self.alive = True
        
    
    def update(self):
        RandomBouncyObject.update(self)
        
        self.fireMissile()
        
    def newMissileCountdown(self):
        self.missileCountdown = 10
        
    def fireMissile(self):
        if self.missileCountdown is 0:
            theta = self.vector[0]
            theta += random.uniform(-30 ,  30) * math.pi / 180
            missile = Projectile(self.rect.center,  theta)
            self.newMissile(missile)
            self.newMissileCountdown()
        else:
            self.missileCountdown -= 1
        
        
