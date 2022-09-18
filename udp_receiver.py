from socket import socket, AF_INET, SOCK_DGRAM

connection = socket(AF_INET, SOCK_DGRAM)

HOST, PORT = '', 52381
connection.bind((HOST, PORT))

while True:
    data = connection.recvfrom(1024)[0]
    hex_data = data.hex().upper()
    formatted_data = ' '.join(hex_data[i:i + 2] for i in range(0, len(hex_data), 2))
    print(formatted_data)
