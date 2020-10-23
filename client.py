import socket
import sys
import board as bd

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

def initializeClient():
    try:
        print('Creating socket')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('Connecting to the server')
        sock.connect((HOST, PORT))

        print('Connection sucess!')

        return sock
    except:
        print('Failed to create connection')
        sys.exit()

def initializeBoard():
    bd.initializeBoard(4)
    bd.print_board()

def get_shot(msg):
    coordinates = msg.split(',')
    print coordinates

    x = int(coordinates[0])
    y = int(coordinates[1])

    return (x, y)

def shot_ship(x, y):
    hit = bd.shot_ship(x, y)

def check_ship_destroyed(x, y):
    s_destroyed = bd.ship_destroyed(x, y)
    if s_destroyed:
        print('SHIP DESTROYED')

def format_shot(x, y):
    return str(x) + ',' + str(y)

sock = initializeClient()
board = initializeBoard()

print('Para sair use CTRL+X\n')
msg = ''
while msg <> '\x18':
    print 'Coordenada x'
    x = raw_input()    
    print 'Coordenada y'
    y = raw_input()    
    sock.send((x + ',' + y))

    response = sock.recv(1024)
    
    print(response)
    print('BOARD CLIENT')
    bd.print_board()


    shot = get_shot(response)
    hit = shot_ship(shot[0], shot[1])

    if hit:
        ship_destroyed = check_ship_destroyed(x,y)
    #sock.close()