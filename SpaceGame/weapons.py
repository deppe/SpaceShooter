import util
from observer import Signal
from missilelauncher import MissileLauncher

import pygame

class Weapons:
    def __init__(self):
        self.newMissile = Signal()
        self.newSprite = Signal()
        
        self.weapons = []
        
    def init(self):
        #weapon = self.createWeapon(util.ONEMISSILE, util.UNLIMITED_AMMO)
        #self.weapons.append(weapon )
        self.currentWeaponIndex = -1
        
        self.ui = WeaponUI()
        self.ui.newSprite.connect(self.newSprite)
        self.ui.init()
        
    #this whole thing is very broken...
    def addWeapon(self,  type,  ammunition):
        newWeapon = True
        for weapon in self.weapons:
            if weapon.type == type:
                if ammunition != util.UNLIMITED_AMMO:
                    weapon.ammunition += ammunition
                newWeapon = False
                
        if newWeapon:
            weapon = self.createWeapon(type,  ammunition)
            weapon.newMissile.connect(self.newMissile)
            
            self.weapons.append(weapon)
            self.currentWeaponIndex = len(self.weapons) - 1
            
    def createWeapon(self,  type,  ammunition):
        weapon = {
                  util.ONEMISSILE : lambda ammo : MissileLauncher(type,  1, ammo, 10), 
                  util.TWOMISSILE : lambda ammo : MissileLauncher(type,  2, ammo, 15), 
                  util.THREEMISSILE : lambda ammo : MissileLauncher(type,  3, ammo, 25), 
                  util.FOURMISSILE : lambda ammo : MissileLauncher(type,  4, ammo, 30), 
                  util.FIVEMISSILE : lambda ammo : MissileLauncher(type,  5, ammo, 45), 
                  util.SIXMISSILE : lambda ammo : MissileLauncher(type,  6, ammo, 50), 
                  util.SEVENMISSILE : lambda ammo : MissileLauncher(type,  7, ammo, 60), 
                  util.BIGSHOT : lambda ammo : MissileLauncher(type,  1, ammo, 40,  5,  7,  10), 
                  util.BUTTBOMB : lambda ammo : MissileLauncher(type,  1,  ammo,  35,  0,  3,  2)
                  }[type](ammunition)
            
        weapon.newMissile.connect(self.newMissile)
        
        return weapon
            
    def fireCurrentWeapon(self,  pos,  theta):
        if self.currentWeaponIndex == -1:
            return
            
        weapon = self.getCurrentWeapon()
        weapon.fire(pos,  theta)
        
        if weapon.ammunition == 0:
            index = self.weapons.index(weapon)
            self.removeCurrentWeapon()
            
            if index is self.currentWeaponIndex or index < self.currentWeaponIndex:
                self.currentWeaponIndex -= 1
            
    def getCurrentWeapon(self):
        return self.weapons[self.currentWeaponIndex]
        
    def removeCurrentWeapon(self):
        del self.weapons[self.currentWeaponIndex]
        
    def update(self):
        if self.currentWeaponIndex == -1:
            return
            
        self.ui.updateAmmoCount(self.getCurrentWeapon().ammunition)
        for weapon in self.weapons:
            weapon.update()
        
class WeaponUI():
    def __init__(self):
        self.newSprite = Signal()
        
        self.ammoText = pygame.sprite.GroupSingle()
        
        self.ammoCount = None
        
    def init(self):
        
        text = util.Text("Ammo", util.HUD_FONT,  util.HUD_RED,  (85,  0))
        self.newSprite(text)
        
    def updateAmmoCount(self,  count):
        if (count is not self.ammoCount):
            sprites = self.ammoText.sprites()
            
            if (len(sprites) > 0):
                sprites[0].kill()
            
            str = self.getAmmoString(count)

            self.ammoCount = count
            text = util.Text(str,  util.HUD_FONT,  util.HUD_RED,  (85,  10))
            
            self.ammoText.add(text)
            self.newSprite(text)
    
    def getAmmoString(self,  count):
        if count is util.UNLIMITED_AMMO:
            return "--"
        else:
            return str(count)
