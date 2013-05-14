import pygame
import util
import lifebar
import math
import random
from observer import Signal
from weapons import Weapons
from powerup import PowerupDash

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #signals
        self.newSprite = Signal()
        self.newMissile = Signal()
        
        self.image, self.rect = util.load_png('ship.png')

        self.area = pygame.display.get_surface().get_rect()
        self.original_image = self.image
        self.missiles = pygame.sprite.Group()

        self.MAX_INVULNERABLE_TIME = 40

        self.pixelArray = pygame.PixelArray(self.image)
        self.DEFAULT_SHIP_COLOR = self.getShipColor()

    def init(self):
        self.speed = 5
        self.theta = 0

        self.thrusters = {}
        
        self.rect.center = self.area.center

        self.firing = False
        self.missile_reload = 0
        
        self.weapons = self.newWeapons()
        self.weapons.addWeapon(util.ONEMISSILE, util.UNLIMITED_AMMO)
        
        self.passiveWeapons = self.newWeapons()

        self.life = 3
        self.lifebar = lifebar.Lifebar(self.life)
        
        self.lifebar.newSprite.connect(self.newSprite)
        self.lifebar.init()
        
        self.powerupDash = self.newPowerupDash()
        self.passivePowerupDash = self.newPowerupDash()
        
        self.vulnerable = True

        self.setShipColor(self.DEFAULT_SHIP_COLOR)
        
    def newWeapons(self):
        weapons = Weapons()
        weapons.newMissile.connect(self.newMissile)
        weapons.newSprite.connect(self.newSprite)
        weapons.init()
        return weapons
        
    def newPowerupDash(self):
        dash = PowerupDash()
        dash.newSprite.connect(self.newSprite)
        dash.init()
        return dash
        
    def update(self):
        
        #move the ship
        moveoffset = self.getMoveOffset()
        newpos = self.rect.move(moveoffset)
        if self.area.contains(newpos):
            self.rect = newpos

        #rotate the ship
        self.theta = self.calculate_missile_angle(pygame.mouse.get_pos())
        self.image = pygame.transform.rotate(self.original_image, -180*self.theta/math.pi - 90 )
        self.rect.center = self.rect.center
        
        self.fire(self.passiveWeapons)

        #countdown invulnerablity
        if not self.vulnerable:
            self.invulnerable_time += 1
            if self.invulnerable_time == self.MAX_INVULNERABLE_TIME:
                self.vulnerable = True
                self.setShipColor(self.DEFAULT_SHIP_COLOR)
        
        #update all the sprites owned by the ship
        self.missiles.update()
        self.weapons.update()
        self.passiveWeapons.update()
        
        #reset thrusters
        self.thrusters = {}

    def getMoveOffset(self):
        x = 0
        y = 0
        
        for key in self.thrusters.iterkeys():
            if key == util.LEFT:
                x -= self.speed
            elif key == util.RIGHT:
                x += self.speed
            elif key == util.UP:
                y -= self.speed
            elif key == util.DOWN:
                y += self.speed
                
        return (x, y)
        
    def setShipColor(self, color):
        ship_color = self.getShipColor()
        if ship_color != color:
            self.pixelArray.replace(ship_color, color)
            
    def getShipColor(self):
        return self.pixelArray[4][0]
            

    def fire(self,  weapons = None):
        weapons = weapons or self.weapons
        weapons.fireCurrentWeapon(self.rect.center,  self.theta)

    def calculate_missile_angle(self, mousePos):
        mouseX, mouseY = mousePos
        x = mouseX - self.rect.x
        y = mouseY - self.rect.y

        if x != 0:
            theta = math.atan(float(y)/float(x))
            if x < 0:
                theta += math.pi
        elif y < 0:
            theta = math.pi*3/2
        else:
            theta = math.pi/2
            
        return theta

    def thrust(self, direction):
        self.thrusters[direction] = True
        

    def takedamage(self):
        if self.vulnerable:
            self.life -= 1
            self.vulnerable = False
            self.invulnerable_time = 0
            self.setShipColor((254,0,0))
            self.lifebar.loseLife()
            
    def addPowerup(self,  type):
        if type == util.POWERUP_MULTISHOT:
            nMissiles = random.randint(2,5)
            self.weapons.addWeapon(util.getMultishotWeaponType(nMissiles), 20)
            self.powerupDash.changePowerup("multishot")
            
        elif type == util.POWERUP_BIGSHOT:
            self.weapons.addWeapon(util.BIGSHOT,  8)
            self.powerupDash.changePowerup("bigshot")
        
        elif type == util.POWERUP_BUTTBOMB:
            self.passiveWeapons.addWeapon(util.BUTTBOMB,  4)
            self.passivePowerupDash.changePowerup("buttbomb")
