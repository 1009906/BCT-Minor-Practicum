import pickle
from src.system.context import Context
from src.system.blockchain.TxBlock import TxBlock
from src.system.services.pool_service import load_transaction_by_id, remove_transaction_from_pool, set_transaction_to_invalid_in_pool

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