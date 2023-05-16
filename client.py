import pygame
from pygame.locals import *
from pygame.constants import *

from network import Network
from bullet import Bullet

WIDTH = 800
HEIGHT = 600
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

text_font = pygame.font.SysFont("Helvetica", 30)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def redraw_window(players, pickups, bullets, score):
    screen.fill((0, 0, 0))
    for player in players:
        player.draw(screen)

    for pickup in pickups:
        pickup.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    textToShow = f"Points: {score}"
    draw_text(textToShow, text_font, (255, 255, 255), 20, 20)
    pygame.display.update()
    clock.tick(60)


def main():
    run = True
    n = Network()
    pickups = n.send("pickups")

    score = 0

    p = n.get_player()
    all_players = [p]
    bullets = []

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                newX, newY = pygame.mouse.get_pos()
                mouseVector = newX - p.x, newY - p.y
                length = (mouseVector[0] ** 2 + mouseVector[1] ** 2) ** 0.5
                normVector = mouseVector[0] / length, mouseVector[1] / length
                velocity = 5
                newBullet = Bullet(p.x + p.width/2, p.y + p.height/2, normVector[0] * velocity, normVector[1] * velocity, (255, 255, 255), p)
                bullets = n.send(newBullet)

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            p.move(0, -0.5)
        if keys[K_s]:
            p.move(0, 0.5)
        if keys[K_a]:
            p.move(-0.5, 0)
        if keys[K_d]:
            p.move(0.5, 0)



        p.update()
        all_players = n.send(p)
        pickups = n.send("pickups")
        score = n.send("score")
        bullets = n.send("bullets")

        redraw_window(all_players, pickups, bullets, score)



if __name__ == "__main__":
    main()
