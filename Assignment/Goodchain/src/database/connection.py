import sqlite3

def get_connection():
    try:
        return sqlite3.connect('file:src/database/database.db?mode=rw', uri=True)
    except sqlite3.OperationalError:
        exit("FATAL ERROR: Could not connect to the database, possibly because it's missing or corrupt.")