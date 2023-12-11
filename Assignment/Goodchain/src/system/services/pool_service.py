import os
import pickle
import uuid

from src.system.context import Context
from src.system.blockchain.Transaction import MINERREWARD, MINERREWARD_VALUE, SIGNUP, Tx
from src.system.blockchain.TxBlock import VALID

def transfer_coins(recieverName, amountCoins, transactionFee):
    #Check if receiver exists.
    find_receiver = get_receiver_public_key(recieverName)

    if not find_receiver[0]:
        return False, "The receiver does not exist!"

    #Check if the receiver is not the sender.
    if recieverName == Context.user_name:
        return False, "You can't send coins to yourself!"
    
    #Check if sender has enough coins.
    check_balance_sender = check_balance()
    if check_balance_sender - amountCoins < 0:
        return False, "You don't have enough coins!"

    transaction_id = generate_random_transaction_id()

    newTx = Tx(transaction_id, Context.user_name, recieverName, transaction_fee = transactionFee)
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

def explore_chain_valid_blocks():
    blocks = []
    try:
        with open(Context.ledger_path, "rb") as f:
            while True:
                block = pickle.load(f)
                if block.status == VALID:
                    blocks.append(block)
    except EOFError:
        # No more lines to read from file.
        pass

    return blocks
    
def check_balance():
    #This function is used in transfer_coins to check if the sender has enough coins to send. There is also another check_balance, that one is used in the node menu to show the balance of the user.
    #This function is only showing the balance of the user in the chain for valid blocks, not pending blocks.
    total_in = 0
    total_out = 0

    chain = explore_chain_valid_blocks() #Load all valid blocks in chain (dont load PENDING blocks).

    for block in chain:
        for tx in block.data:
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

def check_pool_reward_transactions():
    reward_transactions = []
    try:
        with open(Context.pool_path, "rb") as f:
            while True:
                transaction = pickle.load(f)
                if (transaction.type == MINERREWARD or transaction.type == SIGNUP) and transaction.is_valid():
                    reward_transactions.append(transaction)
    except EOFError:
        # No more lines to read from file.
        pass

    return reward_transactions

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

def set_transactions_back_to_pool(block):
    #Return all transactions of the rejected block back to the pool
    #If the block is rejected because of some invalid transactions, those invalid transactions must be also flagged as invalid on the pool to be nullified by the creator of the transaction upon login. 
    # Other valid transactions in the rejected block must be returned to the pool, waiting for the next mining process to be included in a new block again.
    for transaction in block.data:
        if transaction.is_valid():
            transaction.set_valid()
        else:
            transaction.set_invalid()
        
        add_transaction_to_pool(transaction)

    block.data = []
    return block

def create_mining_reward(miner_of_block_name, total_fee_for_miner):
    find_receiver = get_receiver_public_key(miner_of_block_name)
    if not find_receiver[0]:
        return False, "The receiver does not exist!"
    
    total_reward_value = MINERREWARD_VALUE + float(total_fee_for_miner) #50.0 (Reward for mining) + total fee in transactions for the miner

    #Create transaction give miner reward
    tx = Tx(generate_random_transaction_id(), None, miner_of_block_name, MINERREWARD)
    tx.add_output(find_receiver[1], total_reward_value)
    tx.set_valid()

    savefile = open(Context.pool_path, "ab")
    pickle.dump(tx, savefile)
    savefile.close()