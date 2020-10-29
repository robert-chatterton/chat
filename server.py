import socket
import threading

PORT = 5051
# SERVER = "50.237.25.142" # <-- my computer
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 128
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msgLen = conn.recv(HEADER).decode(FORMAT)
        if msgLen:
            msgLen = int(msgLen)
            msg = conn.recv(msgLen).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                break
            
            print(f"[{addr}] {msg}")
            conn.send("msg received".encode(FORMAT))
    conn.close()
    print(f"[CLOSING CONNECTION] client at {addr[0]} successfully closed")

def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()