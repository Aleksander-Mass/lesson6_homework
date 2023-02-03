import socket
import threading

class Client:
    def __init__(self, sock: socket.socket, addr):
        self.sock = sock
        self.addr = addr
        self.name = ''

def send_to_socket(sock: socket.socket, message: str):
    sock.sendall(message.encode(encoding='utf8'))

def receive_from_socket(sock: socket.socket):
    data = sock.recv(1024)
    if data:
        return data.decode(encoding='utf8')

def clientthread(client: Client, clients: list[Client]):
    client.name = receive_from_socket(client.sock)
    send_to_socket(client.sock, f'{client.name}, welcome to this chatroom!')
 
    while True:
            try:
                message = receive_from_socket(client.sock)
                if message:
                    formatted_message = "<" + client.name + "> " + message
                    print(formatted_message)
                    broadcast(client, clients, formatted_message)
 
                else:
                    remove(client, clients)
            except:
                continue

def broadcast(client: Client, clients: list[Client], message: str):
    for other_client in clients:
        if other_client != client:
            try:
                send_to_socket(other_client.sock, message)
            except:
                other_client.sock.close()
                remove(other_client, clients)

def remove(client: Client, clients: list[Client]):
    if client in clients:
        clients.remove(client)

def main():
    server_addr = ('127.0.0.1', 55555)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.listen(100)

    print(f'Server started at {server_addr}')

    clients = list[Client]()
    
    while True:
        client_sock, client_addr = server.accept()
        client = Client(client_sock, client_addr)
        clients.append(client)
        print(f'New client connected at {client.addr}')

        client_thread = threading.Thread(target=clientthread, args=[client, clients])
        client_thread.start()

main()