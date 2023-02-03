import socket
import threading

def send_to_socket(sock: socket.socket, message: str):
    sock.sendall(message.encode(encoding='utf8'))

def receive_from_socket(sock: socket.socket):
    return sock.recv(1024).decode(encoding='utf8')

def send_message(sock: socket.socket):
    while True:
        message = input()
        send_to_socket(sock, message)

def receive_message(sock: socket.socket):
    while True:
        message = receive_from_socket(sock)
        print(message)

def main():
    sock = socket.socket()
    addr = ('127.0.0.1', 55555)
    sock.connect(addr)

    name = input('Enter your name: ')
    send_to_socket(sock, name)

    send_thread = threading.Thread(target=send_message, args=[sock])
    receive_thread = threading.Thread(target=receive_message, args=[sock])
    send_thread.start()
    receive_thread.start()

main()