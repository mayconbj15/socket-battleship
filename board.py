import numpy as np
import random as rand

board = np.zeros((10,10))

BOARD_SIZE = 10

ships = []

def random_board(number_of_ships):
    for i in range(0, number_of_ships):
        created = ship_created([])
        while not created:
            new_ship = make_ship(rand.randint(0,9), rand.randint(0,9), rand.randint(2,5))
            if ship_created(new_ship):
                ships.append(new_ship)
                created = True

    return board

def make_ship(initial_pixel_x, initial_pixel_y, ship_size):
    orientation = rand.randint(0,1)

    ship = []
    print('make ship \n' + 'x: ' + str(initial_pixel_x) + '\ny: ' + str(initial_pixel_y) + '\nsize: ' + str(ship_size) + '\n orientarion: ' + str(orientation))
    if orientation == 0:
        if can_get_ship(initial_pixel_y, ship_size):
            ship = get_horizontal_ship(initial_pixel_x, initial_pixel_y, ship_size)
    else:
        if can_get_ship(initial_pixel_x, ship_size):
            ship = get_vertical_ship(initial_pixel_x, initial_pixel_y, ship_size)

    if not have_ship(ship) and len(ship) > 0:
        make_ship_in_board(ship)

    return ship

def ship_created(ship):
    return len(ship) > 0

def get_horizontal_ship(initial_pixel_x, initial_pixel_y, ship_size):
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

def have_ship(ship):
    for ship_coordinate in ship:
        if get_point(ship_coordinate[0], ship_coordinate[1]) == 1:
            return True
    
    return False

def make_ship_in_board(ship):
    print('make ship')
    print(ship)
    for ship_coordinate in ship:
        print('index: of ' + str(ship_coordinate[0]) + ' ' + str(ship_coordinate[1]))
        print(ship.index((ship_coordinate[0], ship_coordinate[1])))
        
        set_point(ship_coordinate[0], ship_coordinate[1], 1)

def can_get_ship(initial_pixel, ship_size):
    return initial_pixel + ship_size <= BOARD_SIZE

def get_ship(x, y):
    ship = []
    for s in ships:
        try:
            print('SHIP')
            print(s)
            ship_index = s.index((x, y))
            
            print('FOUND SHIP: ' + str(ship_index))
            return s
        except:
            print('ship is not in list: ' + str(x) + str(y))
            print(s)
    
    return ship

def remove_pixel_of_ship(ship, coordinates):
    ship.remove(coordinates)

    return is_ship_destroyed(ship)

def ship_destroyed(x, y):
    ship = get_ship(x, y)
    return remove_pixel_of_ship(ship, (x, y))

def is_ship_destroyed(ship):
    return len(ship) == 0

def shot_ship(x, y):
    if have_pixel(x, y):    
        set_point(x, y, -1)
        return True
    else:
        return False
    
def have_pixel(x, y):
    print(board)
    return get_point(x, y) == 1

def print_board():
    print(board)

def set_point(x, y, value):
    board[x][y] = value

def get_point(x, y):
    if valid_point(x, y):
        return board[x][y]

def valid_point(x, y):
    return x < 10 and y < 10

def initializeBoard(number_of_ships):
    random_board(number_of_ships)


