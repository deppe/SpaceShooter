import util
import operator
import math
from combocounter import comboCounter
from observer import Signal
from projectile import Projectile


import pygame

class MissileLauncher:
    def __init__(self,  type,  nMissiles,  ammunition,  cooldown, speed = 5,  missileSize = 1,  missileLife = 1):
        self.newMissile = Signal()
        
        self.type = type
        self.ammunition = ammunition
        self.nMissiles = nMissiles
        self.missileSize = missileSize
        self.COOLDOWN = cooldown
        self.missileLife = missileLife
        self.reload = 0
        self.speed = speed
        
    def fire(self,  pos,  theta):
        if self.reload == 0:
            
            comboId = comboCounter.createNewCombo()
            #print comboId
            fireMiddileMissile = True
            if operator.mod(self.nMissiles,  2) == 0:
                fireMiddileMissile = False
            
            angleOffset = 15 * math.pi / 180
            missilesPerSide = self.nMissiles / 2
            
            for i in range(-missilesPerSide,  missilesPerSide + 1):
                if (i is not 0 or (i is 0 and fireMiddileMissile)):
                    missile = Projectile(pos, theta + angleOffset*i, self.speed,  comboId,   self.missileSize,  self.missileLife)
                    self.newMissile(missile)
                    
            self.reload = self.COOLDOWN
            
            if self.ammunition is not util.UNLIMITED_AMMO:
                self.ammunition -= 1
            
    def update(self):
        if self.reload is not 0:
            self.reload -= 1
