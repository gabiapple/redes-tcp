import socket                   # Import socket module
import os
import binascii
import datetime
import sys
from python_arptable import *
import fcntl, struct

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
    print "MAC ORIGEM: " +  pdu[2]
    print "MAC DESTINO: " +  pdu[3]
    print "TIPO: " +  str(int(pdu[4],2))

# Referencias consultadas para achar MAC_ADRESS:
# https://github.com/LukeCSmith0/hyperspeed-tester/blob/master/Client-Script/execute_test_final.py
# https://stackoverflow.com/questions/159137/getting-mac-address
def calculaMAC(ip):
    if ip == 'localhost':
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', interface[:15]))
        gateway_mac = ':'.join(['%02x' % ord(char) for char in info[18:24]])
        return gateway_mac
   
    os.system("ping -c 2 " + ip)
    ##Import the contents of the ARP table for reading
    arp_table = get_arp_table()
    gateway_mac = '0'
    ##Loop through each ARP entry to check whether the gateway address is present
    for arp_entry in arp_table:
        if arp_entry['IP address'] ==  str(ip):
            ##Grab the MAC address associated with the gateway address
            gateway_mac = str(arp_entry['HW address'])
            print gateway_mac
            break;

    return gateway_mac

def criaFrame(msg):
    print "Gerando PDU da camada fisica"
    preambulo = '10101010101010101010101010101010101010101010101010101010'
    start_frame = '10101011'
    mac_orig = calculaMAC('localhost') # MAC do cliente
    mac_dest = calculaMAC(ip_servidor) # MAC do servidor
    tipo = '0000000011111111'
    frame = ""
    frame += preambulo + '\n' + start_frame + '\n' + mac_orig + '\n' + mac_dest + '\n' + tipo + '\n' + msg[1]
    exibePDU(frame.split('\n'))
    return frame

def recebeMensagem():
    filename = 'mensagem.txt'
    f = open(filename,'rb')
    msg = f.read()
    f.close()
    return msg

# recebendo ip do servidor
if len(sys.argv) != 4:
    print 'Uso: python ' + sys.argv[0] + ' [interface] [ip_servidor] [ip_cliente]'
    sys.exit()

interface = sys.argv[1]
ip_servidor = sys.argv[2]
host = sys.argv[3]     # Get local machine name

# configurando socket para ouvir camada superior 
port_superior = 10001                  # Reserve a port for your service.
s_superior = socket.socket()             # Create a socket object
host_superior = 'localhost'     # Get local machine name
s_superior.bind(('localhost', port_superior))            # Bind to the port
s_superior.listen(5)                     # Escutando camada superior.

while True:
    # Comunicacao camada superior -> fisica -> servidor fisica
    g = open('log_c.txt', 'a')
 #   g.write('Arquivo aberto [' + str(datetime.datetime.now()) + ']' + '\n')
   
    g.write('Esperando conexao com a camada superior [' + str(datetime.datetime.now()) + ']' + '\n')
       
    # estabelece conexao com camada superior
    conn_superior, addr_superior = s_superior.accept()     # Establish connection with client.
    g.write('Estabeleceu conexao com a camada superior ' + str(addr_superior) + '[' + str(datetime.datetime.now()) + ']' + '\n')
          
    msg = conn_superior.recv(40) # recebendo mensagem da camada superior
    g.write('Recebeu mensagem da camada superior [' + str(datetime.datetime.now()) + ']' + '\n')
            
        
    # converte para binario
    msg_bin = stringToBin(msg)

    # cria Frame Ethernet
    frame = criaFrame(msg_bin)
    with open('frameEnvio1.txt', 'w') as f:
        print 'file opened'
        f.write(frame)
        f.write('')
    f.close()

    # configurando socket para enviar mensagem para o servidor da fisica
    s = socket.socket()             # Create a socket object
    port = 10200                     # Reserve a port for your service.

    s.connect((ip_servidor, port))

    g.write('Estabelece conexao com Servidor da Fisica [' + str(datetime.datetime.now()) + ']' + '\n')

    # Pergunta TMQ
    s.send('TMQ?')
    g.write('Pergunta TMQ [' + str(datetime.datetime.now()) + ']' + '\n')
    print 'recebendo TMQ'
    TMQ = s.recv(10)
    g.write('Recebe TMQ [' + str(datetime.datetime.now()) + ']' + '\n')

    # Envia frame para servidor
    filename = 'frameEnvio1.txt'
    file = open(filename,'rb')
    l = file.read(int(TMQ))
    while (l):
        s.send(l)
        g.write('Envia quadro para servidor [' + str(datetime.datetime.now()) + ']' + '\n')
        #print('Sent ',repr(l))
        l = file.read(int(TMQ))
    g.write('Arquivo enviado [' + str(datetime.datetime.now()) + ']' + '\n')
    print('Arquivo enviado')

    # Envia TMQ para servidor da fisica
    message = s.recv(10)
    s.send(TMQ)
    g.write('Enviou TMQ [' + str(datetime.datetime.now()) + ']' + '\n')
    frame = ""
    
    # Recebendo resposta do servidor
    while True:
        print('recebendo dados...')
        part = s.recv(int(TMQ))
        g.write('Recebeu dados [' + str(datetime.datetime.now()) + ']' + '\n')
        frame += part
        if not part or part == '':
            break
    g.write('Quadro recebido [' + str(datetime.datetime.now()) + ']' + '\n')
    print('Recebido frame com sucesso')

    s.close()
    g.write('Conexao com Servidor da Fisica encerrada [' + str(datetime.datetime.now()) + ']' + '\n\n')
    print ("Conexao encerrada do servidor se comunicando com cliente")

   
    # separar frame (PREAMBULO, START_DELIMITER, MAC_ORIG, MAC_DEST)
    data = frame.split('\n')

    # exibir PDU
    print "Processando PDU da camada Fisica"
    exibePDU(data[:5])

    msg_bin = data[5]
    msg = binToString(msg_bin)
    with open('rf.txt', 'wb') as f:
        f.write(msg)
       # print msg

    # envia mensagem para camada superior
    conn_superior.send(msg)

    g.close()
    
