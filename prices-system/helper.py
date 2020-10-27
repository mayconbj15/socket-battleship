import sys


def read_file(path):
    msg = ''
    f = open(path, 'r')
    msg = f.readlines()

    return normalize_list_str(msg)


def write_file(data, path):
    data = data.split(' ')
    print(data)
    txt = ''

    file_type = data[0] + ' '
    gas_station_id = data[1]
    txt += file_type
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

    f = open(path + gas_station_id.replace('\\n', '') + '.txt', 'w')
    f.write(txt)

    f.close()


def search_cheap(file_id, gas_type, radius, latitude, longitude):
    data = read_file('server_files/' + file_id + '.txt')
    data = data.split(' ')

    cheap = sys.maxsize
    file_data = []
    i = 2
    while i < len(data):
        j = i
        while j < i+4:
            file_data.append(data[j])
            j += 1

        print(file_data)
        if file_data[0] == gas_type:
            if int(latitude) + int(radius) <= int(file_data[2]) and int(longitude) + int(radius) <= int(file_data[3]):
                if float(file_data[1]) < cheap:
                    cheap = float(file_data[1])

        file_data.clear()
        i += 4

    print(cheap)
    print('cheap')


def normalize_list_str(msg):
    msg = str(msg)
    print(msg)
    print('msg')
    msg = msg.replace('[', '')
    msg = msg.replace(']', '')
    msg = msg.replace(',', '')
    msg = msg.replace('\\n', '')
    msg = msg.replace('\'', '')

    return msg
