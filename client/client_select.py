import socket
import sys
import os

# define buffer size
BUF_SIZE = 4096

# initialize socket object with AF_INET as address family and SOCK_STREAM as socket type
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the given address
HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
server_address = (HOST, PORT)
client_socket.connect(server_address)

sys.stdout.write(">> ")

try:
    while True:
        message = sys.stdin.readline()
        client_socket.send(bytes(message, 'utf-8'))

        received_msg = client_socket.recv(1024).decode('utf-8')
        sys.stdout.write(received_msg)
        if received_msg == "Start sending file...":
            file_name = client_socket.recv(1024).decode('utf-8')
            file_size = int(client_socket.recv(1024).decode('utf-8'))
            with open(file_name, "wb") as file:
                received_size = 0
                while received_size < file_size:
                    received_file = client_socket.recv(BUF_SIZE)
                    received_size += BUF_SIZE
                    file.write(received_file)
                file.close()
            sys.stdout.write(" " + file_name + " received\n")
        sys.stdout.write(">> ")

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)