import socket
import threading

PORT = 5051
SERVER = "192.168.69.59" # <-- my computer
# SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 128
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handleClient(conn, addr):
    clientLen = conn.recv(HEADER).decode(FORMAT)
    if not clientLen:
        name = str(addr[0])
    else:
        clientLen = int(clientLen)
        name = conn.recv(clientLen).decode(FORMAT)
        conn.send("name received".encode(FORMAT))
    print(f"[NEW CONNECTION] {name} connected.")
    connected = True
    while connected:
        msgLen = conn.recv(HEADER).decode(FORMAT)
        if msgLen:
            msgLen = int(msgLen)
            msg = conn.recv(msgLen).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                conn.send("closing connection".encode(FORMAT))
                break
            
            print(f"[{name}] {msg}")
            conn.send("msg received".encode(FORMAT))
    conn.close()
    print(f"[CLOSING CONNECTION] client {name} successfully closed")

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