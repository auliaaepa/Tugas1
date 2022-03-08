import socket
import sys
import re

# define buffer size
BUF_SIZE = 1024

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
        # request to server
        message = sys.stdin.readline()
        client_socket.send(bytes(message, 'utf-8'))

        # receive response from server
        received_msg = client_socket.recv(BUF_SIZE).decode('utf-8')
        sys.stdout.write(received_msg)
        # download file if command correct
        if received_msg == "Start sending file...\n":
            # extract header(file name and file size) and content from message
            received_file = client_socket.recv(BUF_SIZE)
            extract = received_file.split(b",\n", 2)
            file_name, file_size, content = extract[0].decode('utf-8'), int(extract[1].decode('utf-8')), extract[2]
            new_file_name = "from_server_" + file_name

            # get file content
            with open(new_file_name, "wb") as file:
                file.write(content)
                content_size = len(content)
                sys.stdout.write(">> {:>6.2f}%\n".format(content_size*100/file_size))
                # loop until get full file content
                while content_size < file_size:                    
                    received_file = client_socket.recv(BUF_SIZE)
                    extract = received_file.split(b",\n", 2)
                    content = extract[2]
                    file.write(content)
                    content_size += len(content)
                    sys.stdout.write(">> {:>6.2f}%\n".format(content_size*100/file_size))

            sys.stdout.write(">> " + file_name + " successfully downloaded.\n")
            sys.stdout.write(">> file saved as " + new_file_name + "\n")
        sys.stdout.write(">> ")

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)