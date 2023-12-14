import pickle
import socket
from threading import Timer
import uuid

from Signature import generate_keys
from Transaction import Tx
from cryptography.hazmat.primitives import serialization

HEADER = 64
# PORT = 5050
W_SERVER_PORTS = [5000, 5002]

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HOST_IP = 'localhost'

# ADDR = (HOST_IP, PORT)

class WalletClient:
    # client = None
    # cont_flag = False

    def initialize_socket(self, port):
        ADDR = (HOST_IP, port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(ADDR)
        client_name = input('please enter your name: ') #TODO take username from context.
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
        # Serialize the Tx object before sending it
        serialized_tx = pickle.dumps(tx)
        msg_length = len(serialized_tx)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client_socket.send(send_length)
        client_socket.send(serialized_tx)
        print(client_socket.recv(2048).decode(FORMAT))

    def stop_the_client(self, client_socket: socket.socket):
        # global cont_flag
        mes = DISCONNECT_MESSAGE
        self.send(mes, client_socket)
        # self.cont_flag = False
        client_socket.close() #TODO: check if this is needed.
        return False

    def handle_server(self, transaction):
        for port in W_SERVER_PORTS:
            client_socket = self.initialize_socket(port)
            
            cont_flag = True
            while cont_flag:

                timeout = 15
                timeout_thread = Timer(timeout, self.stop_the_client, [])
                timeout_thread.start()

                if not cont_flag:
                    print('The connection has already terminated.')
                    break

                # print('--------------------------')
                # print('You can send a message to server')
                # print('to stop connection, press enter on a blank message')
                # mes = input('Your message: ')
                try:
                    self.send_tx(transaction, client_socket)
                    cont_flag = self.stop_the_client(client_socket)
                except:
                    print('The connection has already terminated.')
                    cont_flag = False

                timeout_thread.cancel()


def create_test_transaction():
        alex_prv, alex_pbc = generate_keys()
        mike_prv, mike_pbc = generate_keys()

        alex_prv_ser = alex_prv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
            )
        
        alex_pbc_ser = alex_pbc.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        
        mike_pbc_ser = mike_pbc.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

        Tx1 = Tx(uuid.uuid1(), "Alex", "Mike", 0.1)
        Tx1.add_input(alex_pbc_ser, 2.3)
        Tx1.add_output(mike_pbc_ser, 1.0)
        Tx1.sign(alex_prv_ser)

        return Tx1

new_transaction = create_test_transaction()

wallet_client = WalletClient()
wallet_client.handle_server(new_transaction)