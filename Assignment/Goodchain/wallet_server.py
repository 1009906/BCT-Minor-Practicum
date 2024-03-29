import pickle
import select
import socket 
import threading
from src.system.context import Context
from src.system.services.network_service import process_received_remove_transactions, process_received_set_invalid_transactions, process_received_transaction

HEADER = 64

ADDR = Context.W_SERVER_ADDR

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
REMOVE_TXS_MESSAGE = "!REMOVE_TXS"
SET_INVALID_TXS_MESSAGE = "!SET_INVALID_TXS"

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
                    received_tx = pickle.loads(msg)
                    print(f"[{client_name}@{addr}]>> Received Transaction: {received_tx}")

                    transaction_processed = process_received_transaction(received_tx)
                    print("Validation Result: " + str(transaction_processed[0]))

                    return_message = f'Server received and processed your transaction: {transaction_processed[1]}'
                    conn.send(return_message.encode(FORMAT))
                except:
                    msg = msg.decode(FORMAT)

                    if msg.startswith(REMOVE_TXS_MESSAGE):
                        tx_ids = msg[len(REMOVE_TXS_MESSAGE):].split(",")

                        print(f"[{client_name}@{addr}]>> Received Remove Transactions: {tx_ids}")
                        result = process_received_remove_transactions(tx_ids)
                        print("Remove Result: " + str(result))

                    elif msg.startswith(SET_INVALID_TXS_MESSAGE):
                        tx_ids = msg[len(SET_INVALID_TXS_MESSAGE):].split(",")

                        print(f"[{client_name}@{addr}]>> Received Set Invalid Transactions: {tx_ids}")
                        result = process_received_set_invalid_transactions(tx_ids)
                        print("Set Invalid Result: " + str(result))

                    elif msg == DISCONNECT_MESSAGE:
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
    print(f"[LISTENING] Wallet Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Wallet Server is starting...")
start()