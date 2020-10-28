import numpy as np
import random as rand

board = np.zeros((10, 10))

BOARD_SIZE = 10

ships = []

global n_ships


def random_board(number_of_ships):
    """
        Generate a random board with n ships

        Parameters
        ----------
        number_of_ships: int
            The number of ships in the board

        Returns
        -------
        ndarray
            An array with the ships marked 

    """
    for i in range(0, number_of_ships):
        created = False
        while not created:
            new_ship = make_ship(rand.randint(
                0, 9), rand.randint(0, 9), rand.randint(2, 5))
            if ship_created(new_ship):
                ships.append(new_ship)
                created = True
    global n_ships
    n_ships = number_of_ships

    return board


def board_file(filepath):
    f = open(filepath)

    lines = f.readlines()

    for line in lines:
        ship_size = int(line[0])
        i = 2
        while i < ship_size * 4:
            x = int(line[i])
            y = int(line[i+2])
            set_point(x, y, 1)
            i += 4

    f.close()


def make_ship(initial_pixel_x, initial_pixel_y, ship_size):
    orientation = rand.randint(0, 1)

    ship = []
    if orientation == 0:
        if can_get_ship(initial_pixel_y, ship_size):
            ship = get_horizontal_ship(
                initial_pixel_x, initial_pixel_y, ship_size)
    else:
        if can_get_ship(initial_pixel_x, ship_size):
            ship = get_vertical_ship(
                initial_pixel_x, initial_pixel_y, ship_size)

    if not have_ship(ship) and len(ship) > 0:
        make_ship_in_board(ship)

    return ship


def ship_created(ship):
    return len(ship) > 0


def get_horizontal_ship(initial_pixel_x, initial_pixel_y, ship_size):
    ship = []
    i = 0
    while i < ship_size:
        ship.append((initial_pixel_x, initial_pixel_y))
        i = i + 1
        initial_pixel_y = initial_pixel_y + 1

    return ship


def get_vertical_ship(initial_pixel_x, initial_pixel_y, ship_size):
    i = 0
    ship = []

    while i < ship_size:
        ship.append((initial_pixel_x, initial_pixel_y))
        i = i + 1
        initial_pixel_x = initial_pixel_x + 1

    return ship


def have_ship(ship):
    for ship_coordinate in ship:
        if get_point(ship_coordinate[0], ship_coordinate[1]) == 1:
            return True

    return False


def make_ship_in_board(ship):
    for ship_coordinate in ship:
        set_point(ship_coordinate[0], ship_coordinate[1], 1)


def can_get_ship(initial_pixel, ship_size):
    """
        Check whether the dimension of ship is inside the board

        Returns
        -------
        bool
            If the ship dimension is inside the board
    """
    return initial_pixel + ship_size <= BOARD_SIZE


def get_ship(coordinates):
    """
        Get the ship in the coordinates

        Parameters
        ----------
        coordinates: int
            The coordinates of ship to be searched

        Returns
        -------
        list
            A list with the ship coordinates

    """
    ship = []
    for s in ships:
        try:
            s.index(coordinates)

            return s
        except:
            pass

    return ship


def check_ship_destroyed(coordinates):
    """
        Remove the coordinate of the attacked ship

        Returns
        -------
        bool
            If the ship has been destroyed
    """
    ship = get_ship(coordinates)
    ship.remove(coordinates)
    ship_destroyed = is_ship_destroyed(ship)

    if ship_destroyed:
        #global n_ships
        n_ships = n_ships - 1

    return ship_destroyed


def check_end_game():
    """Checks the end of game"""
    return n_ships == 0


def is_ship_destroyed(ship):
    """
        Checks whether the ship was destroyed

        Returns
        -------
        bool
            If the ship was destroyed
    """
    return len(ship) == 0


def shot_ship(x, y):
    """
        Remove the pixel of ship

        Returns
        -------
        bool
            If the pixel is removed
    """
    if have_pixel(x, y):
        set_point(x, y, -1)
        return True
    else:
        return False


def have_pixel(x, y):
    """
        Check if the point in the x,y coordinate is equal to 1

        Returns
        -------
        bool
            If the point is equal to 1
    """
    return get_point(x, y) == 1


def print_board():
    """Print the board"""
    print(board)


def set_point(x, y, value):
    """Set a point in x,y coordinate with value"""
    board[x][y] = value


def get_point(x, y):
    """
        Get a point of board in x,y coordinate

        Returns
        -------
        int 
            A point of the board
    """
    if valid_point(x, y):
        return board[x][y]


def valid_point(x, y):
    """
        Checks if determined coordinate is valid in board dimensions

        Returns
        -------
        bool 
            If the coordinate is in board dimensions
    """
    return x < 10 and y < 10


def initializeBoard(number_of_ships):
    random_board(number_of_ships)
