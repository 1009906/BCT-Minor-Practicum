import os
from src.system.context import Context
from src.system.blockchain.Transaction import Tx
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

    newTx = Tx(transaction_id, Context.user_name)
    newTx.add_input(Context.public_key, amountCoins)
    newTx.add_output(find_receiver[1], amountCoins) 
    newTx.sign(Context.private_key)

    if newTx.is_valid():
        #Transaction is valid
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

