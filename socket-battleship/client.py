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
    """Initialize a socket with the TCP protocol"""
    try:
        print('Creating socket')
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('Connecting to the server')
        tcp_sock.connect((args.host, args.port))

        print('Connection sucess!')

        return tcp_sock
    except:
        print('Failed to create connection')
        sys.exit()


def initializeBoard(number_of_ships):
    """
        Initialize a board with n ships

        Parameters
        ----------
        number_of_ships: int
            The number of ships
    """
    # bd.board_file('board.txt')
    bd.initializeBoard(number_of_ships)
    bd.print_board()


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
    print(coordinates)

    x = int(coordinates[0])
    y = int(coordinates[1])

    return (x, y)


def format_shot(x, y):
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
    return str(x) + ',' + str(y)


def get_data(inp):
    """
        Validate and return a normalized string

        Parameters
        ----------
        inp: str
            The input send by user

        Returns
        -------
        str
            A normalized string if the inp is valid
            A empty string if the inp is not valid
    """
    if len(inp) == 1:
        return ''
    elif len(inp) > 1:
        data = inp.split(' ')
        print(data)
        return format_shot(int(data[0]), int(data[1]))
    elif len(inp) == 0:
        return ''


def get_response_status(response):
    """
        Verify the response of the server

        Parameters
        ----------
        response: str
            The response of the server

        Returns
        -------
        bool 
            If the response have error    
    """
    if response == 'error':
        return False
    else:
        return True


def send_data(data):
    """
        Send data to server

        Parameters
        ----------
        data: str
            The data that'll be send to server

        Returns
        -------
        bool
            If the data was send
    """
    send = False
    if data == 'p' or data == 'P':
        bd.print_board()
        send = False
    elif data != '':
        tcp_sock.send(data.encode())
        send = True
    else:
        print('Invalid data. Send again')
        send = False

    return send


get_arguments()
tcp_sock = initializeClient()
initializeBoard(1)

print('Type "q" to exit\n')
msg = ''
while msg != 'q':
    print('Enter the input to the server')
    inp = input()

    data = get_data(inp)

    if data:
        send = send_data(data)

        if send:
            response = tcp_sock.recv(1024).decode("utf-8")

            sucess = get_response_status(response)

            if sucess:
                if args.debug:
                    bd.print_board()

                if response != 'you win':
                    shot = get_shot(response)
                    hit = bd.shot_ship(shot)

                    if hit:
                        ship_destroyed = bd.check_ship_destroyed(shot)

                        if ship_destroyed:
                            print('SHIP DESTROYED')
                            end_game = bd.check_end_game()
                            if end_game:
                                print('END OF GAME')
                                tcp_sock.close()
                else:
                    print('You win!')
            else:
                print('Server error')
    else:
        print('Format of input invalid')
