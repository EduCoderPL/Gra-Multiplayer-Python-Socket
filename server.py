import socket
from _thread import *
import sys

def read_pos(text):
    text = text.split(",")
    return int(text[0]), int(text[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])



#
server = "192.168.1.88"
port = 5555

# Tworzenie gniazda sieciowego (socket) z rodzajem AF_INET (IPv4) i typem SOCK_STREAM (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Próba powiązania gniazda z adresem IP serwera i portem
try:
    s.bind((server, port))

except socket.error as e:
    str(e)

# Nasłuchiwanie połączeń przychodzących z maksymalnie 2 klientami
s.listen(10)
print("Waiting for a connection, server Started")

positions = [(0, 0), (100, 100)]


# Definicja funkcji obsługującej klienta
def threaded_client(conn, playerNum):
    # Wysłanie informacji o nawiązaniu połączenia z klientem
    conn.send(str.encode(make_pos(positions[playerNum])))

    print(str.encode(make_pos(positions[playerNum])))
    reply = ""
    while True:
        try:
            # Odczytanie danych od klienta
            data = read_pos(conn.recv(2048).decode())
            # Dekodowanie danych do formatu utf-8
            positions[playerNum] = data

            # Sprawdzenie, czy odebrano jakieś dane
            if not data:
                print("Disconnected")
                break
            else:
                if playerNum == 1:
                    reply = positions[0]
                else:
                    reply = positions[1]

                # Wyświetlenie otrzymanych danych
                print(f"Received: {reply}")
                # Przesłanie tych samych danych z powrotem do klienta
                print(f"Sending: {reply}")

            conn.sendall(str.encode(make_pos(reply)))
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