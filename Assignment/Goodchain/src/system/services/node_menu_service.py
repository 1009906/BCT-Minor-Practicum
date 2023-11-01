from datetime import datetime
import os
from sqlite3 import IntegrityError
from src.system.context import Context
from src.system.blockchain.Transaction import Tx
from src.system.blockchain.TxBlock import TxBlock
import pickle
import uuid

def update_last_login_date():
    con = Context.db_connection
    c = con.cursor()

    try:
        c.execute(
            "UPDATE users "
            "SET    LastLogin = ? "
            "WHERE Name = ?"
            , (datetime.now(), Context.user_name))

        if c.rowcount == 1:
            con.commit()
            return True, "User updated."
        else:
            return False, "Error: Could not update user."

    except IntegrityError as e:
        return False, str(e)

def transfer_coins(recieverName, amountCoins, transactionFee):
    #Check if receiver exists.
    find_receiver = get_receiver_public_key(recieverName)
    if not find_receiver[0]:
        return False, "The receiver does not exist!"
    
    #Check if the receiver is not the sender.
    if recieverName == Context.user_name:
        return False, "You can't send coins to yourself!"
    
    #TODO Check of de sender genoeg coins heeft
    transaction_id = generate_random_transaction_id()

    newTx = Tx(transaction_id, Context.user_name, transaction_fee = transactionFee)
    newTx.add_input(Context.public_key, amountCoins)
    newTx.add_output(find_receiver[1], amountCoins) 
    newTx.sign(Context.private_key)

    if newTx.is_valid():
        #Transaction is valid
        newTx.set_valid()
        savefile = open(Context.pool_path, "ab")
        pickle.dump(newTx, savefile)
        savefile.close()
        return True, "Transaction is valid! (added to the pool)"
    else:
        #Transaction is not valid
        return False, "Transaction is invalid! (not added to the pool)"
    
def get_receiver_public_key(recieverName):
    con = Context.db_connection
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE Name=?", [recieverName])
    user_result = c.fetchone()

    if user_result:
        return True, user_result[3]
    else:
        return False, None
    
def generate_random_transaction_id():
    return uuid.uuid1()
    
def check_pool():
    transactions = []
    try:
        with open(Context.pool_path, "rb") as f:
            while True:
                transaction = pickle.load(f)
                transactions.append(transaction)
    except EOFError:
        # No more lines to read from file.
        pass

    return transactions

def check_pool_valid_transactions():
    valid_transactions = []
    try:
        with open(Context.pool_path, "rb") as f:
            while True:
                transaction = pickle.load(f)
                if transaction.is_valid_transaction and transaction.is_valid():
                    valid_transactions.append(transaction)
    except EOFError:
        # No more lines to read from file.
        pass

    return valid_transactions

def load_transaction_by_id(transaction_id):
    try:
        with open(Context.pool_path, "rb") as f:
            while True:
                transaction = pickle.load(f)
                if str(transaction.id) == transaction_id:
                    return transaction
    except EOFError:
        # No more lines to read from file.
        pass

    return None

def explore_chain():
    blocks = []
    try:
        with open(Context.ledger_path, "rb") as f:
            while True:
                block = pickle.load(f)
                blocks.append(block)
    except EOFError:
        # No more lines to read from file.
        pass

    return blocks

def cancel_transaction_from_pool(transaction_id):
    transaction_is_removed = False
    with open(Context.pool_path, "rb") as original_file, open(Context.temp_pool_path, "wb") as temp_file:
        try:
            while True:
                transaction = pickle.load(original_file)
                if str(transaction.id) == transaction_id and transaction.owner == Context.user_name:
                    # Skip this transaction
                    transaction_is_removed = True
                    continue
                pickle.dump(transaction, temp_file)
        except EOFError:
            pass
        
    # Replace the original pool file with the temporary file
    os.remove(Context.pool_path)
    os.rename(Context.temp_pool_path, Context.pool_path)

    return transaction_is_removed

def remove_transaction_from_pool(transaction_id):
    transaction_is_removed = False
    with open(Context.pool_path, "rb") as original_file, open(Context.temp_pool_path, "wb") as temp_file:
        try:
            while True:
                transaction = pickle.load(original_file)
                if str(transaction.id) == transaction_id:
                    # Skip this transaction
                    transaction_is_removed = True
                    continue
                pickle.dump(transaction, temp_file)
        except EOFError:
            pass
        
    # Replace the original pool file with the temporary file
    os.remove(Context.pool_path)
    os.rename(Context.temp_pool_path, Context.pool_path)

    return transaction_is_removed

def set_transaction_to_invalid_in_pool(transaction_id):
    transaction_set_invalid = False
    with open(Context.pool_path, "rb") as original_file, open(Context.temp_pool_path, "wb") as temp_file:
        try:
            while True:
                transaction = pickle.load(original_file)
                if str(transaction.id) == transaction_id:
                    # Set transaction to invalid
                    transaction.set_invalid()
                    transaction_set_invalid = True
                pickle.dump(transaction, temp_file)
        except EOFError:
            pass
        
    # Replace the original pool file with the temporary file
    os.remove(Context.pool_path)
    os.rename(Context.temp_pool_path, Context.pool_path)

    return transaction_set_invalid

def mine_new_block(transaction_ids):
    transactions_to_add = [] #Add to block
    transactions_to_remove = [] #Remove from pool
    transactions_to_set_invalid = [] #Set invalid in pool

    for transaction_id in transaction_ids:
        #Load transaction by id and Check if transaction is valid
        transaction = load_transaction_by_id(transaction_id)
        if transaction:
            if transaction.is_valid():
                transactions_to_add.append(transaction)
                transactions_to_remove.append(str(transaction.id))
            else:
                transactions_to_set_invalid.append(str(transaction.id))

    #Check if there is a previousBlock in the chain. If not, create a genesis block.
    get_chain = explore_chain()
    if len(get_chain) == 0:
        #Create genesis block
        newBlock = TxBlock(None)
    else:
        last_block = get_chain[-1]
        #Create new block
        newBlock = TxBlock(last_block)

    #Add transactions to block
    for transaction in transactions_to_add:
        newBlock.addTx(transaction)

    #Find nonce for block
    newBlock.find_nonce()

    #Add block to ledger
    savefile = open(Context.ledger_path, "ab")
    pickle.dump(newBlock, savefile)
    savefile.close()

    #Remove transactions from pool
    for transaction_id in transactions_to_remove:
        remove_transaction_from_pool(transaction_id)
    
    #Set transactions to invalid in pool
    for transaction_id in transactions_to_set_invalid:
        set_transaction_to_invalid_in_pool(transaction_id)