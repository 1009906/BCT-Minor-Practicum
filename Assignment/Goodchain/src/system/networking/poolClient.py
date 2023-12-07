from src.system.networking.poolServer import PoolServer

class PoolClient:
    def __init__(self):
        self.pool_server = PoolServer()

    #TODO Implement the following methods:
    # def send_transaction(self, transaction)