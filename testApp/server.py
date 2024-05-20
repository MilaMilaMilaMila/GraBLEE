import socket as sct


host = "84.38.181.98"
port = 23
pcg_size = 1024
listeners_amount = 2

socket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
socket.bind((host, port))
socket.listen(listeners_amount)

print('start sending cytoscape connection status')
status = 1
status_bin = status.to_bytes(length=8, byteorder='big')
socket.send(status_bin+b'\n')
print(f'status {status} was sent')
response = socket.recv(pcg_size).decode()
print(f'client response: {response}')

print('finish sending cytoscape connection status')