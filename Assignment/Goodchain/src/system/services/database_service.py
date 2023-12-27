from src.system.connection import get_connection
from src.system.context import Context

def add_user_to_database(parsed_user_data):
    try:
        user_name = parsed_user_data["username"]
        hashed_password = parsed_user_data["hashed_password"]
        prv_ser = parsed_user_data["private_key"]
        pbc_ser = parsed_user_data["public_key"]

        con = Context.db_connection if Context.db_connection else get_connection()
        c = con.cursor()
        c.execute(
                "INSERT INTO users (Name, Password, PrivateKey, PublicKey) "
                "VALUES (?, ?, ?, ?)",
                (user_name, hashed_password, prv_ser, pbc_ser))
        con.commit()
        return True
    except:
        return False

def is_user_in_database(user_name):
    con = Context.db_connection if Context.db_connection else get_connection()
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE Name=?", (user_name,))
    return c.fetchone() is not None