import socket
from threading import Timer

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HOST_IP = 'localhost'

ADDR = (HOST_IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client_name = input('please enter your name: ')
client.send(client_name.encode(FORMAT))
print(client.recv(2048).decode(FORMAT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def stop_the_client():
    global cont_flag
    mes = DISCONNECT_MESSAGE
    send(mes)
    cont_flag = False

cont_flag = True
while cont_flag:

    timeout = 15
    timeout_thread = Timer(timeout, stop_the_client, [])
    timeout_thread.start()

    if not cont_flag:
        print('The connection has already terminated.')
        break

    print('--------------------------')
    print('You can send a message to server')
    print('to stop connection, press enter on a blank message')
    mes = input('Your message: ')
    if not mes:
        mes = DISCONNECT_MESSAGE
        cont_flag = False
    try:
        send(mes)
    except:
        print('The connection has already terminated.')
        cont_flag = False

    timeout_thread.cancel()