import socket
import select
import sys
import os

# define buffer size
BUF_SIZE = 1024

# initialize socket object with AF_INET as address family and SOCK_STREAM as socket type
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# validating address passed to bind() must allow reuse of local address
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind to the given address
HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
server_address = (HOST, PORT)
server_socket.bind(server_address)

# accept connections from max 5 clients at the same time
server_socket.listen(5)

# list to store accepted client
input_socket = [server_socket]

try:
    while True:
        # get read, write, and exception list from select
        read_list, write_list, exception_list = select.select(input_socket, [], [])
        
        for sock in read_list:
            # accept client and add it to the accepted client list
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                print("Accepted client:", client_address)
            # handle receiving message and sending file
            else:
                try:
                    # receive message from client
                    message = sock.recv(BUF_SIZE).decode("utf-8")

                    if message:
                        # get command
                        splitted_message = message.split()
                        command = splitted_message[0]

                        if command == "unduh":
                            if len(splitted_message) != 2: 
                                error_msg = "Unknown argument\n"
                                sock.send(error_msg.encode("utf-8"))
                                print("Send to client :", sock.getpeername(), error_msg.encode("utf-8"))
                                continue
                            
                            # get filename and filepath
                            filename = splitted_message[1]
                            filepath = os.path.join(os.getcwd(), "dataset", filename)

                            # if requested file exist in dataset
                            if os.path.exists(filepath):
                                success_msg = "Start sending file...\n"
                                sock.send(success_msg.encode("utf-8"))
                                print("Send to client :", sock.getpeername(), success_msg.encode("utf-8"))

                                # create header message
                                filesize = os.path.getsize(filepath)
                                header = filename + ",\n" + str(filesize) + ",\n"
                                header = header.encode("utf-8")

                                # send file content
                                with open(filepath, 'rb') as file:
                                    send_size = 0
                                    while send_size < filesize:
                                        content = file.read(BUF_SIZE-len(header))
                                        send_file = header + content
                                        sock.send(send_file)
                                        send_size += len(content)
                                        print("Send to client :", sock.getpeername(), filename, "[{:>6.2f}%]".format(send_size*100/filesize))
                            else:
                                error_msg = "File not found\n"
                                sock.send(error_msg.encode("utf-8"))
                                print("Send to client :", sock.getpeername(), error_msg.encode("utf-8"))
                        else:
                            error_msg = "Unknown command\n"
                            sock.send(error_msg.encode("utf-8"))
                            print("Send to client :", sock.getpeername(), error_msg.encode("utf-8"))
                    # client close connection
                    else:
                        print("Closed client:", sock.getpeername())
                        sock.close()
                        input_socket.remove(sock)                        
                
                except IndexError:
                    error_msg = "Unknown command\n"
                    sock.send(error_msg.encode("utf-8"))
                    print("Send to client :", sock.getpeername(), error_msg.encode("utf-8"))

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)