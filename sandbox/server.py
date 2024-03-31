import socket
import time

def server_program():
    # get the hostname
    host = '127.0.0.1'
    port = 65432  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print(f"[From user {address[0]}:{address[1]}] " + str(data))
        data = 'hello from server!'
        time.sleep(1)
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()
