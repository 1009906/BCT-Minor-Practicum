class Context:
    user_id: int = None
    user_name: str = None
    private_key: str = None
    public_key: str = None

    db_connection = None  # database connection

    database_path = "src/database/database.db"
    ledger_path = "src/ledger/ledger.dat"
    pool_path = "src/pool/pooltx.dat"
    temp_pool_path = "src/pool/temppooltx.dat"
    hash_file_path = "src/hash_file.txt"