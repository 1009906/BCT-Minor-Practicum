import pickle
import socket
from threading import Timer
import uuid

from Signature import generate_keys
from Transaction import Tx
from cryptography.hazmat.primitives import serialization

HEADER = 64
PORT = 5050
W_SERVER_PORTS = [5000, 5002]

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HOST_IP = 'localhost'

ADDR = (HOST_IP, PORT)

class WalletClient:
    client = None
    cont_flag = False

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        client_name = input('please enter your name: ') #TODO take username from context.
        self.client.send(client_name.encode(FORMAT))
        print(self.client.recv(2048).decode(FORMAT))

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode(FORMAT))

    def send_tx(self, tx):
        # Serialize the Tx object before sending it
        serialized_tx = pickle.dumps(tx)
        msg_length = len(serialized_tx)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(serialized_tx)
        print(self.client.recv(2048).decode(FORMAT))

    def stop_the_client(self):
        # global cont_flag
        mes = DISCONNECT_MESSAGE
        self.send(mes)
        self.cont_flag = False
        self.client.close() #TODO: check if this is needed.

    def create_test_transaction(self):
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

    def handle_server(self): 
        self.cont_flag = True
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
            try:
                if not mes:
                    # mes = DISCONNECT_MESSAGE
                    # self.cont_flag = False
                    # self.send(mes)
                    self.stop_the_client()
                else:
                    # send(mes)
                    tx = self.create_test_transaction()
                    self.send_tx(tx)
                    self.stop_the_client()
            except:
                print('The connection has already terminated.')
                self.cont_flag = False

            timeout_thread.cancel()

wallet_client = WalletClient()
wallet_client.handle_server()