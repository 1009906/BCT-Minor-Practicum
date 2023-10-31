import os
from src.system.context import Context
from src.system.blockchain.Transaction import Tx
from src.system.blockchain.TxBlock import TxBlock
import pickle
import uuid

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
                if transaction.is_valid_transaction:
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

def remove_transaction_from_pool(transaction_id):
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

def mine_new_block(transaction_ids):
    # During this process, a miner will check the transactions and validate them.
    # Any invalid transaction must be flagged as invalid, in the pool. 
    # The miner will then create a new block with the valid transactions.
    # The miner will then add the block to the ledger.
    # The miner will then remove the transactions from the pool.

    transactions_to_add = [] #Add to block
    transactions_to_remove = [] #Remove from pool
    transactions_to_set_invalid = [] #Set invalid in pool

    for transaction_id in transaction_ids:
        #TODO Load transaction by id and Check if transaction is valid
        transaction = load_transaction_by_id(transaction_id)
        if transaction:
            if transaction.is_valid():
                transactions_to_add.append(transaction)
                transactions_to_remove.append(str(transaction.id))
            else:
                transactions_to_set_invalid.append(transaction) #TODO Hele transactie of alleen id?
        else:
            #TODO Transaction not found
            pass

    #TODO Check if there are enough transactions in transactions_to_add, otherwise add from pool?
    #TODO Check if there is a previousBlock in the chain. If not, create a genesis block.

    #TODO Create new block
    newBlock = TxBlock(None)

    #TODO Add transactions to block
    for transaction in transactions_to_add:
        newBlock.addTx(transaction)

    #TODO find nonce for block
    newBlock.find_nonce()

    #TODO Add block to ledger
    savefile = open(Context.ledger_path, "wb") #TODO Check if this needs to be append 'ab', with the pool we use append 
    pickle.dump(newBlock, savefile)
    savefile.close()

    #TODO Remove transactions from pool
    for transaction_id in transactions_to_remove:
        remove_transaction_from_pool(transaction_id)
    
    #TODO Set transactions to invalid in pool
    