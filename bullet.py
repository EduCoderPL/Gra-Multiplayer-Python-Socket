import pygame
from pygame.locals import *
from pygame.constants import *

class Bullet:
    def __init__(self, x, y, velX, velY, color, owner):
        self.x = x + velX * 10
        self.y = y + velY * 10
        self.width = 10
        self.height = 10

        self.color = color

        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.velX = velX
        self.velY = velY

        self.owner = owner

    def update(self):
        self.x += self.velX
        self.y += self.velY

        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, x, y):
        self.velX += x
        self.velY += y

