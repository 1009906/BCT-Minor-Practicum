import socket
from threading import Timer
from src.system.context import Context

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HOST_IP = 'localhost'

ADDR = (HOST_IP, PORT)
class PoolClient:

    def __init__(self):
        self.cont_flag = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.client_name = Context.user_name
        self.client.send(self.client_name.encode(FORMAT))
        print(self.client.recv(2048).decode(FORMAT))

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode(FORMAT))

    def stop_the_client(self):
        mes = DISCONNECT_MESSAGE
        self.send(mes)
        self.cont_flag = False

    def start_client(self):

        while self.cont_flag:

            timeout = 15
            timeout_thread = Timer(timeout, self.stop_the_client, [])
            timeout_thread.start()

            if not self.cont_flag:
                print('The connection has already terminated.')
                break

            print('--------------------------')
            print('You can send a message to server')
            print('to stop connection, press enter on a blank message')
            mes = input('Your message: ')
            if not mes:
                mes = DISCONNECT_MESSAGE
                self.cont_flag = False
            try:
                self.send(mes)
            except:
                print('The connection has already terminated.')
                self.cont_flag = False

            timeout_thread.cancel()