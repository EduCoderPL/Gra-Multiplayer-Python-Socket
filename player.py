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
        self.velY = 0
        self.score = 0

    def update(self):
        self.velY += 0.5
        self.y += self.velY

        if self.y > 600 - self.height:
            self.y = 600 - self.height
            self.velY *= -1

        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, x, y):
        self.x += x
        self.y += y