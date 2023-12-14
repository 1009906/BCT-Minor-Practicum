import pickle
import select
import socket 
import threading

HEADER = 64
PORT = 5002 #5050
# local_ip = socket.gethostbyname('localhost')
local_ip = 'localhost'
ADDR = (local_ip, PORT)
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

                try:
                    # Deserialize the received message to reconstruct the Tx object
                    received_tx = pickle.loads(msg)

                    # Process received_tx as needed
                    print(f"[{client_name}@{addr}]>> Received Transaction: {received_tx}")

                    # Send acknowledgment or process the transaction
                    return_message = f'Server received your transaction: {received_tx}'
                    conn.send(return_message.encode(FORMAT))
                    
                except:
                    msg = msg.decode(FORMAT)
                    if msg == DISCONNECT_MESSAGE:
                        connected = False

                    print(f"[{client_name}@{addr}]>> {msg}")
                    return_message = f'Server received your message: "{msg}"'
                    conn.send(return_message.encode(FORMAT))

                # msg = conn.recv(msg_length).decode(FORMAT)
                # if msg == DISCONNECT_MESSAGE:
                #     connected = False

                # print(f"[{client_name}@{addr}]>> {msg}")
                # return_message = f'Server received your message: "{msg}"'
                # conn.send(return_message.encode(FORMAT))
        else:
            connected = False
            return_message = f'\nTimeout! You are disconnected.'
            conn.send(return_message.encode(FORMAT))
    
    bye_message = f"\nBye {client_name}!"
    conn.send(bye_message.encode(FORMAT))
    conn.close()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")    

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {local_ip}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()