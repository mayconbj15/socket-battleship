import socket
import argparse

import helper

global args


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Battleship tcp socket')

    parser.add_argument("-d", "--debug", dest="debug", default="n",
                        choices=['y', 'n'], help="Run in debug mode that print board of client")
    parser.add_argument("-i", "--host", dest="host", default="127.0.0.1",
                        help="The host of server")
    parser.add_argument("-p", "--port", dest="port", default=5000,
                        help="The port of server")

    global args
    args = parser.parse_args()


get_arguments()
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (args.host, args.port)

print('Para sair use CTRL+X\n')
msg = input()

while msg != '\x18':
    msg = helper.read_file('client_files/' + msg + '.txt')

    udp.sendto(msg.encode(), dest)
    msg = input()

udp.close()
