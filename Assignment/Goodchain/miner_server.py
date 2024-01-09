import pickle
import select
import socket 
import threading
from src.system.context import Context
from src.system.services.network_service import process_received_block

HEADER = 64

ADDR = Context.M_SERVER_ADDR

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    client_name = conn.recv(2048).decode(FORMAT)

    print(f"\n[NEW CONNECTION] {client_name}@{addr} is connected.")
    connection_message = f"...\nHi {client_name}! \nYou are successfully connected to the server {ADDR}"
    conn.send(connection_message.encode(FORMAT))
    connected = True
    while connected:
        ready_to_read, ready_to_write, in_error = select.select([conn], [], [conn], 20)
        if len(ready_to_read):
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)

                msg = conn.recv(msg_length)

                print("Received message length: ", msg_length)

                try:
                    received_block = pickle.loads(msg)
                    print(f"[{client_name}@{addr}]>> Received Block: {received_block}")

                    block_processed = process_received_block(received_block)
                    print("Validation Result: " + str(block_processed[0]))

                    return_message = f'Server received and processed your block: {block_processed[1]}'
                    conn.send(return_message.encode(FORMAT))
                except:
                    msg = msg.decode(FORMAT)
                    if msg == DISCONNECT_MESSAGE:
                        connected = False

                    print(f"[{client_name}@{addr}]>> {msg}")
                    return_message = f'Server received your message: "{msg}"'
                    conn.send(return_message.encode(FORMAT))
        else:
            connected = False
            return_message = f'\nTimeout! You are disconnected.'
            conn.send(return_message.encode(FORMAT))
    
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")    

def start():
    server.listen()
    print(f"[LISTENING] Miner Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Miner Server is starting...")
start()