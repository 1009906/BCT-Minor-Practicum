import sqlite3
from src.system.context import Context

def get_connection():
    try:
        return sqlite3.connect(f'file:{Context.database_path}?mode=rw', uri=True)
    except sqlite3.OperationalError:
        exit("FATAL ERROR: Could not connect to the database, possibly because it's missing or corrupt.")