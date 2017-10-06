import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 8001                    # Reserve a port for your service.

s.connect((host, port))
#s.send("Hello server!")

s.send('TMQ?')
print 'recebendo TMQ'
TMQ = s.recv(20)
print TMQ


with open('received_file', 'wb') as f:
    print 'file opened'
    while True:
        print('receiving data...')
        data = s.recv(int(TMQ))
        print('data=%s', (data))
        if not data or data == 'EOF':
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')