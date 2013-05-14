import pygame
import random
import math
import util
from pygame.locals import *

from enemy import Enemy
from observer import Signal
from ship import Ship
from killcounter import KillCounter
from combocounter import comboCounter
from explosion import Explosion
from powerup import Powerup
from mothership import Mothership

class SpaceActionState:
    def __init__(self,  screen,  background):
        
        #signals
        self.endState = Signal()
        
        self.screen = screen
        self.background = background
        
        self.level = 0
        
        self.allsprites = pygame.sprite.RenderUpdates()
        
        self.dispatcher = Dispatcher()
        self.dispatcher.newSprite.connect(self.onNewSprite)
        self.dispatcher.shipDestroyed.connect(self.onShipDestroyed)
        
        self.dispatcher.init()
        
    def onNewSprite(self,  sprite):
        self.allsprites.add(sprite)
        
    def handleEvent(self,  input):
        ship = self.dispatcher.getShip()
        if (ship is not None):
            if input.isactive(K_a): ship.thrust(util.LEFT)
            if input.isactive(K_d): ship.thrust(util.RIGHT)
            if input.isactive(K_s): ship.thrust(util.DOWN)
            if input.isactive(K_w): ship.thrust(util.UP)
        
            if input.isactive(input.butt[1]):
                ship.fire()
        else:
            if input.isactive(K_RETURN):
                self.endState()
            
    def update(self):
        self.dispatcher.dispatch()
        self.dispatcher.checkCollisions()
        
        self.allsprites.update()
        self.allsprites.clear(self.screen, self.background)
        changes = self.allsprites.draw(self.screen)
        pygame.display.update(changes)
        
    def killAllSprites(self):
        for sprite in self.allsprites.sprites():
            sprite.kill()
            
    def onShipDestroyed(self):
        self.dispatcher.destroyShip()
        
        msg = "The world is fucking destroyed"
        font = pygame.font.Font("freesansbold.ttf",40)
        color = (230, 0, 0)
        x, y = self.background.get_rect().midleft
        y -= 40
        text = util.Text(msg, font,  color,  (x, y))
        self.allsprites.add(text)
        
        msg = "Press enter to start game"
        color = (40 , 40, 40)
        pos = (self.background.get_rect().midleft)
        text = util.Text(msg, font,  color,  pos)
        self.allsprites.add(text)
        

class Dispatcher:
    def __init__(self):
                
        #signals
        self.newSprite = Signal()
        self.shipDestroyed = Signal()
        
        self.ship = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        
        self.powerups = pygame.sprite.Group()
        
        #hostiles are anything that can damage the ship
        self.hostiles = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        
    def init(self):
        self.level = 0
        
        self.createShip()
        self.createKillCounter()
        self.createComboCounter()
        
        self.createDispatchers()
    
    def createDispatchers(self):
        
        if self.level == 0:
            self.enemyCount = 1
            self.dispatchMotherShip()
            self.dispatchers = []
            
            
        if self.level == 1:
            self.enemyCount = 100
            self.dispatchers = [ DispatchCountdown((10, 30),  self.dispatchEnemy), 
                                    DispatchCountdown((100,  300),  self.dispatchPowerup), 
                                    DispatchKillCount(self.killCounter,  5,  self.dispatchMotherShip) ]
            
                                        
    def getShip(self):
        return util.getSingleSprite(self.ship)
            
        
    def checkCollisions(self):
        #explode any enemies that hit an explosion
        collisions = pygame.sprite.groupcollide(self.explosions, self.enemies, False, False)
        for explosion,  enemies in collisions.iteritems():
            comboId= explosion.comboId
            for enemy in enemies:
                self.destroyEnemy(enemy,  comboId)
                
        #exlode any enemies that hit a missile
        ship = self.getShip()
        if ship is not None:
            collisions = pygame.sprite.groupcollide(self.missiles, self.enemies, False, False)
            for missile,  enemies in collisions.iteritems():
                for enemy in enemies:
                    self.destroyEnemy(enemy,  missile.comboId)
                missile.takeDamage()
                if missile.isDestroyed():
                    #todo: maybe have the missile have a destruction?
                    missile.kill()
    
            #see if the ship hit a hostile
            collisions = pygame.sprite.spritecollide(ship, self.hostiles, False)
            if len(collisions) > 0:
                ship.takedamage()
                
            collisions = pygame.sprite.spritecollide(ship, self.powerups,  False)
            
            for powerup in collisions:
                ship.addPowerup(powerup.type)
                powerup.kill()
        
            if (ship.life == 0):
                self.shipDestroyed()
            
    def createShip(self):
        ship = Ship()
        ship.newSprite.connect(self.newSprite)
        ship.newMissile.connect(self.onNewMissile)
        ship.init()
        
        self.ship.add(ship)
        self.newSprite(self.ship)
        
    def onNewMissile(self,  missile):
        self.missiles.add(missile)
        self.newSprite(missile)
        
    def dispatch(self):
        for dispatcher in self.dispatchers:
            dispatcher.dispatch()
        
    def addEnemy(self,  enemy):
        
        if self.enemyCount != 0:
            self.enemies.add(enemy)
            self.hostiles.add(enemy)
            
            self.newSprite(enemy)
            self.enemyCount -= 1
        
    def dispatchEnemy(self):
        enemy = Enemy(self.getRandomSide(), util.getRandomVector(), self.getRandomColor())
            #enemy = Enemy("left",  (0, 3),  (50, 50, 50))
            
        self.addEnemy(enemy)
        
    def dispatchMotherShip(self):
        enemy = Mothership(self.getRandomSide(),  util.getRandomVector())
        enemy.newMissile.connect(self.newEnemyMissile)
        
        self.addEnemy(enemy)
            
    def newEnemyMissile(self, missile):
        self.hostiles.add(missile)
        self.newSprite(missile)
        
    def dispatchPowerup(self):
        powerup = Powerup(self.getRandomSide(), util.getRandomVector(), self.getRandomColor())
        self.powerups.add(powerup)
        
        self.newSprite(powerup)
        
    def createKillCounter(self):
        self.killCounter = KillCounter()
        self.killCounter.newSprite.connect(self.newSprite)
        self.killCounter.init()
        
    def createComboCounter(self):
        comboCounter.newSprite.connect(self.newSprite)
        comboCounter.init()


    def getRandomColor(self):
        return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        
    def getRandomSide(self):
        return ["left",  "right",  "top",  "bottom"][random.randint(0,3)]

    def destroyShip(self):
        ship = self.getShip()
        ship.kill()
        
        comboId = comboCounter.createNewCombo()
        self.createExplosion((ship.rect.centerx,  ship.rect.centery),  (0, 0),  comboId)
        
        
    def onEnemyExploded(self, explosion):
        self.explosions.add(explosion)
        self.hostiles.add(explosion)
        
        self.newSprite(explosion)
        
        
    def createExplosion(self, pos,  vector,  comboId):
            
        #create explosion and connect to destroy signal
        explosion = Explosion(pos, vector,  comboId)
        
        #add to sprite groups
        self.explosions.add(explosion)
        self.hostiles.add(explosion)
        
        #raise new sprite signal
        self.newSprite(explosion)
        
    def destroyEnemy(self, enemy,  comboId):
        if enemy.alive == True:
            
            self.createExplosion(enemy.rect.center,  enemy.vector,  comboId)

            self.killCounter.addKill()
            
            enemy.kill()
            enemy.alive = False

class DispatchCountdown:
    def __init__(self,  range,  callback):
        self.range = range
        self.callback = callback
        
        self.countdown = self.getCountdown()
        
    def getCountdown(self):
        return random.randint(*self.range)
        
    def dispatch(self):
        self.countdown -= 1
        if (self.countdown == 0):
            self.callback()
            self.countdown = self.getCountdown()
            
class DispatchKillCount:
    def __init__(self,  killCounter,  count,  callback):
        self.killCounter = killCounter
        self.count = count
        self.callback = callback
        
    def dispatch(self):
        #print self.killCounter.killCount,  self.count
        if (self.killCounter.killCount is self.count):
            self.callback()
            self.count += 5
