import socket
import configparser
from datetime import datetime
import py4cytoscape as p4c
import os


def save_client_cytoscape_file(data, file_name=None, file_format='gml'):
    # if file name wasn't specified, file name created with current datetime info nx_graph_{date and time}
    if file_name is None:
        file_name = f'nx_graph_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'

    # create file in default(gml)
    full_file_name = f'{file_name}.{file_format}'

    file = open(full_file_name, "wb")
    file.write(data)
    file.close()

    return full_file_name


def get_gml_file(conn, data_package_bytes_limit=1024):

    data_len = conn.recv(data_package_bytes_limit)
    data_len = int.from_bytes(data_len, byteorder='big')
    print(data_len)
    conn.send(f'get file len {data_len}'.encode())
    data = conn.recv(data_len)
    if not data:
        # if data is not received break
        return
    file_name = save_client_cytoscape_file(data)
    conn.send(file_name.encode())  # send data to the client
    conn.send(file_name.encode())  # send data to the client
    return file_name


def save_network_as_session(session_name=None):
    p4c.save_session(filename=session_name)


def create_cytoscape_session(filename, session_name=None):
    p4c.import_network_from_file(filename)
    # save current network as cytoscape session
    if session_name is None:
        session_name = ''.join(filename.split('.')[0:-1]) + '_session'

    save_network_as_session(session_name)

    # destroy current network
    suid = p4c.get_network_suid()
    p4c.delete_network(suid)
    return session_name + '.cys'


def sent_cytoscape_session_file_to_client(conn, session_file_name):
    file = open(session_file_name, "rb")
    data = file.read()
    file.close()
    len_data = len(data)
    conn.send(len_data.to_bytes(length=8, byteorder='big'))
    conn.send(data)
    answ = conn.recv(1024).decode()
    print(f'client status: {answ}')
    conn.send('get client status'.encode())


def server_program():
    config = configparser.ConfigParser()
    config.read('config_server.ini')

    host = config['REMOTE']['Host']
    port = int(config['REMOTE']['Port']) # initiate port no above 1024
    listeners_amount = int(config['REMOTE']['Listeners_amount'])

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(listeners_amount)

    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        filename = get_gml_file(conn)
        print(filename)
        session_file_name = create_cytoscape_session(filename)
        sent_cytoscape_session_file_to_client(conn, session_file_name)

        os.remove(filename)
        os.remove(session_file_name)
        conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
