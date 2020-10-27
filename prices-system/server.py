import socket
import argparse

import helper

global args


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


get_arguments()
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (args.host, args.port)
udp.bind(orig)

while True:
    print('recebi')
    msg, cliente = udp.recvfrom(1024)

    data = msg.decode()

    file_type = data[0]

    if file_type == 'D':
        helper.write_file(data, 'server_files/')
    elif file_type == 'P':
        data = data.split(' ')
        file_id = data[1]
        gas_type = data[2]
        radius = data[3]
        latitude = data[4]
        longitude = data[5]
        helper.search_cheap(file_id, gas_type, radius, latitude, longitude)

    print(str(cliente) + str(msg))

udp.close()
