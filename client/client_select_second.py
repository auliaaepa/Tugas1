import socket
import sys
import os

server_address = ('localhost', 5002)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
  while True:
    message = sys.stdin.readline()
    client_socket.send(bytes(message, 'utf-8'))
    confirmation = client_socket.recv(1024).decode('utf-8')
    if confirmation == "file-doesn't-exist":
      print("File doesn't exist on server.")

      client_socket.shutdown(socket.SHUT_RDWR)
      client_socket.close()

      client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client_socket.connect(server_address)
    else:
      command = message.split(" ")
      filename = command[1][:-1]
      write_name = 'from_server_'+ filename
      if os.path.exists(write_name):
        os.remove(write_name)
      
      with open(write_name,'wb') as file:
        while True:
          data = client_socket.recv(1024)
          if not data:
            break
          file.write(data)
      print('>> ' + filename + ' successfully downloaded.')
      client_socket.shutdown(socket.SHUT_RDWR)
      client_socket.close()

      client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client_socket.connect(server_address)
      sys.stdout.write('>> ')

except KeyboardInterrupt:
  client_socket.close()
  sys.exit(0)