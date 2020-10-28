import sys
import socket
import argparse
import random as rand
import numpy as np
import board as bd


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Battleship tcp socket')

    parser.add_argument("-d", "--debug", dest="debug", default="n",
                        choices=['y', 'n'], help="Run in debug mode that print board of server")
    parser.add_argument("-i", "--host", dest="host", default="",
                        help="The host of server")
    parser.add_argument("-p", "--port", dest="port", default=5000,
                        help="The port of server")

    global args
    args = parser.parse_args()


def initializeBoard():
    bd.initializeBoard(1)
    bd.print_board()


def initializeServer():
    get_arguments()
    try:
        print('Starting server')
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (args.host, args.port)
        tcp_sock.bind(orig)
        tcp_sock.listen(1)
        print('Server connected')

        return tcp_sock
    except:
        print('Connection failed')
        sys.exit()


def get_shot(msg):
    coordinates = msg.split(',')

    x = int(coordinates[0])
    y = int(coordinates[1])

    return (x, y)


def make_shot(random_shot, actual_shot=(0, 0)):
    if random_shot:
        x = rand.randint(0, 9)
        y = rand.randint(0, 9)
        return format_shot((x, y))
    else:
        orientation = rand.randint(0, 3)
        if orientation == 1:
            new_shot = make_new_shot((x, y + 1))
        elif orientation == 2:
            new_shot = make_new_shot((x + 1, y))
        elif orientation == 3:
            new_shot = make_new_shot((x, y - 1))
        else:
            new_shot = make_new_shot((x - 1, y))

        return format_shot(new_shot)


def make_new_shot(coordinate):
    if bd.valid_point(coordinate):
        return coordinate


def format_shot(coordinates):
    return str(coordinates[0]) + ',' + str(coordinates[1])


tcp_sock = initializeServer()
initializeBoard()

while True:
    con, cliente = tcp_sock.accept()
    print('Connected' + str(cliente))
    while True:
        try:
            msg = con.recv(1024)
            if not msg:
                break

            msg = msg.decode("utf-8")

            shot = get_shot(msg)

            hit = bd.shot_ship(shot)

            if hit:
                ship_destroyed = bd.check_ship_destroyed(shot)
                if ship_destroyed:
                    print('SHIP DESTROYED')
                    end_game = bd.check_end_game()
                    if not end_game:
                        shot = make_shot(False, shot)
                    else:
                        print('GAME FINISHED')
                else:
                    shot = make_shot(True)
            else:
                shot = make_shot(True)

            if args.debug:
                print('BOARD SERVER')
                bd.print_board()

            con.sendall(shot.encode())
        except:
            con.sendall('error'.encode())

    print('Closing connection' + str(cliente))
    con.close()
