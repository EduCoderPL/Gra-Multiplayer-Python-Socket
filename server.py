import socket
from _thread import *
import sys

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


# Definicja funkcji obsługującej klienta
def threaded_client(conn):
    # Wysłanie informacji o nawiązaniu połączenia z klientem
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            # Odczytanie danych od klienta
            data = conn.recv(2048)
            # Dekodowanie danych do formatu utf-8
            reply = data.decode("utf-8")

            # Sprawdzenie, czy odebrano jakieś dane
            if not data:
                print("Disconnected")
                break
            else:
                # Wyświetlenie otrzymanych danych
                print(f"Received: {reply}")
                # Przesłanie tych samych danych z powrotem do klienta
                print(f"Sending: {reply}")

            conn.sendall(str.encode(reply))
        except:
            break
    # Wyświetlenie komunikatu o utraceniu połączenia z klientem i zamknięcie połączenia

    print("Lost connection")
    conn.close()


# Nieskończona pętla while, w której serwer przyjmuje nowych klientów i tworzy dla nich nowe wątki
while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}.")

    start_new_thread(threaded_client, (conn,))