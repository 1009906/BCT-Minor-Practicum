from datetime import datetime
from sqlite3 import IntegrityError
from src.system.context import Context
from src.system.blockchain.TxBlock import PENDING, VALID

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
    #TODO: Nadenken over of dat we de creationdate van een block updaten als die van pending naar valid gaat.
    # Nu komt namelijk een transactie die van pending naar valid gaat niet in de lijst erbij.
    result = ""
    valid_mined_blocks = []
    pending_mined_blocks = []

    if len(blocks_added_since_last_login) == 0:
        result += "No blocks that you mined were added to the chain since your last login."
    else:
        for block in blocks_added_since_last_login:
            if block.status == VALID and block.miner_of_block == user_name:
                valid_mined_blocks.append(block)
            if block.status == PENDING and block.miner_of_block == user_name:
                pending_mined_blocks.append(block)
        
        if len(valid_mined_blocks) > 0:
            result += f"The following blocks you mined were added to the chain since your last login: \n"
            for block in valid_mined_blocks:
                result += f"Block hash: {block.blockHash} \n"

        if len(pending_mined_blocks) > 0:
            result += f"\n\nThe following blocks you mined are still pending since your last login: \n"
            for block in pending_mined_blocks:
                result += f"Block hash: {block.blockHash} \n"

    return result