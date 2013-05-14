import memoizer
import weakref
import pygame
import os
import random
import math

memoize = memoizer.memoizer(new_dict=weakref.WeakValueDictionary)


UP    = "up"
DOWN  = "down"
LEFT  = "left"
RIGHT = "right"


POWERUP_MULTISHOT = "multishot"
POWERUP_BIGSHOT = "bigshot"
POWERUP_BUTTBOMB = "buttbomb"

ONEMISSILE = "one_missile"
TWOMISSILE = "two_missile"
THREEMISSILE = "three_missile"
FOURMISSILE = "four_missile"
FIVEMISSILE = "five_missile"
SIXMISSILE = "six_missile"
SEVENMISSILE = "seven_missile"
BIGSHOT = "big_shot"
BUTTBOMB = "butt_bomb"

UNLIMITED_AMMO = -99

HUD_RED = (240, 0, 0)
HUD_FONT = None

    
def load_entire_image(name):
    """Loads the image with the given name."""
 
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image
 

def load_png(name, colorkey=None, rect=None):
    """Returns a rectangular portion of a named image."""
 
    image = load_entire_image(name)
    if rect is not None:
        image = image.subsurface(Rect(rect))
    if colorkey is -1:
        colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey)
    return image, image.get_rect()

##def load_png(name):
##        """ Load image and return image object"""
##        fullname = os.path.join('data', name)
##        image = pygame.image.load(fullname)
##        if image.get_alpha is None:
##            image = image.convert()
##        else:
##            image = image.convert_alpha()
##        return image, image.get_rect()
##
##def load_png(name):
##        """ Load image and return image object"""
##        image = load_image(name)
##        return image, image.get_rect()

class Text(pygame.sprite.Sprite):
    def __init__(self, text, font, color, pos):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.font = font
        self.image = self.font.render(text, 1, self.color)
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = pos
    
    def changeText(self,  text):
        self.image = self.font.render(text,  1,  self.color)

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    return pygame.mixer.Sound(fullname)
    
#returns the sprite from a GroupSingle 
def getSingleSprite(groupSingle):
    sprite = groupSingle.sprites()
    if (len(sprite) == 0):
        return None
    else:
        return sprite[0]
        
def getMultishotWeaponType(nMissiles):
    type = {
        1 : ONEMISSILE, 
        2 : TWOMISSILE, 
        3 : THREEMISSILE, 
        4 : FOURMISSILE, 
        5 : FIVEMISSILE, 
        6 : SIXMISSILE, 
        7 : SEVENMISSILE
        }[nMissiles]
    return type
    
def getRandomVector():
    z = random.randint(1,5)
    theta = random.uniform(0, 2*math.pi)
    return (theta, z)
