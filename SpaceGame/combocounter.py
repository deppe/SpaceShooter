import pygame
import util
from observer import Signal
    
class ComboCounter:
    def __init__(self):
        self.newSprite = Signal()
        
        self.comboPos = (35,  10)
        
        self.comboDict = {}
        self.currentId = 0
        
        self.comboCount = 0
        
        self.comboText = pygame.sprite.GroupSingle()
        
    def init(self):
        text = util.Text("Combo",  util.HUD_FONT,  util.HUD_RED,  (35, 0))
        self.newSprite(text)
        
        text = util.Text(str(self.comboCount),  util.HUD_FONT,  util.HUD_RED,  self.comboPos)
        self.comboText.add(text)
        self.newSprite(text)
        
    
    def createNewCombo(self):
        id = self.currentId
        self.comboDict[id] = (0, 0)
        self.currentId += 1
            
        return id
        
    def addCount(self,  id,  increaseComboCount,  increaseObjectCount):
        nCombos,  nObjects = self.comboDict[id]
        
        if increaseComboCount : 
            nCombos += 1
        if increaseObjectCount:
            nObjects += 1
        
        self.comboDict[id] = (nCombos,  nObjects)
        if nCombos > self.comboCount:
            self.comboCount = nCombos
            self.updateComboCount(self.comboCount)
        
    def dropObjectCount(self,  id):
        nCombos,  nObjects = self.comboDict[id]
        nObjects -= 1
        
        self.comboDict[id] = (nCombos,  nObjects)
    
        if nObjects == 0:
            del self.comboDict[id]
            
            
    def updateComboCount(self,  comboCount):
        text = self.comboText.sprites()[0]
        text.kill()
        
        self.comboCount = comboCount
        
        text = util.Text(str(self.comboCount),  util.HUD_FONT,  util.HUD_RED, self.comboPos)
        self.comboText.add(text)
        self.newSprite(text)
        
comboCounter = ComboCounter()
