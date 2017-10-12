import socket                   # Import socket module
import time
import binascii
import datetime
import os
from python_arptable import *

def binToString(data_binary):
    n = int(data_binary,2)
    data_hex = binascii.unhexlify('%x' %n)
    return data_hex

with open('log_s.txt', 'w') as j:
    port = 8520                  # Reserve a port for your service.
    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    s.bind((host, port))            # Bind to the port
    s.listen(5)                     # Now wait for client connection.
    j.write('Esperando conexao [' + str(datetime.datetime.now()) + ']' + '\n')
    TMQ = '1024'


    print 'Server listening....'
    op = True
    while op == True:
        conn, addr = s.accept()     # Establish connection with client.
        j.write('Estabeleceu conexao com ' + str(addr) + '[' + str(datetime.datetime.now()) + ']' + '\n')
        # simulando envio de Quadro Ethernet (como se fosse da camada superior)
        print 'Estabeleceu conexao com', addr
        message = conn.recv(10)
        conn.send(TMQ)
        j.write('Enviou TMQ [' + str(datetime.datetime.now()) + ']' + '\n')
        frame = ""
        while True:
            print('recebendo dados...')
            part = conn.recv(int(TMQ))
            j.write('Recebeu dados [' + str(datetime.datetime.now()) + ']' + '\n')
            frame += part
           # print('part=%s', (part))
            if not part or part == '':
                break
            # write data to a file
            #f.write(data)
        j.write('Quadro recebido [' + str(datetime.datetime.now()) + ']' + '\n')
    #f.close()
        print('Recebido frame com sucesso')

        # separar frame (PREAMBULO, START_DELIMITER, MAC_ORIG, MAC_DEST)
        data = frame.split('\n')
        msg_bin = data[5]
        msg = binToString(msg_bin)
        with open('rf.txt', 'wb') as f:
            f.write(msg)
            print msg

        conn.close()
        j.write('Conexao encerrada [' + str(datetime.datetime.now()) + ']' + '\n\n')
        #print('Servidor aguardando solicitacao pressione q para sair ou qualquer tecla para continuar:')
        #c = raw_input()
        #if c == 'q':
        #    op = False
j.close()
