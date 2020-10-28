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
    msg, client = udp.recvfrom(1024)

    data = msg.decode()
    print('Client message')
    print(data)

    if data:
        file_type = data[0]

        if file_type == 'D':
            helper.write_file(data, 'server_files/')
            udp.sendto("Created!".encode('utf-8'), client)
        elif file_type == 'P':
            data = data.split(' ')
            cheap = helper.search_cheap(
                file_id=data[1], gas_type=data[2], radius=data[3], latitude=data[4], longitude=data[5])

            udp.sendto(str(cheap).encode('utf-8'), client)

udp.close()
