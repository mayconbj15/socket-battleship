import socket
import numpy as np 

board = np.zeros((10,10))

print board

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
while True:
    con, cliente = tcp.accept()
    print 'Conectado por', cliente
    while True:
        msg = con.recv(1024)
        if not msg: 
            break
        
        coordinates = msg.split(',')
        #print type(msg)
        #print coordinates
        #board[coordinates[0], coordinates[1]] = 1
        #print board
        print cliente, msg
        print con
        con.sendall('RESPOSTA')
    
    print 'Finalizando conexao do cliente', cliente
    con.close()