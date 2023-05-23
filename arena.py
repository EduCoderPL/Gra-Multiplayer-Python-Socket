import pygame
from pygame.locals import Rect


class Arena:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, player):
        if player.x < self.x:
            player.x = self.x
            player.velX = 0

        if player.y < self.y:
            player.y = self.y
            player.velY = 0

        if player.x + player.width > self.x + self.width:
            player.x = self.x + self.width - player.width
            player.velX = 0

        if player.y + player.height > self.y + self.height:
            player.y = self.y + self.height - player.height
            player.velY = 0

    def draw(self, screen, camera):
        self.drawRect = Rect(self.x - camera.x, self.y - camera.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), self.drawRect)
