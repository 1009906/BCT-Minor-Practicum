from sqlite3 import IntegrityError
from src.system.security.hashing import hash_password
from src.system.context import Context

def create_user(user_name, password, private_key, public_key):
    con = Context.db_connection
    c = con.cursor()

    hashed_password = hash_password(password)

    try:
        c.execute(
            "INSERT INTO users (Name, Password, PrivateKey, PublicKey) "
            "VALUES (?, ?, ?, ?)",
            (user_name, hashed_password, private_key, public_key))
        con.commit()

        return True, f"{user_name} Added to the system."

    except IntegrityError:
        return False, "User already exists."