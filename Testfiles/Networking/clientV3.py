import pickle
import socket
from threading import Timer
import uuid

from Signature import generate_keys
from Transaction import Tx
from cryptography.hazmat.primitives import serialization

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

def send_tx(tx):
    # Serialize the Tx object before sending it
    serialized_tx = pickle.dumps(tx)
    msg_length = len(serialized_tx)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(serialized_tx)
    print(client.recv(2048).decode(FORMAT))

def stop_the_client():
    global cont_flag
    mes = DISCONNECT_MESSAGE
    send(mes)
    cont_flag = False

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
    try:
        if not mes:
            mes = DISCONNECT_MESSAGE
            cont_flag = False
            send(mes)
        else:
            # send(mes)
            tx = create_test_transaction()
            send_tx(tx)
    except:
        print('The connection has already terminated.')
        cont_flag = False

    timeout_thread.cancel()