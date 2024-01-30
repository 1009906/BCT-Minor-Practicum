import base64
from src.system.networking.client_helper import create_database_client_and_send_create_user, create_database_client_and_send_create_user_V2, create_wallet_client_and_send_transaction
from src.system.networking.database_client import CREATE_USER_MESSAGE
from src.system.security.hashing import hash_password
from cryptography.hazmat.primitives import serialization
from src.system.blockchain.Transaction import *
from src.system.services.database_service import is_user_in_database
from src.system.services.pool_service import generate_random_transaction_id, get_receiver_public_key
from src.system.util.formatting_util import create_formatted_string

def create_user(user_name, password):
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
    
    prv_base64 = base64.b64encode(prv_ser).decode('utf-8')
    pbc_base64 = base64.b64encode(pbc_ser).decode('utf-8')

    if is_user_in_database(user_name):
        return False, "User already exists."
    
    try:
        # user_data = {
        #     "username": user_name,
        #     "hashed_password": hashed_password,
        #     "private_key": prv_ser,
        #     "public_key": pbc_ser
        # }

        # formatted_string = create_formatted_string(CREATE_USER_MESSAGE, user_data)

        user_data = {
            "username": user_name,
            "hashed_password": hashed_password,
            "private_key": prv_base64,
            "public_key": pbc_base64
        }

        try:
            # create_database_client_and_send_create_user(formatted_string, "System")
            create_database_client_and_send_create_user_V2(user_data, "System")
        except:
            return False, "Error while sending create user message over the network."

        return True, f"{user_name} Added to the system."

    except :
        return False, "Error while creating user."

def signup_reward(receiver_name):
    try:
        public_key = get_receiver_public_key(receiver_name)

        if not public_key[0]:
            return False, "The receiver does not exist!"
        
        #Create transaction user gets 50 coins
        tx = Tx(generate_random_transaction_id(), None, receiver_name, SIGNUP)
        tx.add_output(public_key[1], SIGNUP_REWARD)
        tx.set_valid()

        try:
            create_wallet_client_and_send_transaction(tx, receiver_name)
        except:
            return False, "Error while sending signup reward transaction over the network."
        
        return True, "Signup reward transaction created."
    except:
        return False, "Error while creating signup reward transaction."