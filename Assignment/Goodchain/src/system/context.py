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

    database_path = f"data/{current_node}/database.db"
    ledger_path = f"data/{current_node}/ledger.dat"
    temp_ledger_path = f"data/{current_node}/templedger.dat"
    pool_path = f"data/{current_node}/pooltx.dat"
    temp_pool_path = f"data/{current_node}/temppooltx.dat"
    hash_file_path = f"data/{current_node}/hash_file.txt"
    
    def __repr__(self):
        repr_str = f"User id: {self.user_id}\n"
        repr_str += f"User name: {self.user_name}\n"
        repr_str += f"Last login date: {self.last_login_date}\n"
        return repr_str