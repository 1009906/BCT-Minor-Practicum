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
    database_path = f"data/{current_node}/database.db"
    ledger_path = f"data/{current_node}/ledger.dat"
    temp_ledger_path = f"data/{current_node}/templedger.dat"
    pool_path = f"data/{current_node}/pooltx.dat"
    temp_pool_path = f"data/{current_node}/temppooltx.dat"
    hash_file_path = f"data/{current_node}/hash_file.txt"

    #All used addresses, depends on current_node
    CURRENT_HOST_IP = 'localhost'
    OTHER_HOST_IP = 'localhost'

    W_SERVER_ADDRESSES = [(CURRENT_HOST_IP, 5000), (OTHER_HOST_IP, 5002)]
    M_SERVER_ADDRESSES = [(CURRENT_HOST_IP, 5001), (OTHER_HOST_IP, 5003)]
    DB_SERVER_ADDRESSES = [(CURRENT_HOST_IP, 5004), (OTHER_HOST_IP, 5005)]

    W_SERVER_ADDR = W_SERVER_ADDRESSES[0] if current_node == "node1" else W_SERVER_ADDRESSES[1]
    M_SERVER_ADDR = M_SERVER_ADDRESSES[0] if current_node == "node1" else M_SERVER_ADDRESSES[1]
    DB_SERVER_ADDR = DB_SERVER_ADDRESSES[0] if current_node == "node1" else DB_SERVER_ADDRESSES[1]

    subprocesses = []
    
    def __repr__(self):
        repr_str = f"User id: {self.user_id}\n"
        repr_str += f"User name: {self.user_name}\n"
        repr_str += f"Last login date: {self.last_login_date}\n"
        return repr_str