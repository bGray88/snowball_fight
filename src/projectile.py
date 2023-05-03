import pygame, sys, random
from pygame.locals import *

class Projectile:
    
    def __init__(self, projRect, projSpeed, projDirection, projImg):
        self.rect = projRect
        self.xSpeed = projSpeed
        self.ySpeed = random.randint(-20, 20)
        self.direction = projDirection
        self.set_proj_img(projImg)
        self.projAnimate = []
        self.currentImgIndex = 0
    
    def animate_proj(self):
        self.stop_projectile_movement()
        self.endImgIndex = len(self.projAnimate)
        if self.currentImgIndex < self.endImgIndex - 1:
            self.currentImgIndex = self.currentImgIndex + 1
            self.projImg = self.projAnimate[self.currentImgIndex]
        else:
            return 'removeProj'
            
    def move_projectile(self):
        if self.direction > 0:
            self.rect.left += self.xSpeed
            self.rect.top += self.ySpeed
        else:
            self.rect.left -= self.xSpeed
            self.rect.top -= self.ySpeed
    
    def reverse_projY_direction(self):
        self.ySpeed = self.ySpeed * -1
    
    def set_proj_img(self, imgName):
        self.projImg = pygame.image.load(imgName)
    
    def set_proj_animate(self, imgNames):
        if len(imgNames) > 1:
            for img in imgNames:
                self.projAnimate.append(pygame.image.load(img))
        else:
            self.projAnimate = pygame.image.load(imgNames[0])
    
    def stop_projectile_movement(self):
        self.xSpeed = 0
        self.ySpeed = 0
    