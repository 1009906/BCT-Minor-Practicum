from sqlite3 import IntegrityError
from src.system.connection import get_connection
from src.system.context import Context
from src.system.util.formatting_util import unformat_datetime

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

def update_last_login_date_user(user_name, last_login_date):
    last_login_date = unformat_datetime(last_login_date)
    con = Context.db_connection if Context.db_connection else get_connection()
    c = con.cursor()

    try:
        c.execute(
            "UPDATE users "
            "SET    LastLogin = ? "
            "WHERE Name = ?"
            , (last_login_date, user_name))

        if c.rowcount == 1:
            con.commit()
            return True
        else:
            return False

    except IntegrityError as e:
        return False