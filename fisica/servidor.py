import socket                   # Import socket module
import time
import binascii
import datetime
import os
from python_arptable import *

def stringToBin(msg):
    data_binary = bin(int(binascii.hexlify(msg),16)).split('b')
    return data_binary

def criaFrame(msg):
    preambulo = '10101010101010101010101010101010101010101010101010101010'
    start_frame = '10101011'
    mac_orig = stringToBin(''.join(get_arp_table()[0]['HW address'].split(':')))
    mac_dest = stringToBin(''.join(get_arp_table()[0]['HW address'].split(':')))
    tipo = '0000000011111111'
    frame = ""
    frame += preambulo + '\n' + start_frame + '\n' + mac_orig[1] + '\n' + mac_dest[1] + '\n' + tipo + '\n' + msg[1]
    return frame

def recebeMensagem():
    filename = 'mensagem.txt'
    f = open(filename,'rb')
    msg = f.read()
    f.close()
    return msg


def binToString(data_binary):
    n = int(data_binary,2)
    data_hex = binascii.unhexlify('%x' %n)
    return data_hex

while True:
    # Cliente comunica com esse servidor e esse servidor comunica com a camada superior
    with open('log_s.txt', 'a') as j:

        port = 10200                 # Reserve a port for your service.
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
            j.write('Estabeleceu conexao com cliente Fisica: ' + str(addr) + '[' + str(datetime.datetime.now()) + ']' + '\n')
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
            op = False
            print 'saiur'
            server = socket.socket()         # Create a socket object
            host = socket.gethostname() # Get local machine name
            port = 10006                # Reserve a port for your service.
         
            # estabelecendo conexao
            server.connect((host, port))
            #print server.recv(1024)
            j.write('Estabeleceu conexao com servidor da camada superior: ' + str(addr) + '[' + str(datetime.datetime.now()) + ']' + '\n')
         
            # envia mensagem
            server.send(msg)
            server.close()

    j.close()

    time.sleep(1)

    # Eesse servidor se comunica com o cliente
    with open('log_s.txt', 'a') as g:     
        server = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 10006                # Reserve a port for your service.
         
        # estabelecendo conexao
        server.connect((host, port))
        #print server.recv(1024)
        g.write('Estabeleceu conexao com servidor da camada superior: ' + str(addr) + '[' + str(datetime.datetime.now()) + ']' + '\n')
        print 'i am here'
        # recebe resposta
      #  with open('mensagem.txt', 'w') as f:
        msg = server.recv(1024)
       #     f.close()
       # server.close
            
        # converte para binario
        msg_bin = stringToBin(msg)
            
        # cria Frame Ethernet
        frame = criaFrame(msg_bin)
        with open('frameEnvio.txt', 'wb') as f:
            print 'file opened'
            f.write(frame)

        # configura socket para comunicar com cliente da fisica
        s = socket.socket()             # Create a socket object
        host = socket.gethostname()     # Get local machine name
        port = 10500                     # Reserve a port for your service.

        s.connect((host, port))
        g.write('Estabelece conexao com cliente da fisica [' + str(datetime.datetime.now()) + ']' + '\n')

        # Pergunta TMQ

        s.send('TMQ?')
        g.write('Pergunta TMQ [' + str(datetime.datetime.now()) + ']' + '\n')
        print 'recebendo TMQ'
        TMQ = s.recv(10)
        g.write('Recebe TMQ [' + str(datetime.datetime.now()) + ']' + '\n')

        # Envia frame para servidor
        filename = 'frameEnvio.txt'
        f = open(filename,'rb')
        l = f.read(int(TMQ))
        while (l):
            s.send(l)
            g.write('Envia quadro para servidor [' + str(datetime.datetime.now()) + ']' + '\n')
            #print('Sent ',repr(l))
            l = f.read(int(TMQ))
        g.write('Arquivo enviado [' + str(datetime.datetime.now()) + ']' + '\n')
        s.close()
        g.write('Conexao fechada [' + str(datetime.datetime.now()) + ']' + '\n')
        print('Conexao fechada')
