import pickle
import socket
from _thread import *
import sys

from player import Player

server = "192.168.0.193"
port = 5555

# Tworzenie gniazda sieciowego (socket) z rodzajem AF_INET (IPv4) i typem SOCK_STREAM (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Próba powiązania gniazda z adresem IP serwera i portem
try:
    s.bind((server, port))

except socket.error as e:
    str(e)

# Nasłuchiwanie połączeń przychodzących z maksymalnie 2 klientami
s.listen(2)
print("Waiting for a connection, server Started")

players = [Player(0,0,50,50,(255,0,0)), Player(100,100, 50,50, (0,0,255))]


# Definicja funkcji obsługującej klienta
def threaded_client(conn, player):
    # Wysłanie informacji o nawiązaniu połączenia z klientem
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            # Odczytanie danych od klienta
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            # Sprawdzenie, czy odebrano jakieś dane
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                # Wyświetlenie otrzymanych danych
                print(f"Received: {reply}")
                # Przesłanie tych samych danych z powrotem do klienta
                print(f"Sending: {reply}")

            conn.sendall(pickle.dumps(reply))
        except:
            break
    # Wyświetlenie komunikatu o utraceniu połączenia z klientem i zamknięcie połączenia

    print("Lost connection")
    conn.close()

currentPlayer = 0
# Nieskończona pętla while, w której serwer przyjmuje nowych klientów i tworzy dla nich nowe wątki
while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}.")

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1