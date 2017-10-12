import socket                   # Import socket module
import os
import binascii
import datetime
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

with open('log_c.txt', 'wb') as g:
    msg = recebeMensagem()
    g.write('Arquivo aberto [' + str(datetime.datetime.now()) + ']' + '\n')
    # converte para binario
    msg_bin = stringToBin(msg)

    # cria Frame Ethernet
    frame = criaFrame(msg_bin)
    with open('frameEnvio.txt', 'wb') as f:
        print 'file opened'
        f.write(frame)

    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    port = 8520                     # Reserve a port for your service.

    s.connect((host, port))
    g.write('Estabelece conexao [' + str(datetime.datetime.now()) + ']' + '\n')

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
    print('Arquivo enviado')
    s.close()
    g.write('Conexao fechada [' + str(datetime.datetime.now()) + ']' + '\n')
    print('Conexao fechada')
