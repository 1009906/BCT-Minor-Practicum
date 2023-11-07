from datetime import datetime
from sqlite3 import IntegrityError
from src.system.context import Context
from src.system.blockchain.TxBlock import PENDING, VALID
from src.system.services.blockchain_service import explore_chain
from src.system.services.pool_service import check_pool_valid_transactions
from src.user_interface.util.colors import convert_to_green, convert_to_red, convert_to_yellow

def update_last_login_date():
    con = Context.db_connection
    c = con.cursor()
    datetime_now = datetime.now()

    try:
        c.execute(
            "UPDATE users "
            "SET    LastLogin = ? "
            "WHERE Name = ?"
            , (datetime_now, Context.user_name))

        if c.rowcount == 1:
            con.commit()
            Context.last_login_date = datetime_now
            return True, "User updated."
        else:
            return False, "Error: Could not update user."

    except IntegrityError as e:
        return False, str(e)
    
def check_mined_blocks_status_since_last_login(blocks_added_since_last_login, user_name):
    result = ""
    valid_mined_blocks = []
    pending_mined_blocks = []

    if len(blocks_added_since_last_login) == 0:
        result += convert_to_red("No blocks that you mined were added to the chain since your last login.")
    else:
        for block in blocks_added_since_last_login:
            if block.status == VALID and block.miner_of_block == user_name:
                valid_mined_blocks.append(block)
            if block.status == PENDING and block.miner_of_block == user_name:
                pending_mined_blocks.append(block)
        
        if len(valid_mined_blocks) > 0:
            result += convert_to_green(f"The following blocks you mined were added to the chain since your last login: \n")
            for block in valid_mined_blocks:
                result += f"Block hash: {block.blockHash} \n"

        if len(pending_mined_blocks) > 0:
            result += convert_to_yellow(f"\n\nThe following blocks you mined are still pending since your last login: \n")
            for block in pending_mined_blocks:
                result += f"Block hash: {block.blockHash} \n"

    return result

def check_balance():
    total_in = 0
    total_out = 0

    chain = explore_chain() #Load all blocks in chain, (valid and pending).
    valid_transactions_pool = check_pool_valid_transactions() #Load all valid transactions in pool.

    for block in chain:
        for tx in block.data:
            for addr, amt in tx.inputs:
                if addr == Context.public_key:
                    total_in = total_in + amt
            for addr, amt in tx.outputs:
                if addr == Context.public_key:    
                    total_out = total_out + amt

    for tx in valid_transactions_pool:
        for addr, amt in tx.inputs:
            if addr == Context.public_key:
                total_in = total_in + amt
        for addr, amt in tx.outputs:
            if addr == Context.public_key:    
                total_out = total_out + amt

    return total_out - total_in

def get_current_password_hashed():
    con = Context.db_connection
    c = con.cursor()

    try:
        c.execute(
            "SELECT Password "
            "FROM   users "
            "WHERE  Name = ?"
            , (Context.user_name,))

        row = c.fetchone()
        if row is not None:
            return True, row[0]
        else:
            return False, "Error: Could not get current password."

    except IntegrityError as e:
        return False, str(e)

def update_password(new_password_hashed):
    con = Context.db_connection
    c = con.cursor()

    try:
        c.execute(
            "UPDATE users "
            "SET    Password = ? "
            "WHERE Name = ?"
            , (new_password_hashed, Context.user_name))

        if c.rowcount == 1:
            con.commit()
            return True, "Password updated."
        else:
            return False, "Error: Could not update password."

    except IntegrityError as e:
        return False, str(e)