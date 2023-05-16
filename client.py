import pygame
from pygame.locals import *
from pygame.constants import *

from network import Network

WIDTH = 800
HEIGHT = 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")



def redraw_window(players, pickups):
    screen.fill((0, 0, 0))
    for player in players:
        player.draw(screen)

    for pickup in pickups:
        pickup.draw(screen)

    pygame.display.update()
    clock.tick(60)


def main():
    run = True
    n = Network()
    pickups = n.send("pickups")

    p = n.get_player()


    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            p.move(0, -2)
        if keys[K_s]:
            p.move(0, 2)
        if keys[K_a]:
            p.move(-2, 0)
        if keys[K_d]:
            p.move(2, 0)

        p.update()
        pickups = n.send("pickups")
        all_players = n.send(p)

        redraw_window(all_players, pickups)



if __name__ == "__main__":
    main()
