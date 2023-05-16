import pickle
import random
import socket
from _thread import *
import sys

import pygame

from player import Player
from pickup import Pickup

from constants import *


def check_pickups(player_num, pickups):
    for pickup in pickups:
        if players[player_num].rect.colliderect(pickup.rect):
            pickups.remove(pickup)
            del pickup
            # scores[player_num] += 100

def server_logic():
    clock = pygame.time.Clock()

    run = True
    while run:
        if len(pickups) < 10:
            pickup_x = random.randint(0, 700)
            pickup_y = random.randint(0, 500)
            pickup_size = 20
            new_pickup = Pickup(pickup_x, pickup_y, pickup_size)
            pickups.append(new_pickup)

        # for bullet in bullets:
        #     bullet.update()

        for playerNum in range(len(players)):
            check_pickups(playerNum, pickups)

            # for bullet in bullets:
            #     if players[playerNum].rect.colliderect(bullet.rect) and bullet.owner != players[playerNum]:
            #         players[playerNum].velX += 10 * bullet.velX
            #         players[playerNum].velY += 10 * bullet.velY
            #         bullets.remove(bullet)
            #         del bullet



        clock.tick(60)



# Tworzenie gniazda sieciowego (socket) z rodzajem AF_INET (IPv4) i typem SOCK_STREAM (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Próba powiązania gniazda z adresem IP serwera i portem
try:
    s.bind((SERVER, PORT))

except socket.error as e:
    str(e)
try:
    # Nasłuchiwanie połączeń przychodzących z maksymalnie 10 klientami
    s.listen(10)
    print("Waiting for a connection, server Started")

    players = []
    pickups = []

    for i in range(10):
        pickup_x = random.randint(0, 700)
        pickup_y = random.randint(0, 500)
        pickup_size = 20
        new_pickup = Pickup(pickup_x, pickup_y, pickup_size)
        pickups.append(new_pickup)

    # Definicja funkcji obsługującej klienta
    def threaded_client(conn, player_number):
        # Wysłanie informacji o nawiązaniu połączenia z klientem
        conn.send(pickle.dumps(players[player_number]))

        reply = ""
        while True:
            if len(pickups) < 10:
                pickup_x = random.randint(0, 700)
                pickup_y = random.randint(0, 500)
                pickup_size = 20
                new_pickup = Pickup(pickup_x, pickup_y, pickup_size)
                pickups.append(new_pickup)

            # print(player)
            # print(players[player])
            # try:
            #     check_pickups(players[player], pickups)
            # except Exception as e:
            #     print(e)

            try:
                # Odczytanie danych od klienta
                data = pickle.loads(conn.recv(2048))

                # Sprawdzenie, czy odebrano jakieś dane
                if not data:
                    print("Disconnected")
                    break
                elif data == "pickups":
                    reply = pickups
                # elif data == "score":
                #     reply = scores[player_number]
                #
                # elif data == "bullets":
                #     reply = bullets

                elif isinstance(data, Player):
                    players[player_number] = data
                    reply = players

                # elif isinstance(data, Bullet):
                #     bullets.append(data)
                #     # Odeślij zaktualizowane dane gracza do klienta
                #     reply = bullets
                else:
                    reply = ""

                conn.sendall(pickle.dumps(reply))
            except:
                break
        # Wyświetlenie komunikatu o utraceniu połączenia z klientem i zamknięcie połączenia

        print("Lost connection")
        try:
            players.pop(player_number)
        except:
            conn.close()


    start_new_thread(server_logic, ())

    currentPlayer = 0
    # Nieskończona pętla while, w której serwer przyjmuje nowych klientów i tworzy dla nich nowe wątki
    while True:
        conn, addr = s.accept()
        print(f"Connected to: {addr}.")

        # Dodanie nowego gracza do puli
        randColor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        players.append(Player(0, 60 * currentPlayer, 50, 50, randColor))

        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
except error as e:
    print("BŁOND: ", e)