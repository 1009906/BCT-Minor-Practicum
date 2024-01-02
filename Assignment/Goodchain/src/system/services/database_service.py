from sqlite3 import IntegrityError
from src.system.blockchain.Signature import generate_keys
from src.system.connection import get_connection
from src.system.context import Context
from src.system.util.formatting_util import unformat_datetime
from cryptography.hazmat.primitives import serialization

def add_user_to_database(parsed_user_data):
    try:
        user_name = parsed_user_data["username"]
        hashed_password = parsed_user_data["hashed_password"]
        prv_ser = parsed_user_data["private_key"]
        pbc_ser = parsed_user_data["public_key"]

        public_key = bytes(pbc_ser[2:-1], 'utf-8')
        private_key = bytes(prv_ser[2:-1], 'utf-8')

        con = Context.db_connection if Context.db_connection else get_connection()
        c = con.cursor()
        c.execute(
                "INSERT INTO users (Name, Password, PrivateKey, PublicKey) "
                "VALUES (?, ?, ?, ?)",
                (user_name, hashed_password, private_key, public_key))
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
    
def update_password_user(parsed_user_data):
    con = Context.db_connection if Context.db_connection else get_connection()
    c = con.cursor()

    user_name = parsed_user_data["username"]
    hashed_password = parsed_user_data["hashed_password"]

    try:
        c.execute(
            "UPDATE users "
            "SET    Password = ? "
            "WHERE Name = ?"
            , (hashed_password, user_name))

        if c.rowcount == 1:
            con.commit()
            return True
        else:
            return False

    except IntegrityError as e:
        return False