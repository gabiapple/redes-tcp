import socket                   # Import socket module
import os
import binascii
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
    frame += preambulo + '|' + start_frame + '|' + mac_orig[1] + '|' + mac_dest[1] + '|' + tipo + '|' + msg[1]
    return frame

def recebeMensagem():
    filename = 'mensagem.txt'
    f = open(filename,'rb')
    msg = f.read()
    f.close()
    return msg


msg = recebeMensagem()

# converte para binario
msg_bin = stringToBin(msg)

# cria Frame Ethernet
frame = criaFrame(msg_bin)

with open('frameEnvio.txt', 'wb') as f:
    print 'file opened'
    f.write(frame)

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 8795                   # Reserve a port for your service.

s.connect((host, port))

# Pergunta TMQ
s.send('TMQ?')
print 'recebendo TMQ'
TMQ = s.recv(10)
print TMQ

# Envia frame para servidor
filename = 'frameEnvio.txt'
f = open(filename,'rb')
l = f.read(int(TMQ))
while (l):
    s.send(l)
    #print('Sent ',repr(l))
    l = f.read(int(TMQ))

print('Arquivo enviado')
s.close()
print('Conexao fechada')
