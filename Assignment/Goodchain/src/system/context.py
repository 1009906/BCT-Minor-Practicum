from datetime import datetime

class Context:
    user_id: int = None
    user_name: str = None
    private_key: str = None
    public_key: str = None
    last_login_date: datetime = None
    current_node: str = "node1"

    db_connection = None  # database connection

    #All used paths, depends on current_node
    database_path = f"data/database.db"
    ledger_path = f"data/ledger.dat"
    temp_ledger_path = f"data/templedger.dat"
    pool_path = f"data/pooltx.dat"
    temp_pool_path = f"data/temppooltx.dat"
    hash_file_path = f"data/hash_file.txt"

    #All used addresses, depends on current_node
    HOST_IP_NODE_1 = 'localhost'
    HOST_IP_NODE_2 = 'localhost'

    W_SERVER_ADDRESSES = [(HOST_IP_NODE_1, 5000), (HOST_IP_NODE_2, 5002)]
    M_SERVER_ADDRESSES = [(HOST_IP_NODE_1, 5001), (HOST_IP_NODE_2, 5003)]
    DB_SERVER_ADDRESSES = [(HOST_IP_NODE_1, 5004), (HOST_IP_NODE_2, 5005)]

    W_SERVER_ADDR = W_SERVER_ADDRESSES[0] if current_node == "node1" else W_SERVER_ADDRESSES[1]
    M_SERVER_ADDR = M_SERVER_ADDRESSES[0] if current_node == "node1" else M_SERVER_ADDRESSES[1]
    DB_SERVER_ADDR = DB_SERVER_ADDRESSES[0] if current_node == "node1" else DB_SERVER_ADDRESSES[1]

    subprocesses = []
    
    def __repr__(self):
        repr_str = f"User id: {self.user_id}\n"
        repr_str += f"User name: {self.user_name}\n"
        repr_str += f"Last login date: {self.last_login_date}\n"
        return repr_str