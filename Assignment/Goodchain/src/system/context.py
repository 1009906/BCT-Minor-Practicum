from datetime import datetime

class Context:
    user_id: int = None
    user_name: str = None
    private_key: str = None
    public_key: str = None
    last_login_date: datetime = None
    current_node: str = "node1"

    db_connection = None  # database connection

    #TODO REMOVE, Values from part 1.
    # database_path = "data/database/database.db"
    # ledger_path = "data/ledger/ledger.dat"
    # temp_ledger_path = "data/ledger/templedger.dat"
    # pool_path = "data/pool/pooltx.dat"
    # temp_pool_path = "data/pool/temppooltx.dat"
    # hash_file_path = "data/hash_file.txt"

    #All used paths, depends on current_node
    database_path = f"data/{current_node}/database.db"
    ledger_path = f"data/{current_node}/ledger.dat"
    temp_ledger_path = f"data/{current_node}/templedger.dat"
    pool_path = f"data/{current_node}/pooltx.dat"
    temp_pool_path = f"data/{current_node}/temppooltx.dat"
    hash_file_path = f"data/{current_node}/hash_file.txt"

    #All used ports
    HOST_IP = 'localhost'
    
    W_SERVER_PORTS = [5000, 5002]
    M_SERVER_PORTS = [5001, 5003]

    W_SERVER_PORT = 5000 if current_node == "node1" else 5002
    M_SERVER_PORT = 5001 if current_node == "node1" else 5003

    # W_SERVER_PORT_CURRENT_NODE = 5000
    # W_SERVER_PORT_OTHER_NODE = 5002

    # M_SERVER_PORT_CURRENT_NODE = 5001
    # M_SERVER_PORT_OTHER_NODE = 5003
    
    def __repr__(self):
        repr_str = f"User id: {self.user_id}\n"
        repr_str += f"User name: {self.user_name}\n"
        repr_str += f"Last login date: {self.last_login_date}\n"
        return repr_str