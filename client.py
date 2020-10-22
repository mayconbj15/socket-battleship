import socket
import numpy as np

board = np.zeros((10,10))

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

'''
    try:
        print('Creating socket')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('Connecting to the server')
        sock.connect((HOST, PORT))

        print('Connection sucess!')
    except:
        print('Failed to create connection')
'''

print board
print type(board)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print('Para sair use CTRL+X\n')
msg = ''
while msg <> '\x18':
    print 'Coordenada x'
    x = raw_input()    
    #print 'Coordenada y'
    #y = raw_input()    
    #tcp.send(x + ',' + y)
    tcp.send(x)

    response = tcp.recv(1024)
    print(response)
    #tcp.close()