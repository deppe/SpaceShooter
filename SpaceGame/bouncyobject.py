import pygame
import random
import util
import math

class GenericBouncyObject(pygame.sprite.Sprite):
    def __init__(self, side, vector, imagename):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = util.load_png(imagename)
        
        self.area = pygame.display.get_surface().get_rect()
        self.vector = vector
        
        self.setuppos(side)
        self.x,self.y = self.rect.centerx, self.rect.centery
        
        
    def setuppos(self, side):
        
        x = self.area.width - self.rect.width - 5
        y = self.area.height - self.rect.height - 5
        if side == "top":
            self.rect.topleft = (random.randint(5, x), 5)
        elif side == "bottom":
            self.rect.bottomleft = (random.randint(5, x), self.area.height - 5)
        elif side == "right":
            self.rect.topright = (self.area.width - 5, random.randint(5, y))
        elif side == "left":
            self.rect.topleft = (5, random.randint(5, y))

    def update(self):
        self.x, self.y = self.calcnewpos(self.rect, self.vector)
        self.rect.centerx, self.rect.centery = self.x, self.y

        (theta, z) = self.vector

        if not self.area.contains(self.rect):
            tl = not self.area.collidepoint(self.rect.topleft)
            tr = not self.area.collidepoint(self.rect.topright)
            bl = not self.area.collidepoint(self.rect.bottomleft)
            br = not self.area.collidepoint(self.rect.bottomright)
            
            if tr and tl or (br and bl):
                theta = -theta
            if tl and bl:
                theta = math.pi - theta
            if tr and br:
                theta = math.pi - theta
        self.vector = (theta,z)

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return (self.x+dx, self.y+dy)


class RandomBouncyObject(pygame.sprite.Sprite):
    def __init__(self, side, vector, imagename):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = util.load_png(imagename)
        
        self.area = pygame.display.get_surface().get_rect()
        self.vector = vector
        
        self.setuppos(side)
        self.x,self.y = self.rect.centerx, self.rect.centery
        
        self.countdownToTurn = self.getNewCountdown()
    
    def getNewCountdown(self):
        return random.randint(30, 250)
        
    def setuppos(self, side):
        
        x = self.area.width - self.rect.width - 5
        y = self.area.height - self.rect.height - 5
        if side == "top":
            self.rect.topleft = (random.randint(5, x), 5)
        elif side == "bottom":
            self.rect.bottomleft = (random.randint(5, x), self.area.height - 5)
        elif side == "right":
            self.rect.topright = (self.area.width - 5, random.randint(5, y))
        elif side == "left":
            self.rect.topleft = (5, random.randint(5, y))
            
    def update(self):
        if self.countdownToTurn is 0:
            self.vector = util.getRandomVector()
            self.countdownToTurn = self.getNewCountdown()
        else:
            self.countdownToTurn -= 1
            
        self.x, self.y = self.calcnewpos(self.rect, self.vector)
        self.rect.centerx, self.rect.centery = self.x, self.y

        (theta, z) = self.vector

        if not self.area.contains(self.rect):
            tl = not self.area.collidepoint(self.rect.topleft)
            tr = not self.area.collidepoint(self.rect.topright)
            bl = not self.area.collidepoint(self.rect.bottomleft)
            br = not self.area.collidepoint(self.rect.bottomright)
            
            self.vector = util.getRandomVector()
            
            if tr and tl:
                self.y += 3
            if br and bl:
                self.y -= 3
                
            if tl and bl:
                self.x += 3
            if tr and br:
                self.x -= 3

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return (self.x+dx, self.y+dy)
