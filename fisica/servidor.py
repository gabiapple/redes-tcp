import socket                   # Import socket module
import time
import binascii
from python_arptable import *

def binToString(data_binary):
    n = int(data_binary,2)
    data_hex = binascii.unhexlify('%x' %n)
    return data_hex


port = 8795                   # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.
TMQ = '1024'


print 'Server listening....'

while True:
    conn, addr = s.accept()     # Establish connection with client.
  
    # simulando envio de Quadro Ethernet (como se fosse da camada superior)
    print 'Estabeleceu conexao com', addr
    message = conn.recv(10)
    conn.send(TMQ)
    
    frame = ""
    while True:
        print('recebendo dados...')
        part = conn.recv(int(TMQ))
        frame += part
       # print('part=%s', (part))
        if not part or part == '':
            break
        # write data to a file
        #f.write(data)

#f.close()
    print('Recebido frame com sucesso')

    # separar frame (PREAMBULO, START_DELIMITER, MAC_ORIG, MAC_DEST)
    data = frame.split('|')
    msg_bin = data[5]
    msg = binToString(msg_bin)
    print msg

    conn.close()


