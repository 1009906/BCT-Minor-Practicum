from datetime import datetime

class Context:
    user_id: int = None
    user_name: str = None
    private_key: str = None
    public_key: str = None
    last_login_date: datetime = None

    db_connection = None  # database connection

    database_path = "src/database/database.db"
    ledger_path = "src/ledger/ledger.dat"
    pool_path = "src/pool/pooltx.dat"
    temp_pool_path = "src/pool/temppooltx.dat"
    hash_file_path = "src/hash_file.txt"

    def __repr__(self):
        repr_str = f"User id: {self.user_id}\n"
        repr_str += f"User name: {self.user_name}\n"
        repr_str += f"Last login date: {self.last_login_date}\n"
        repr_str += "\n"
        repr_str += f"Private key: {self.private_key}\n"
        repr_str += "\n"
        repr_str += f"Public key: {self.public_key}\n"
        return repr_str