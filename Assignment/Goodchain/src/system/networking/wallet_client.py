import pickle
import socket
from threading import Timer

from src.system.context import Context

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class WalletClient:
    def initialize_socket(self, port):
        ADDR = (Context.HOST_IP, port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(ADDR)
        client_name = Context.user_name
        client_socket.send(client_name.encode(FORMAT))
        print(client_socket.recv(2048).decode(FORMAT))
        return client_socket

    def send(self, msg, client_socket: socket.socket ):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client_socket.send(send_length)
        client_socket.send(message)
        print(client_socket.recv(2048).decode(FORMAT))

    def send_tx(self, tx, client_socket: socket.socket):
        serialized_tx = pickle.dumps(tx)
        msg_length = len(serialized_tx)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client_socket.send(send_length)
        client_socket.send(serialized_tx)
        print(client_socket.recv(2048).decode(FORMAT))

    def stop_the_client(self, client_socket: socket.socket):
        mes = DISCONNECT_MESSAGE
        self.send(mes, client_socket)
        client_socket.close()
        return False

    def handle_server(self, transaction):
        for port in Context.W_SERVER_PORTS:
            try:
                client_socket = self.initialize_socket(port)
            except:
                continue
            
            cont_flag = True
            while cont_flag:

                timeout = 15
                timeout_thread = Timer(timeout, self.stop_the_client, [client_socket])
                timeout_thread.start()

                if not cont_flag:
                    print('The connection has already terminated.')
                    break

                try:
                    self.send_tx(transaction, client_socket)
                    cont_flag = self.stop_the_client(client_socket)
                except:
                    print('The connection has already terminated.')
                    cont_flag = False

                timeout_thread.cancel()