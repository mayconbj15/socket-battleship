import socket
import sys
import argparse
import board as bd


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


def initializeClient():
    get_arguments()
    try:
        print('Creating socket')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('Connecting to the server')
        sock.connect((args.host, args.port))

        print('Connection sucess!')

        return sock
    except:
        print('Failed to create connection')
        sys.exit()


def initializeBoard():
    bd.board_file('board.txt')
    bd.print_board()


def get_shot(msg):
    coordinates = msg.split(',')
    print(coordinates)

    x = int(coordinates[0])
    y = int(coordinates[1])

    return (x, y)


def format_shot(x, y):
    return str(x) + ',' + str(y)


def get_data(inp):
    if len(inp) == 1:
        return inp
    elif len(inp) > 1:
        data = inp.split(' ')
        print(data)
        return format_shot(int(data[0]), int(data[1]))
    elif len(inp) == 0:
        return ''


def get_response_status(response):
    if response == 'error':
        return False
    else:
        return True


def send_data(data):
    send = False
    if data == 'p' or data == 'P':
        bd.print_board()
        send = False
    elif data != '':
        sock.send(data.encode())
        send = True
    else:
        print('Invalid data. Send again')
        send = False

    return send


sock = initializeClient()
initializeBoard()

print('Para sair use CTRL+X\n')
msg = ''
while msg != '\x18':
    print('Enter the input to the server')
    inp = input()

    data = get_data(inp)

    send = send_data(data)

    if send:
        response = sock.recv(1024).decode("utf-8")

        sucess = get_response_status(response)

        if sucess:
            if args.debug:
                bd.print_board()

            shot = get_shot(response)
            hit = bd.shot_ship(shot[0], shot[1])

            if hit:
                ship_destroyed = bd.check_ship_destroyed(shot)

                if ship_destroyed:
                    print('SHIP DESTROYED')
                    end_game = bd.check_end_game()
                    if end_game:
                        print('END OF GAME')
                        sock.close()
        else:
            print('Server error')
