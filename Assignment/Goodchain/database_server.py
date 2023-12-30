import select
import socket 
import threading
from src.system.context import Context
from src.system.services.database_service import add_user_to_database, update_last_login_date_user
from src.system.util.formatting_util import parse_formatted_string

HEADER = 64

ADDR = Context.DB_SERVER_ADDR

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

CREATE_USER_MESSAGE = "!CREATE_USER"
EDIT_PASSWORD_MESSAGE = "!EDIT_PASSWORD"
UPDATE_LAST_LOGIN_DATE_MESSAGE = "!UPDATE_LAST_LOGIN_DATE"

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

                msg = msg.decode(FORMAT)

                if msg.startswith(CREATE_USER_MESSAGE):
                    print("Create user message received.")
                    msg = msg.replace(CREATE_USER_MESSAGE + " ", "")
                    parsed_user_data = parse_formatted_string(msg)
                    result = add_user_to_database(parsed_user_data)
                    if result:
                        print(f'User {parsed_user_data["username"]} is successfully created!')
                    else:
                        print(f'Error while creating user {parsed_user_data["username"]}!')

                elif msg.startswith(UPDATE_LAST_LOGIN_DATE_MESSAGE):
                    print("Update last login date message received.")
                    msg = msg.replace(UPDATE_LAST_LOGIN_DATE_MESSAGE + " ", "")
                    parsed_user_data = parse_formatted_string(msg)
                    result = update_last_login_date_user(parsed_user_data["username"], parsed_user_data["last_login_date"])
                    if result:
                        print(f'User {parsed_user_data["username"]} is successfully updated!')
                    else:
                        print(f'Error while updating user {parsed_user_data["username"]}!')
                    
                elif msg == DISCONNECT_MESSAGE:
                    connected = False

                print(f"[{client_name}@{addr}]>> {msg}")
                return_message = f'Server received your message: "{msg}"'
                conn.send(return_message.encode(FORMAT))
        else:
            connected = False
            return_message = f'\nTimeout! You are disconnected.'
            conn.send(return_message.encode(FORMAT))
    
    # bye_message = f"\nBye {client_name}!"
    # conn.send(bye_message.encode(FORMAT))
    # conn.close()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")    

def start():
    server.listen()
    print(f"[LISTENING] Database Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Database Server is starting...")
start()