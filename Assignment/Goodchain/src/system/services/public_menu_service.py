from sqlite3 import IntegrityError
from src.system.networking.client_helper import create_wallet_client_and_send_transaction
from src.system.security.hashing import hash_password
from src.system.context import Context
from cryptography.hazmat.primitives import serialization
from src.system.blockchain.Transaction import *
from src.system.services.pool_service import generate_random_transaction_id

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
        signup_reward(user_name, pbc_ser)
        return True, f"{user_name} Added to the system."

    except IntegrityError:
        return False, "User already exists."

def signup_reward(receiver_name, public_key):
    #Create transaction user gets 50 coins
    tx = Tx(generate_random_transaction_id(), None, receiver_name, SIGNUP)
    tx.add_output(public_key, SIGNUP_REWARD)
    tx.set_valid()

    #TODO Remove
    # savefile = open(Context.pool_path, "ab")
    # pickle.dump(tx, savefile)
    # savefile.close()

    create_wallet_client_and_send_transaction(tx, receiver_name)