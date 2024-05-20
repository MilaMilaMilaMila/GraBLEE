import socket as sct


if __name__ == '__main__':
    host = "84.38.181.98"
    port = 23
    pcg_size = 1024

    socket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
    socket.connect((host, port))

    print('start getting cytoscape connection status')

    status = socket.recv(pcg_size)
    status = int.from_bytes(status, byteorder='big')
    print(f'status {status} was got')
    msg = f'received cytoscape connection status: {status}'
    print(msg)
    socket.send(msg.encode())

    print('finish getting cytoscape connection status')
