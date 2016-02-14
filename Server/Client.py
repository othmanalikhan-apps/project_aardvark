import socket

HOST = ''    #server name goes in here
PORT = 3820
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST,PORT))
with open('myUpload.txt', 'rb') as file_to_send:
    for data in file_to_send:
        socket.sendall(data)
print('end')
socket.close()t