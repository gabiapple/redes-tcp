import socket                   # Import socket module
import time
import binascii
import datetime
import os
import re
import sys

from python_arptable import get_arp_table
from socket import timeout

def stringToBin(msg):
    data_binary = bin(int(binascii.hexlify(msg),16)).split('b')
    return data_binary

def binToString(data_binary):
    n = int(data_binary,2)
    data_hex = binascii.unhexlify('%x' %n)
    return data_hex

def exibePDU(pdu):
    print "Preambulo: " + str(int(pdu[0],2))
    print "Start_frame: " +  str(int(pdu[1],2))
    print "MAC ORIGEM: " +  binToString(pdu[2])
    print "MAC DESTINO: " +  binToString(pdu[3])
    print "TIPO: " +  str(int(pdu[4],2))

def calculaMAC():
    # https://github.com/LukeCSmith0/hyperspeed-tester/blob/master/Client-Script/execute_test_final.py
    os.system("ping -c 2 " + host)
    ##Import the contents of the ARP table for reading
    arp_table = get_arp_table()
    print arp_table 
    print '\n'
    ##Loop through each ARP entry to check whether the gateway address is present
    for arp_entry in arp_table:
        print arp_entry
        if arp_entry["IP address"] ==  host:
            ##Grab the MAC address associated with the gateway address
            gateway_mac = arp_entry["HW address"]
            print "here"
            break;

    return gateway_mac

def criaFrame(msg):
    print "Gerando PDU da camada fisica"
    preambulo = '10101010101010101010101010101010101010101010101010101010'
    start_frame = '10101011'
    mac_orig = stringToBin(''.join(get_arp_table()[0]['HW address'].split(':')))
    mac_dest = stringToBin(''.join(get_arp_table()[0]['HW address'].split(':')))
    tipo = '0000000011111111'
    frame = ""
    frame += preambulo + '\n' + start_frame + '\n' + mac_orig[1] + '\n' + mac_dest[1] + '\n' + tipo + '\n' + msg[1]
    exibePDU(frame.split('\n'))
    return frame

def recebeMensagem():
    filename = 'mensagem.txt'
    f = open(filename,'rb')
    msg = f.read()
    f.close()
    return msg

# recebendo ip do servidor
if len(sys.argv) != 2:
    print 'Uso: python ' + sys.argv[0] + ' [ip_servidor]'
    sys.exit()
host = sys.argv[1]     # Get local machine name

# configurando socket para se comunicar com cliente
port = 10200                 # Reserve a port for your service.
s = socket.socket()             # Create a socket object
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

while True:
    # Cliente comunica com esse servidor e esse servidor comunica com a camada superior
    j = open('log_s.txt', 'a')

    j.write('Esperando conexao [' + str(datetime.datetime.now()) + ']' + '\n')
    TMQ = '1024'

    # esperando conexoes
    print 'Server listening....'

    conn, addr = s.accept()     # Establish connection with client.
    conn.settimeout(1.5)
    j.write('Estabelece conexao com cliente da fisica [' + str(datetime.datetime.now()) + ']' + '\n')

    # Recebe Quadro Ethernet do cliente
    print 'Estabeleceu conexao com', addr
    message = conn.recv(10)
    conn.send(TMQ)
    j.write('Enviou TMQ [' + str(datetime.datetime.now()) + ']' + '\n')
    frame = ""
    while True:
        print('recebendo dados...')
        try:
            part = conn.recv(int(TMQ))
            j.write('Recebeu dados [' + str(datetime.datetime.now()) + ']' + '\n')
            frame += part
        except timeout:
            break
    j.write('Quadro recebido [' + str(datetime.datetime.now()) + ']' + '\n')
    print('Recebido frame com sucesso')

    # separar frame (PREAMBULO, START_DELIMITER, MAC_ORIG, MAC_DEST)
    data = frame.split('\n')

    # exibir PDU
    print "Processando PDU da camada Fisica"
    exibePDU(data[:5])

    msg_bin = data[5]
    msg = binToString(msg_bin)
    print msg

    # configurando socket para conversar com o servidor da camada superior
    server = socket.socket()         # Create a socket object
    host_superior = 'localhost' # Get local machine name
    port_superior = 10050                # Reserve a port for your service.
 
    # estabelecendo conexao
    server.connect((host_superior, port_superior))
    #print server.recv(1024)
    j.write('Estabeleceu conexao com servidor da camada superior: ' + str(addr) + '[' + str(datetime.datetime.now()) + ']' + '\n')
 
    # envia mensagem
    server.send(msg)
    j.write('Envia mensagem para o servidor da camada superior [' + str(datetime.datetime.now()) + ']' + '\n\n')

    # recebe resposta
    msg = server.recv(1024)
    print 'Resposta do servidor de app: ' + msg
    j.write('Recebeu resposta do servidor da camada superior [' + str(datetime.datetime.now()) + ']' + '\n\n')
    server.close()
    j.write('Conexao encerrada [' + str(datetime.datetime.now()) + ']' + '\n\n')
       
    # converte para binario
    msg_bin = stringToBin(msg)
        
    # cria Frame Ethernet
    frame = criaFrame(msg_bin)
    with open('frameEnvio.txt', 'wb') as f:
        print 'file opened'
        f.write(frame)
    j.write('Cria Frame Ethernet [' + str(datetime.datetime.now()) + ']' + '\n\n')

    # Pergunta TMQ
    conn.send('TMQ?')
    j.write('Pergunta TMQ [' + str(datetime.datetime.now()) + ']' + '\n')
    print 'recebendo TMQ'
    TMQ = conn.recv(10)
    j.write('Recebe TMQ [' + str(datetime.datetime.now()) + ']' + '\n')

    # Envia frame para servidor
    filename = 'frameEnvio.txt'
    f = open(filename,'rb')
    l = f.read(int(TMQ))
    while (l):
        conn.send(l)
        j.write('Envia quadro para servidor [' + str(datetime.datetime.now()) + ']' + '\n')
        l = f.read(int(TMQ))
    j.write('Arquivo enviado [' + str(datetime.datetime.now()) + ']' + '\n')
    conn.close()
    j.write('Conexao fechada [' + str(datetime.datetime.now()) + ']' + '\n')
    print('Conexao fechada')
   
    j.close()


    