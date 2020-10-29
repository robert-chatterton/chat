import socket

PORT = 5051
HEADER = 128
SERVER = "192.168.56.1"
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)
COMMANDS = ["help", "exit", "send"]

def send(client, msg):
    message = msg.encode(FORMAT)
    msgLen = len(message)
    sendLen = str(msgLen).encode(FORMAT)
    sendLen += b' ' * (HEADER - len(sendLen))
    client.send(sendLen)
    client.send(message)
    # '2048' is just a placeholder for the overall 
    serverMsg = client.recv(2048).decode(FORMAT)
    if not serverMsg:
        print("[CONNECTION STATUS] did not receive receipt from server")

def main():
    print("[STARTING] client starting...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[CONNECTING] attempting to connect to server at {SERVER}")
    client.connect(ADDR)
    print(f"[CONNECTION STATUS] connected to {SERVER}.")
    helpMsg()
    connected = True
    while connected:
        string = input("[INPUT] enter a command: ")
        commands = string.lower().split()
        if not commands[0] in COMMANDS:
            print(f"[ERROR] command not found: \"{commands[0]}\"")
        # help command
        if commands[0] == COMMANDS[0]:
            helpMsg()
            continue
        # disconnect command
        if commands[0] == COMMANDS[1]:
            send(client, DISCONNECT_MESSAGE)
            connected = False
            continue
        # send command
        if commands[0] == COMMANDS[2]:
            if len(commands) > 1:
                send(client, ' '.join(commands[1:]))
            else:
                send(client, "user sent blank message")
            continue
    input("[CLOSING] client closing, ENTER to leave...")
    
def helpMsg():
    print("[HELP] all possible commands:")
    print("[HELP] \"help\" to show all commands")
    print("[HELP] \"exit\" to disconnect from the server")
    print("[HELP] \"send <message>\" to send a message to the server")

main()