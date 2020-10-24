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
    bd.initializeBoard(1)
    bd.print_board()

def get_shot(msg):
    coordinates = msg.split(',')
    print(coordinates)

    x = int(coordinates[0])
    y = int(coordinates[1])

    return (x, y)

def format_shot(x, y):
    return str(x) + ',' + str(y)

sock = initializeClient()
initializeBoard()

print('Para sair use CTRL+X\n')
msg = ''
while msg != '\x18':
    print('Coordenada x')
    x = input()    
    print('Coordenada y') 
    y = input()
    
    data = str(x) + ',' + str(y)    
    sock.send(data.encode())

    response = sock.recv(1024).decode("utf-8")
    
    print(response)
    print('BOARD CLIENT')
    bd.print_board()

    print('response')
    print(response)
    shot = get_shot(response)
    hit = bd.shot_ship(shot[0], shot[1])

    if hit:
        ship_destroyed = bd.check_ship_destroyed(shot)

        if ship_destroyed:
            print('SHIPT DESTROYED')
            end_game = bd.check_end_game()
            if end_game:
                print('END OF GAME')
                sock.close()