import socket
import time

def client_program():
    host = '127.0.0.1'  # as both the client and server are running on same computer
    port = 65432  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = "hello world"  # take input
    while message.lower().strip() != 'bye':
        time.sleep(1)
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print(f'[From server {host}:{port}] ' + data)  # show in terminal

        message = "hello world"  # again take input

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()