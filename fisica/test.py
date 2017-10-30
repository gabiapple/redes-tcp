import binascii
from python_arptable import *



filename = 'mensagem.txt'
f = open(filename,'rb')
msg = f.read()
f.close()
print msg
data_binary = bin(int(binascii.hexlify(msg),16)).split('b')[1]
print data_binary
n = int(data_binary,2)
print n
data_hex = binascii.unhexlify('%x' %n)
print data_hex


