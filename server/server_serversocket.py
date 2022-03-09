import os 
import threading 
import socketserver 
import sys

# define buffer size, encoding format, and separator for header message
BUF_SIZE = 1024
FORMAT = "utf-8"
SEPARATOR = ",\n"

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler): 
    def handle(self):
        print(threading.current_thread().name, "Accepted client:", self.request.getpeername())
        while True:
            try:
                # receive message from client
                message = self.request.recv(BUF_SIZE).decode(FORMAT)
                if message:
                    # get command
                    splitted_message = message.split()
                    command = splitted_message[0]

                    if command == "unduh":
                        if len(splitted_message) != 2: 
                            error_msg = "Unknown argument\n"
                            self.request.send(error_msg.encode(FORMAT))
                            print(threading.current_thread().name, "Send to client :", self.request.getpeername(), error_msg.encode(FORMAT))
                            continue
                        
                        # get filename and filepath
                        filename = splitted_message[1]
                        filepath = os.path.join(os.getcwd(), "dataset", filename)

                        # if requested file exist in dataset
                        if os.path.exists(filepath):
                            success_msg = "Start sending file...\n"
                            self.request.send(success_msg.encode(FORMAT))
                            print(threading.current_thread().name, "Send to client :", self.request.getpeername(), success_msg.encode(FORMAT))
                            
                            # create header message
                            filesize = os.path.getsize(filepath)
                            header = (filename + SEPARATOR + str(filesize) + SEPARATOR).encode(FORMAT)
                            
                            # send file content
                            with open(filepath, 'rb') as file:
                                send_size = 0
                                while send_size < filesize:
                                    content = file.read(BUF_SIZE-len(header))
                                    send_file = header + content
                                    self.request.send(send_file)
                                    send_size += len(content)
                                    print(threading.current_thread().name, "Send to client :", self.request.getpeername(), filename, "[{:>6.2f}%]".format(send_size*100/filesize))
                        else:
                            error_msg = "File not found\n"
                            self.request.send(error_msg.encode(FORMAT))
                            print(threading.current_thread().name, "Send to client :", self.request.getpeername(), error_msg.encode(FORMAT))
                    else:
                        error_msg = "Unknown command\n"
                        self.request.send(error_msg.encode(FORMAT))
                        print(threading.current_thread().name, "Send to client :", self.request.getpeername(), error_msg.encode(FORMAT))
                # client close connection
                else:
                    print(threading.current_thread().name, "Closed client  :", self.request.getpeername())
                    self.request.close()
                    break
            
            except IndexError:
                error_msg = "Unknown command\n"
                self.request.send(error_msg.encode(FORMAT))
                print(threading.current_thread().name, "Send to client :", self.request.getpeername(), error_msg.encode(FORMAT))            

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Nothing to add here, inherited everything necessary from parents"""
    pass

if __name__ == "__main__":
    # set server address from the given address
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    server_address = (HOST, PORT)

    # initialize socket server
    socket_server = ThreadedTCPServer(server_address, ThreadedTCPRequestHandler)

    try: 
        # start a thread with the socket server - will create one thread for each request
        server_thread = threading.Thread(target=socket_server.serve_forever)
        # server_thread.daemon = False
        server_thread.start()
        print(server_thread.name, "Server bind to :", socket_server.server_address)

        # socket_server.serve_forever()

    except KeyboardInterrupt:
        # socket_server.shutdown()
        socket_server.server_close()
        sys.exit(0)