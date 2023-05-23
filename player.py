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

        self.velX *= 0.95
        self.velY *= 0.95

        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera):
        self.drawRect = Rect(self.x - camera.x, self.y - camera.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.drawRect)

    def move(self, x, y):
        self.velX += x
        self.velY += y
