import pickle
import random
import socket
from _thread import *
import sys

from player import Player
from pickup import Pickup

from constants import *


def check_pickups(player, pickups):
    for pickup in pickups:
        if player.rect.colliderect(pickup.rect):
            pickups.remove(pickup)
            player.score += 1


# Tworzenie gniazda sieciowego (socket) z rodzajem AF_INET (IPv4) i typem SOCK_STREAM (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Próba powiązania gniazda z adresem IP serwera i portem
try:
    s.bind((SERVER, PORT))

except socket.error as e:
    str(e)

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
            players[player_number] = data

            # Sprawdzenie, czy odebrano jakieś dane
            if not data:
                print("Disconnected")
                break
            elif data == "pickups":
                reply = pickups
            else:
                reply = players

                # # Wyświetlenie otrzymanych danych
                # print(f"Received: {reply}")
                # # Przesłanie tych samych danych z powrotem do klienta
                # print(f"Sending: {reply}")

            conn.sendall(pickle.dumps(reply))
        except:
            break
    # Wyświetlenie komunikatu o utraceniu połączenia z klientem i zamknięcie połączenia

    print("Lost connection")
    try:
        players.pop(player_number)
    except:
        conn.close()

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