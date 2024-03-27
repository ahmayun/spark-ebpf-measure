import socket
import sys

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enable SO_REUSEADDR option
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Now you can bind the socket to an address, even if that address was recently used
sock.bind((sys.argv[1], sys.argv[2]))
