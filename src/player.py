import pygame, sys
from pygame.locals import *

class Player:
    
    def __init__(self, playerWidth, playerHeight, playerSpeed, 
                 maxSpeedMod, initPos, playerThrow, playerName, basicImg):
        # Player model
        self.xSize = playerWidth
        self.ySize = playerHeight
        self.xMid = (self.xSize / 2)
        self.yMid = (self.ySize / 2)
        self.playerX = initPos[0]
        self.playerY = initPos[1]
        self.playerRect = Rect(
                               self.playerX,
                               self.playerY,
                               self.xSize,
                               self.ySize
                               )
        # Player stats
        self.name = playerName
        self.throwSpeed = playerThrow
        self.initSpeed = playerSpeed
        self.xSpeed = self.initSpeed
        self.ySpeed = self.initSpeed
        self.maxSpeed = self.initSpeed * maxSpeedMod
        self.set_player_img(basicImg)
        self.currentImgIndex = 0
        self.playerAnimate = []
        #self.playerFail = []
        self.currentHealth = 10
        self.maxHealth = self.currentHealth
    
    def animate_player(self, direction):
        endImgIndex = len(self.playerAnimate)
        if self.currentImgIndex < endImgIndex:
            self.currentImgIndex = self.currentImgIndex + direction
            if self.currentImgIndex == endImgIndex:
                self.currentImgIndex = 0
            if direction < 0 and self.currentImgIndex < 0:
                self.currentImgIndex = endImgIndex - 1
        self.currentAnimateImg = self.playerAnimate[self.currentImgIndex]
            
    def check_external_bounds(self, wallRects):        
        for wall in wallRects:
            if self.playerRect.colliderect(wall):
                if self.playerRect.left < wall.right and self.playerRect.right > wall.right:
                    self.playerRect.left = wall.right
                if self.playerRect.right > wall.left and self.playerRect.left < wall.left:
                    self.playerRect.right = wall.left
                if self.playerRect.bottom < wall.top and self.playerRect.top > wall.top:
                    self.playerRect.bottom = wall.top
                if self.playerRect.top > wall.bottom and self.playerRect.bottom < wall.bottom:
                    self.playerRect.top = wall.bottom
            
    def check_internal_bounds(self, boundRect):
        if self.playerRect.left <= 10:
            self.playerRect.left = 10
        if self.playerRect.top <= 10:
            self.playerRect.top = 10
        if self.playerRect.left >= (boundRect.width - self.playerRect.width - 10):
            self.playerRect.left = (boundRect.width - self.playerRect.width - 10)
        if self.playerRect.top >= (boundRect.height - self.playerRect.height - 50):
            self.playerRect.top = (boundRect.height - self.playerRect.height - 50)
    
    def decrement_health_counter(self):
        if self.currentHealth > 0:
            self.currentHealth = self.currentHealth - 1
    
    def get_hit_reaction(self, playerNum, enemyThrowSpeed):
        self.stop_player_movement()
        self.decrement_health_counter()
        if playerNum % 2 == 0:
            self.playerRect.left += (enemyThrowSpeed * 2)
        else:
            self.playerRect.left -= (enemyThrowSpeed * 2)
            
    def move_player(self, direction):
        if direction == 'Up':
            if self.ySpeed < self.maxSpeed:
                self.ySpeed += self.initSpeed
            self.playerRect.top -= self.ySpeed
        if direction == 'Down':
            if self.ySpeed < self.maxSpeed:
                self.ySpeed += self.initSpeed
            self.playerRect.top += self.ySpeed
        if direction == 'Left':
            if self.xSpeed < self.maxSpeed:
                self.xSpeed += self.initSpeed
            self.playerRect.left -= self.xSpeed
        if direction == 'Right':
            if self.xSpeed < self.maxSpeed:
                self.xSpeed += self.initSpeed
            self.playerRect.left += self.xSpeed
    
    def reset_speed(self, direction):
        if direction == 'yRelease':
            self.ySpeed = self.initSpeed
        if direction == 'xRelease':
            self.xSpeed = self.initSpeed
        
    def set_player_animate(self, imgNames):
        if len(imgNames) > 1:
            for img in imgNames:
                self.playerAnimate.append(pygame.image.load(img))
        else:
            self.playerAnimate = pygame.image.load(imgNames[0])
        self.currentAnimateImg = self.playerAnimate[0]
    
    def set_player_animate_fail(self, imgNames):
        pass
    
    def set_player_img(self, imgName):
        self.playerImg = pygame.image.load(imgName)
        
    def stop_player_movement(self):
        self.ySpeed = 0
        self.xSpeed = 0
    
    def throw_projectile(self, playerNum):
        if playerNum % 2 == 0:
            self.throwDirection = -1
        else:
            self.throwDirection = 1
        return self.throwSpeed, self.throwDirection
