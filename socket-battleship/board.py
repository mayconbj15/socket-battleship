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
    """
        Open a file that describes the ship positions in the board

        Parameters
        ----------
        filepath: string
            Path file
    """
    f = open(filepath)

    lines = f.readlines()

    for line in lines:
        ship_size = int(line[0])
        i = 2
        while i < ship_size * 4:
            x = int(line[i])
            y = int(line[i+2])
            set_point((x, y), 1)
            i += 4

    f.close()


def make_ship(initial_pixel_x, initial_pixel_y, ship_size):
    """
        Set a ship with a size in the board

        Parameters
        ----------
        initial_pixel_x: int
            The initial x coordinate of the ship
        initial_pixel_y: int
            The initial y coordinate of the ship
        ship_size: int
            The ship size
    """
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
    """
        Check whether the ship was created

        Parameters
        ----------
        ship: list
            The ship that'll be checked

        Returns
        -------
        bool
            If the ship was created
    """
    return len(ship) > 0


def get_horizontal_ship(initial_pixel_x, initial_pixel_y, ship_size):
    """
        Get a list with the representation of a horizontal ship

        Parameters
        ----------
        initial_pixel_x: int
            The initial x coordinate of the ship
        initial_pixel_y: int
            The initial y coordinate of the ship
        ship_size: int
            The ship size

        Returns
        -------
        list
            A representation of a ship
    """
    ship = []
    i = 0
    while i < ship_size:
        ship.append((initial_pixel_x, initial_pixel_y))
        i = i + 1
        initial_pixel_y = initial_pixel_y + 1

    return ship


def get_vertical_ship(initial_pixel_x, initial_pixel_y, ship_size):
    """
        Get a list with the representation of a vertical ship

        Parameters
        ----------
        initial_pixel_x: int
            The initial x coordinate of the ship
        initial_pixel_y: int
            The initial y coordinate of the ship
        ship_size: int
            The ship size

        Returns
        -------
        list
            A representation of a ship
    """
    i = 0
    ship = []

    while i < ship_size:
        ship.append((initial_pixel_x, initial_pixel_y))
        i = i + 1
        initial_pixel_x = initial_pixel_x + 1

    return ship


def have_ship(ship):
    """
        Checks if the ship exists in the board

        Parameters
        ----------
        ship: list
            The list with the ship coordinates

        Returns
        -------
        bool
            If the ship exists in the board
    """
    for ship_coordinate in ship:
        if get_point(ship_coordinate) == 1:
            return True

    return False


def make_ship_in_board(ship):
    """
        Set a ship in the board

        Parameters
        ----------
        ship: list
            A representation of the ship
    """
    for ship_coordinate in ship:
        set_point(ship_coordinate, 1)


def can_get_ship(initial_pixel, ship_size):
    """
        Check whether the dimension of ship is inside the board

        Parameters
        ----------
        initial_pixel: int
            The initial pixel of the ship
        ship_size: int
            The size of the ship

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

        Parameters
        ----------
        coordinates: tuple
            The shot coordinates

        Returns
        -------
        bool
            If the ship has been destroyed
    """
    ship = get_ship(coordinates)
    ship.remove(coordinates)
    ship_destroyed = is_ship_destroyed(ship)

    if ship_destroyed:
        # global n_ships
        n_ships = n_ships - 1

    return ship_destroyed


def check_end_game():
    """
        Checks the end of game

        Returns
        -------
        bool
            If the number of ships is equal to zero
    """
    return n_ships == 0


def is_ship_destroyed(ship):
    """
        Checks whether the ship was destroyed

        Parameters
        ----------
        ship: list
            The ship that'll been checked

        Returns
        -------
        bool
            If the ship was destroyed
    """
    return len(ship) == 0


def shot_ship(coordinates):
    """
        Remove the pixel of ship

        Parameters
        ----------
        coordinates: tuple
            The coordinates of the shot

        Returns
        -------
        bool
            If the pixel is removed
    """
    if have_pixel(coordinates):
        set_point(coordinates, -1)
        return True
    else:
        return False


def have_pixel(coordinates):
    """
        Check if the point in the x,y coordinate is equal to 1

        Parameters
        ----------
        coordinates: tuple
            The coordinates of pixel

        Returns
        -------
        bool
            If the point is equal to 1
    """
    return get_point(coordinates) == 1


def print_board():
    """Print the board"""
    print(board)


def set_point(coordinates, value):
    """
        Set a point in coordinates with a value

        Parameters
        ----------
        coordinates: tuple
            The coordinates of the point

        value: int
            The value of the point
    """
    board[coordinates[0]][coordinates[1]] = value


def get_point(coordinates):
    """
        Get a point of board in a coordinate

        Parameters
        coordinates: tuple
            The pixel coordinates

        Returns
        -------
        int 
            A point of the board
    """
    if valid_point(coordinates):
        return board[coordinates[0]][coordinates[1]]


def valid_point(coordinate):
    """
        Checks if determined coordinate is valid in board dimensions

        Returns
        -------
        bool 
            If the coordinate is in board dimensions
    """
    return coordinate[0] < 10 and coordinate[1] < 10


def initializeBoard(number_of_ships):
    random_board(number_of_ships)
