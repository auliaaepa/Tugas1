import socket
import select
import sys
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5002)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

BUFF_SIZE = 1024

try:
  while True:
    read_ready, write_ready, exception = select.select(input_socket, [], [])

    for sock in read_ready:
      if sock == server_socket:
        client_socket, client_address = server_socket.accept()
        print(client_socket)
        input_socket.append(client_socket)
      
      else:
        data = sock.recv(BUFF_SIZE).decode()
        print(sock.getpeername(), data)
        if data:
          command = data.split(" ")
          if command[0] == "unduh":
            file_name = command[1][:-1]
            current_path = os.getcwd()
            file_path = os.path.join(current_path, "dataset", file_name)
            # print(file_path)

            if not os.path.exists(file_path):
              sock.send("file-doesn't-exist".encode())
            else:
              sock.send("file-exist".encode())
              print('sending', file_name)
              if data != '':
                with open(file_path, 'rb') as file:
                  data = file.read(BUFF_SIZE)
                  while data:
                    sock.send(data)
                    data = file.read(BUFF_SIZE)
                
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                input_socket.remove(sock)
          else:
            sock.send("command-is-not-valid".encode())
        else:
          sock.shutdown(socket.SHUT_RDWR)
          sock.close()
          input_socket.remove(sock)

except KeyboardInterrupt:
  server_socket.close()
  sys.exit(0)