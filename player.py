import pygame
from pygame.locals import *
from pygame.constants import *

class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = color

        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.velX = 0
        self.velY = 0
        self.score = 0

        self.canJump = False

    def update(self):
        self.x += self.velX
        self.y += self.velY

        if self.x < 0:
            self.x = 0
            self.velX = 0

        if self.y < 0:
            self.y = 0
            self.velY = 0

        if self.x > 800 - self.width:
            self.x = 800 - self.height
            self.velX = 0

        if self.y > 600 - self.height:
            self.y = 600 - self.height
            self.velY = 0

        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, x, y):
        self.velX += x
        self.velY += y
