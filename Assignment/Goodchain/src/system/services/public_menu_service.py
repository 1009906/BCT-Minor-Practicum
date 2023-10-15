from sqlite3 import IntegrityError
from src.system.security.hashing import hash_password
from src.system.context import Context
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def create_user(user_name, password):
    con = Context.db_connection
    c = con.cursor()

    hashed_password = hash_password(password)
    keys = generate_keys()

    prv_ser = keys[0].private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
                )
    pbc_ser = keys[1].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

    try:
        c.execute(
            "INSERT INTO users (Name, Password, PrivateKey, PublicKey) "
            "VALUES (?, ?, ?, ?)",
            (user_name, hashed_password, prv_ser, pbc_ser))
        con.commit()

        return True, f"{user_name} Added to the system."

    except IntegrityError:
        return False, "User already exists."
    
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key