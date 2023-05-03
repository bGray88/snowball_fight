import pygame, sys
from pygame.locals import *

class Level:
    
    def __init__(self, levelName, levelSize, background, levelwalls = None):
        self.name = levelName
        self.walls = levelwalls
        self.levelBorder = Rect(0, 0, levelSize[0], levelSize[1])
        self.set_level_img(background)
            
    def set_level_img(self, imgName):
        self.bkgdImg = pygame.image.load(imgName)
    