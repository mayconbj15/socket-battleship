import sys
import socket
import random as rand
import numpy as np 
import board as bd


HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

def initializeBoard():
    bd.initializeBoard(4)
    bd.print_board()

def initializeServer():
    try:
        print('Starting server')
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (HOST, PORT)
        tcp.bind(orig)
        tcp.listen(1)
        print('Server connected')

        return tcp
    except:
        print('Connection failed')
        sys.exit()

def get_shot(msg):
    coordinates = msg.split(',')
    print coordinates

    x = int(coordinates[0])
    y = int(coordinates[1])

    return (x, y)
    
def shot_ship(x, y):
    return bd.shot_ship(x, y)

def check_ship_destroyed(x, y):
    s_destroyed = bd.ship_destroyed(x, y)
    if s_destroyed:
        print('SHIP DESTROYED')

def make_shot(random_shot, actual_shot=(0,0)):
    if random_shot:
        x = rand.randint(0,9)
        y = rand.randint(0,9)
        return format_shot(x, y)
    else:
        orientation = rand.randint(0,3)
        if orientation == 1:
            new_shot = make_new_shot(x, y + 1)    
        elif orientation == 2:
            new_shot = make_new_shot(x + 1, y)
        elif orientation == 3:
            new_shot = make_new_shot(x, y - 1)
        else:
            new_shot = make_new_shot(x - 1, y)
        
        return format_shot(x, y)

def make_new_shot(x, y):
    if bd.valid_point(x,y):
        return (x,y)

def format_shot(x, y):
    return str(x) + ',' + str(y)

tcp = initializeServer()
board = initializeBoard()

while True:
    con, cliente = tcp.accept()
    print 'Conectado por', cliente
    while True:
        msg = con.recv(1024)
        if not msg: 
            break
        
        shot = get_shot(msg)
        
        hit = shot_ship(shot[0], shot[1])
        
        if hit:
            ship_destroyed = check_ship_destroyed(shot[0], shot[1])
            if ship_destroyed:
                shot = make_shot(False, shot)    
            else:
                shot = make_shot(True)
        else:
            shot = make_shot(True)

        print('BOARD SERVER')
        bd.print_board()
        print cliente, msg
        print con
        con.sendall(shot)
    
    print 'Finalizando conexao do cliente', cliente
    con.close()