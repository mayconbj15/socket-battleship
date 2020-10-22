import numpy as np
import random as rand

board = np.zeros((10,10))

BOARD_SIZE = 10

def random_board(number_of_ships):
    for i in range(0, number_of_ships):
        ship_created = False
        while not ship_created:
            ship_created = make_ship(rand.randint(0,9), rand.randint(0,9), rand.randint(2,5))

    print(board)

def make_ship(initial_pixel_x, initial_pixel_y, ship_size):
    orientation = rand.randint(0,1)

    ship = []
    print('make ship \n' + 'x: ' + str(initial_pixel_x) + '\ny: ' + str(initial_pixel_y) + '\nsize: ' + str(ship_size) + '\n orientarion: ' + str(orientation))
    if orientation == 0:
        if can_get_ship(initial_pixel_y, ship_size):
            ship = get_horizontat_ship(initial_pixel_x, initial_pixel_y, ship_size)
    else:
        if can_get_ship(initial_pixel_x, ship_size):
            ship = get_vertical_ship(initial_pixel_x, initial_pixel_y, ship_size)

    if not haveShip(ship) and len(ship) > 0:
        make_ship_in_board(ship)
        return True
    
    return False

def get_horizontat_ship(initial_pixel_x, initial_pixel_y, ship_size):
    print('make horizontal ship ' + str(initial_pixel_y) + ' size: ' + str(ship_size))
    ship = []
    i = 0
    while i < ship_size:
        print('i: ' + str(i))  
        ship.append((initial_pixel_x, initial_pixel_y))
        i = i + 1
        initial_pixel_y = initial_pixel_y + 1
    
    print(ship)
    return ship
    

def get_vertical_ship(initial_pixel_x, initial_pixel_y, ship_size):
    print('make vertical ship ' + str(initial_pixel_x) + ' size: ' + str(ship_size))
    i = 0
    ship = []
    
    while i < ship_size:
        ship.append((initial_pixel_x, initial_pixel_y))
        i = i + 1
        initial_pixel_x = initial_pixel_x + 1
    
    print(ship)
    return ship

def haveShip(ship):
    for ship_coordinate in ship:
        if board[ship_coordinate[0]][ship_coordinate[1]] == 1:
            return True
    
    return False

def make_ship_in_board(ship):
    print('make ship')
    print(ship)
    for ship_coordinate in ship:
        print('index: of ' + str(ship_coordinate[0]) + ' ' + str(ship_coordinate[1]))
        print(ship.index((ship_coordinate[0], ship_coordinate[1])))
        board[ship_coordinate[0]][ship_coordinate[1]] = 1

def can_get_ship(initial_pixel, ship_size):
    return initial_pixel + ship_size <= BOARD_SIZE

def remove_pixel(ship, coordinates):
    ship_index = ship.index((coordinates[0], coordinates[1]))
    ship.remove(ship_index)

def ship_destroyed(ship):
    return len(ship) == 0

random_board(2)