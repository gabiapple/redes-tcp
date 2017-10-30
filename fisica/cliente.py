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

def binToString(data_binary):
    n = int(data_binary,2)
    data_hex = binascii.unhexlify('%x' %n)
    return data_hex

# Comunicacao camada superior -> fisica -> servidor fisica
with open('log_c.txt', 'a') as g:
    g.write('Arquivo aberto [' + str(datetime.datetime.now()) + ']' + '\n')
   
    # configurando socket para ouvir camada superior 
    port_superior = 10000                  # Reserve a port for your service.
    s_superior = socket.socket()             # Create a socket object
    host = 'localhost'     # Get local machine name
       
    s_superior.bind((host, port_superior))            # Bind to the port
    s_superior.listen(5)                     # Esperando camada superior.
            
    g.write('Esperando conexao com a camada superior [' + str(datetime.datetime.now()) + ']' + '\n')
       
    # estabelece conexao com camada superior
    conn_superior, addr_superior = s_superior.accept()     # Establish connection with client.
    g.write('Estabeleceu conexao com a camada superior' + str(addr_superior) + '[' + str(datetime.datetime.now()) + ']' + '\n')
          
    msg = conn_superior.recv(10) # recebendo mensagem da camada superior
    print "msg da camada superior:" + msg
        
    # converte para binario
    msg_bin = stringToBin(msg)

    # cria Frame Ethernet
    frame = criaFrame(msg_bin)
    with open('frameEnvio.txt', 'a') as f:
        print 'file opened'
        f.write(frame)

    # configurando socket para enviar mensagem para o servidor da fisica
    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    port = 10200                     # Reserve a port for your service.

    s.connect((host, port))

    g.write('Estabelece conexao com Servidor da Fisica [' + str(datetime.datetime.now()) + ']' + '\n')

    # Pergunta TMQ

    s.send('TMQ?')
    g.write('Pergunta TMQ [' + str(datetime.datetime.now()) + ']' + '\n')
    print 'recebendo TMQ'
    TMQ = s.recv(10)
    g.write('Recebe TMQ [' + str(datetime.datetime.now()) + ']' + '\n')

    # Envia frame para servidor
    filename = 'frameEnvio.txt'
    file = open(filename,'rb')
    l = file.read(int(TMQ))
    while (l):
        s.send(l)
        g.write('Envia quadro para servidor [' + str(datetime.datetime.now()) + ']' + '\n')
        #print('Sent ',repr(l))
        l = file.read(int(TMQ))
    g.write('Arquivo enviado [' + str(datetime.datetime.now()) + ']' + '\n')
    print('Arquivo enviado')
    s.close()
    g.write('Conexao com Servidor da Fisca fechada [' + str(datetime.datetime.now()) + ']' + '\n')
    print('Conexao fechada')
#'''


# Comunica servidor fisica -> cliente fisica -> camada superior
with open('log_c.txt', 'a') as j:
    # configura socket para esperar servidor da fisica se conectar
    port = 10500                  # Reserve a port for your service.
    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    s.bind((host, port))            # Bind to the port
    s.listen(5)                     # Now wait for client connection.
    j.write('Esperando conexao [' + str(datetime.datetime.now()) + ']' + '\n')
    TMQ = '1024'


    print 'Server listening....'
    while True:
        conn, addr = s.accept()     # Establish connection with client.
        j.write('Estabeleceu conexao com servidor da fisica' + str(addr) + '[' + str(datetime.datetime.now()) + ']' + '\n')
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
        conn.close()
        j.write('Conexao encerrada [' + str(datetime.datetime.now()) + ']' + '\n\n')
        print ("Conexao encerrada do servidor se comunicando com cliente")

        j.write('Quadro recebido [' + str(datetime.datetime.now()) + ']' + '\n')
    #f.close()
        print('Recebido frame com sucesso')

        # separar frame (PREAMBULO, START_DELIMITER, MAC_ORIG, MAC_DEST)
        data = frame.split('\n')
        msg_bin = data[5]
        msg = binToString(msg_bin)
        with open('rf.txt', 'wb') as f:
            f.write(msg)
           # print msg

        # configurando socket para se comunicar com a camada superior 
        port_superior = 10000                  # Reserve a port for your service.
        s_superior = socket.socket()             # Create a socket object
        host = 'localhost'     # Get local machine name
                      
        j.write('Esperando conexao com a camada superior [' + str(datetime.datetime.now()) + ']' + '\n')
           
        # estabelece conexao com camada superior
        s_superior.connect((host, port))
        g.write('Estabelece conexao com camada superior [' + str(datetime.datetime.now()) + ']' + '\n')
  
        # envia mensagem para camada superior
        s_superior.send(msg)

        break;
j.close()
print("cliente")
