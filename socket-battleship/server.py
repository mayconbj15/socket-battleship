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
    """Initialize a socket with the TCP protocol"""
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
    """
        Get the coordinates in the message

        Parameters
        ----------
        msg: str
            A message with the format (msg1, msg2), ex: 2,3

        Returns
        -------
        tuple
            A tuple with the int value of the msg1 and msg2
    """
    coordinates = msg.split(',')

    x = int(coordinates[0])
    y = int(coordinates[1])

    return (x, y)


def make_shot(random_shot, actual_shot=(0, 0)):
    """
        Make a new shot to send to client

        Parameters
        ----------
        random_shot: bool
            If the new shot is random
        actual_shot: tuple
            The actual shot of server

        Returns
        -------
        tuple
            A new shot to be send to the client
    """
    if random_shot:
        x = rand.randint(0, 9)
        y = rand.randint(0, 9)
        return format_shot((x, y))
    else:
        orientation = rand.randint(0, 3)
        new_shot = ((rand.randint(0, 9), rand.randint(0, 9)))
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
    """
        Returns the coordinate if it's valid

        Parameters
        ----------
        coordinate: str
            The coordinate to be checked

        Returns
        tuple
            The same coordinate if it's valid
    """
    if bd.valid_point(coordinate):
        return coordinate


def format_shot(coordinates):
    """
        Format the x, y values to a string

        Parameters
        ----------
        x: int
            The x value of the shot
        y: int
            The y value of the shot

        Returns
        -------
        A formated string with the format "x,y"
    """
    return str(coordinates[0]) + ',' + str(coordinates[1])


get_arguments()
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
                        con.sendall('you win'.encode())
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
