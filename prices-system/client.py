import socket
import argparse

import helper

global args


def get_arguments():
    """A function to get arguments pass by command line"""
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


def intialize_client():
    """A function to initialize a socket with the udp protocol"""
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (args.host, args.port)

    return (udp, dest)


get_arguments()
udp, dest = intialize_client()

print('Type "q" to exit\n')
msg = ''

while msg != 'q':
    print('Type the id of file')
    msg = input()
    msg = helper.read_file('client_files/' + msg + '.txt')

    response = udp.sendto(msg.encode(), dest)
    if response == 0:
        print('Error! Sending again')
        response = udp.sendto(msg.encode(), dest)

    msg, server = udp.recvfrom(1024)

    print('Server response')
    print(str(msg))

    msg = input()

udp.close()
