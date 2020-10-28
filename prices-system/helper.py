import sys


def read_file(path):
    """
        Read a file in the path

        Returns
        -------
        str
            A normalized string with the file data
    """
    msg = ''
    try:
        f = open(path, 'r')
        msg = f.readlines()
    except FileNotFoundError:
        print('File not found: ' + path)

    return normalize_list_str(msg)


def write_file(data, path):
    """Saves a file with format

        str(p1) int(p2)
        int(p3) float(p4) int(p5) int(p6)

        Where:
        str(p1) = The type of file. D for data and P for search
        int(p2) = The id of file
        int(p3) = The gas type: 0 - diesel, 1 - álcool, 2 - gasolina
        float(p4) = The price of the gas
        int(p5) = The latitude of gas station
        int(p6) = The longitude of gas station

        The name of file is equal 'str(p1) + int(p2)'

        Parameters
        ----------
        data: list
            The list of values to save in file
        path: str
            The path where the file will be saved
    """
    try:
        data = data.split(' ')
        txt = ''

        file_type = data[0]
        gas_station_id = data[1]
        txt += file_type + ' '
        txt += gas_station_id + '\n'

        file_data = []
        i = 2
        while i < len(data):
            j = i
            while j < i+4:
                file_data.append(data[j])
                j += 1

            txt += file_data[0] + ' '
            txt += str(int(file_data[1])/1000) + ' '
            txt += file_data[2] + ' '
            txt += file_data[3]

            if j < len(data):
                txt += '\n'

            file_data.clear()
            i += 4

        file_path = path + 'D' + gas_station_id.replace('\\n', '') + '.txt'
        f = open(file_path, 'w')
        f.write(txt)

        f.close()
    except:
        print('Error to write file')


def search_cheap(file_id, gas_type, radius, latitude, longitude):
    """
        Search for the cheapset fuel in the gas stations in the data file with the file_id

        Parameters:
        -----------
        file_id: int
            The id of the data file
        gas_type: int
            The type of the gas in the search
        radius: int
            The search radius
        latitude: int
            The gas station latitude
        longitude: int
            The gas station longitude

        Returns:
        --------
        float
            The cheapest fuel in the gas station list
    """
    try:
        data = read_file('server_files/' + 'D' + file_id + '.txt')
        if data:
            data = data.split(' ')
            cheap = float(data[3])
            file_data = []
            i = 2
            while i < len(data):
                j = i
                while j < i+4:
                    file_data.append(data[j])
                    j += 1

                if file_data[0] == gas_type:
                    if in_radius(int(radius), int(latitude), int(longitude), int(file_data[2]), int(file_data[3])):
                        if float(file_data[1]) < cheap:
                            cheap = float(file_data[1])

                file_data.clear()
                i += 4

            return cheap
    except:
        print('Error in search')
        return 0

    return 0


def in_radius(radius, latitude_center, longitude_center, gas_latitude, gas_longitude):
    """
        Defines wheter a latitude is in the search radius

        Parameters:
        -----------
        radius: int
            The search radius
        latitude_center: int
            The central latitude of search 
        longitude_center: int
            The central longitude of search 
        gas_latitude: int
            The gas station latitude
        gas_longitude: int
            The gas station longitude

        Returns:
        --------
        bool
            If the gas station is in the search radius
    """
    return (gas_latitude <= radius + latitude_center
            and gas_longitude <= radius + longitude_center) or (gas_latitude >= radius - latitude_center
                                                                and gas_longitude <= radius - longitude_center)


def normalize_list_str(msg):
    """
        Normalize a string without [],\n\

        Parameters
        ----------
        msg: str
            A string to be normalized

        Returns
        -------
        list
            A string normalized without [,] ' \\n \ characters
    """
    msg = str(msg)
    msg = msg.replace('[', '')
    msg = msg.replace(']', '')
    msg = msg.replace(',', '')
    msg = msg.replace('\\n', '')
    msg = msg.replace('\'', '')

    return msg
