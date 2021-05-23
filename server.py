import socket
import threading
import sys


# Server IP and port
IP = "127.0.0.1"
PORT = 55555

turn = "X"

# Socket type and options
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

# dictionary of client sockets and their nicknames
clients = {}

# debuggin
print(f"Listening for connections on {IP}:{PORT}...")


# Sending Messages To All Connected Clients
def broadcast(message, client_socket):
    # Send messages to all clients except to the original sender
    for client in clients.keys():
        if client is not client_socket:
            client.send(message.encode("utf-8"))


# Function to be called per client
def handle(client_socket):
    while True:
        message = client_socket.recv(1024).decode("utf-8")
        print(message)
        broadcast(message, client_socket)
        if "!exit" in message:
            client_socket.close()
            broadcast("{} left!".format(clients[client_socket]), client_socket)
            clients.pop(client_socket)
            print(clients)
            sys.exit()


# Receiving / Listening Function
def receive():
    global turn
    while True:
        # Accept Connection
        client_socket, address = server_socket.accept()
        print("Connected with {}".format(str(address)))
        client_socket.send(turn.encode('utf-8'))
        nickname = f'player {turn}'
        if turn == "X":
            turn = "O"
        # # Request And Store Nickname
        # client_socket.send("/id".encode("utf-8"))
        # nickname = client_socket.recv(1024).decode("utf-8")
        # Add client info to the dictionary
        clients.update({client_socket: nickname})
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client_socket,))
        thread.start()


receive()
