import sys


def read_file(path):
    msg = ''
    try:
        f = open(path, 'r')
        msg = f.readlines()
    except FileNotFoundError:
        print('File not found: ' + path)

    return normalize_list_str(msg)


def write_file(data, path):
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
    return (gas_latitude <= radius + latitude_center
            and gas_longitude <= radius + longitude_center) or (gas_latitude >= radius - latitude_center
                                                                and gas_longitude <= radius - longitude_center)


def normalize_list_str(msg):
    msg = str(msg)
    msg = msg.replace('[', '')
    msg = msg.replace(']', '')
    msg = msg.replace(',', '')
    msg = msg.replace('\\n', '')
    msg = msg.replace('\'', '')

    return msg
