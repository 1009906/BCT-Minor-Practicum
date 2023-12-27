from sqlite3 import IntegrityError
from src.system.networking.client_helper import create_database_client_and_send_create_user, create_wallet_client_and_send_transaction
from src.system.networking.database_client import CREATE_USER_MESSAGE
from src.system.security.hashing import hash_password
from src.system.context import Context
from cryptography.hazmat.primitives import serialization
from src.system.blockchain.Transaction import *
from src.system.services.database_service import is_user_in_database
from src.system.services.pool_service import generate_random_transaction_id
from src.system.util.formatting_util import create_formatted_string

def create_user(user_name, password):
    #TODO Remove
    # con = Context.db_connection
    # c = con.cursor()

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

    if is_user_in_database(user_name):
        return False, "User already exists."
    
    try:
        # c.execute(
        #     "INSERT INTO users (Name, Password, PrivateKey, PublicKey) "
        #     "VALUES (?, ?, ?, ?)",
        #     (user_name, hashed_password, prv_ser, pbc_ser))
        # con.commit()

        user_data = {
            "username": user_name,
            "hashed_password": hashed_password,
            "private_key": prv_ser,
            "public_key": pbc_ser
        }

        formatted_string = create_formatted_string(CREATE_USER_MESSAGE, user_data)
        create_database_client_and_send_create_user(formatted_string, "System")

        signup_reward(user_name, pbc_ser)
        return True, f"{user_name} Added to the system."

    except :
        return False, "Error while creating user."

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