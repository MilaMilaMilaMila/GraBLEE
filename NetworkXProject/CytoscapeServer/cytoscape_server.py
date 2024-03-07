import socket
import configparser
from datetime import datetime
import py4cytoscape as p4c
import os
import xmltodict as xd


def get_client_file(conn, file_name=None, file_format='cyjs', file_object='GRAPH', package_size=1024):
    print(f'\nSERVER: {file_object} RECEIVE START')
    data_len = conn.recv(package_size)
    print(f'SERVER: sending file size in bytes: {data_len}')
    data_len = int.from_bytes(data_len, byteorder='big')
    print(f'SERVER: sending file size: {data_len}')
    response = f'SERVER MESSAGE: received file len: {data_len}'
    conn.send(response.encode())

    if file_name is None:
        file_name = f'{file_object}_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'

    full_file_name = f'{file_name}.{file_format}'
    file = open(full_file_name, "wb")

    received_data_len = 0
    while True:
        try:
            part_data = conn.recv(package_size)
        except BaseException as e:
            print(f'SERVER: GETTING GRAPH: error: {e}')
            exit()

        print(f'in process get {len(part_data)}')
        conn.send('ok'.encode())

        if not part_data:
            break

        file.write(part_data)
        received_data_len += len(part_data)

        if received_data_len == data_len:
            break

    print(f'SERVER: get bytes: {received_data_len}')
    response = conn.recv(package_size).decode()
    print(response)
    response = f'SERVER MESSAGE: get bytes: {received_data_len}'.encode()
    conn.send(response)
    print(f'SERVER: {file_object} RECEIVE END\n')

    return full_file_name


def save_network_as_session(session_name=None):
    p4c.save_session(filename=session_name)


def create_cytoscape_session(filename, styles_filename, session_name=None):
    p4c.import_network_from_file(filename)

    if styles_filename:
        style_name = apply_style(styles_filename)

    # save current network as cytoscape session
    if session_name is None:
        session_name = ''.join(filename.split('.')[0:-1]) + '_session'

    save_network_as_session(session_name)

    p4c.delete_visual_style(style_name)
    # destroy current network
    suid = p4c.get_network_suid()
    p4c.delete_network(suid)
    return session_name + '.cys'


def send_cytoscape_session_file_to_client(conn, session_file_name, package_size=1024):
    file = open(session_file_name, "rb")
    data = file.read()
    file.close()
    print('\nSERVER: SESSION DELIVERY START')
    data_len = len(data)
    print(f'SERVER: sending session file size: {data_len}')
    len_data_in_bytes = data_len.to_bytes(length=8, byteorder='big')
    print(f'SERVER: sending session file size in bytes: {len_data_in_bytes}')
    conn.send(len_data_in_bytes)
    response = conn.recv(package_size).decode()
    print(response)

    for i in range(0, data_len, package_size):
        conn.send(data[i:min(i + package_size, data_len)])
        response = conn.recv(package_size).decode()
        print(response)

        if response != 'ok':
            print('SERVER: getting file package error')
            print('SERVER: PROGRAM WAS TERMINATED')
            exit()

    conn.send(f'SERVER MESSAGE: all file data was sent'.encode())
    response = conn.recv(package_size).decode()
    print(response)

    # os.remove(graph_filename)
    print('SERVER: delivery successfully')
    print('SERVER: SESSION DELIVERY END\n')


# def ping_cytoscape():
#     try:
#         p4c.cytoscape_ping()
#
#         print('Успешный пинг к Cytoscape')
#         # time.sleep(5)
#
#     except Exception as e:
#         print(f'Ошибка пинга: {e}')
#
#
# def cs_scheduler():
#     schedule = Scheduler(n_threads=0)
#     schedule.cyclic(dt.timedelta(seconds=4), ping_cytoscape)
#     while True:
#         schedule.exec_jobs()

def get_styles(conn, package_size=1024):
    is_styled = conn.recv(package_size).decode()
    response = f'SERVER MESSAGE: received styles flag: {is_styled}'
    conn.send(response.encode())

    if is_styled == 'TRUE':
        return get_client_file(conn, file_format='xml', file_object='STYLES')
    return None


def apply_style(styles_filename):
    p4c.import_visual_styles(styles_filename)
    file = open(styles_filename)
    data = file.read()
    dict = xd.parse(data)
    style_name = dict['vizmap']['visualStyle']['@name']
    p4c.set_visual_style(style_name)
    return style_name


def server_program():
    config = configparser.ConfigParser()
    config.read('config_server.ini')

    host = config['MAC']['Host']
    port = int(config['MAC']['Port']) # initiate port no above 1024
    listeners_amount = int(config['MAC']['Listeners_amount'])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(listeners_amount)

    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("SERVER: Connection from: " + str(address))

        styles_filename = get_styles(conn)
        filename = get_client_file(conn)
        print(filename)
        session_file_name = create_cytoscape_session(filename, styles_filename)
        send_cytoscape_session_file_to_client(conn, session_file_name)

        os.remove(filename)
        os.remove(styles_filename)
        os.remove(session_file_name)
        conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
