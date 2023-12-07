import select
import socket
import pickle

class PoolServer:
    def __init__(self):
        self.TCP_PORT = 5005 #TODO Dont use the same port as the ledger server
        self.BUFFER_SIZE = 1024

    def newServerConnection(self, ip_addr):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip_addr, self.TCP_PORT))
        server_socket.listen()
        return server_socket

    def recvObj(self, socket):
        ready_to_read, ready_to_write, in_error = select.select([socket], [], [socket], 30)
        if socket in ready_to_read:
            print('Server is blocked by accept() ...')
            connected_socket, addr = socket.accept()
            print('Server is released and receiving data ...')
            all_data = b''
            while True:
                data = connected_socket.recv(self.BUFFER_SIZE)
                if not data:
                    break
                all_data = all_data + data
            return pickle.loads(all_data)
        return None


    def sendObj(self, ip_addr, obj):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((ip_addr, self.TCP_PORT))
        data = pickle.dumps(obj)
        soc.send(data)
        soc.close()
        return False