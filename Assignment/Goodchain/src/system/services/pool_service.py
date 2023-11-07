import os
import pickle
import uuid

from src.system.context import Context
from src.system.blockchain.Transaction import MINERREWARD, Tx

def transfer_coins(recieverName, amountCoins, transactionFee, transfer_method):
    #Check if receiver exists.
    #Check if user wants to use public key or username. (1) username, (2) public key
    if transfer_method == "1":
        find_receiver = get_receiver_public_key(recieverName)
    elif transfer_method == "2" and check_public_key_exists(recieverName):
        find_receiver = (True, recieverName)
    else:
        find_receiver = (False, "The receiver does not exist!")

    if not find_receiver[0]:
        return False, "The receiver does not exist!"
    
    #Check if the receiver is not the sender.
    if recieverName == Context.user_name:
        return False, "You can't send coins to yourself!"
    
    #Check if sender has enough coins.
    # check_balance_sender = check_balance()
    # if check_balance_sender - amountCoins < 0:
    #     return False, "You don't have enough coins!"

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
    
def check_public_key_exists(public_key):
    con = Context.db_connection
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE PublicKey=?", [public_key])
    user_result = c.fetchone()

    if user_result:
        return True
    else:
        return False
    
def explore_blocks_in_chain():
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
    
def check_balance():
    total_in = 0
    total_out = 0

    chain = explore_blocks_in_chain() #Load all blocks in chain, (valid and pending).
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
    
def get_receiver_public_key(recieverName):
    con = Context.db_connection
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE Name=?", [recieverName])
    user_result = c.fetchone()

    if user_result:
        return True, user_result[4]
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

def check_pool_invalid_transactions():
    invalid_transactions = []
    try:
        with open(Context.pool_path, "rb") as f:
            while True:
                transaction = pickle.load(f)
                if not transaction.is_valid_transaction or not transaction.is_valid():
                    invalid_transactions.append(transaction)
    except EOFError:
        # No more lines to read from file.
        pass

    return invalid_transactions

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

def find_last_transaction_in_pool():
    last_transaction = None
    try:
        with open(Context.pool_path, "rb") as f:
            while True:
                transaction = pickle.load(f)
                last_transaction = transaction
    except EOFError:
        # No more lines to read from file.
        pass

    return last_transaction

def add_transaction_to_pool(transaction):
    try:
        savefile = open(Context.pool_path, "ab")
        pickle.dump(transaction, savefile)
        savefile.close()
        return True
    except:
        return False

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

def create_mining_reward(miner_of_block_name, total_fee_for_miner):
    find_receiver = get_receiver_public_key(miner_of_block_name)
    if not find_receiver[0]:
        return False, "The receiver does not exist!"
    
    #Create transaction give miner reward
    tx = Tx(generate_random_transaction_id(), None, MINERREWARD)
    tx.add_output(find_receiver[1], float(total_fee_for_miner))
    tx.set_valid()

    savefile = open(Context.pool_path, "ab")
    pickle.dump(tx, savefile)
    savefile.close()