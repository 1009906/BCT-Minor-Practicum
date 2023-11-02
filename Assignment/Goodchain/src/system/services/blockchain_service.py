import os
import pickle
from src.system.context import Context
from src.system.blockchain.TxBlock import PENDING, TxBlock
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

def find_blocks_to_validate():
    blocks_to_validate = []
    try:
        with open(Context.ledger_path, "rb") as f:
            while True:
                block = pickle.load(f)
                if block.status == PENDING:
                    blocks_to_validate.append(block)
    except EOFError:
        # No more lines to read from file.
        pass

    return blocks_to_validate


def mine_new_block(transaction_ids):
    total_fee_for_miner = 0
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
                total_fee_for_miner += transaction.transaction_fee
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

    #Set miner of the block
    newBlock.miner_of_block = Context.user_name

    #Set total fee for miner
    newBlock.total_fee_for_miner = total_fee_for_miner

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

def update_block_in_chain(updated_block):
    block_updated = False
    try:
        with open(Context.ledger_path, "rb") as original_file, open(Context.temp_ledger_path, "wb") as temp_file:
            try:
                while True:
                    block = pickle.load(original_file)
                    if str(block.blockHash) == str(updated_block.blockHash):
                        # Update the block
                        pickle.dump(updated_block, temp_file)
                        block_updated = True
                    else:
                        pickle.dump(block, temp_file)
            except EOFError:
                pass
    except EOFError:
        # No more lines to read from file.
        pass

    # Replace the original ledger file with the temporary file
    os.remove(Context.ledger_path)
    os.rename(Context.temp_ledger_path, Context.ledger_path)

    return block_updated

def remove_block_in_chain(block_to_remove):
    block_removed = False
    try:
        with open(Context.ledger_path, "rb") as original_file, open(Context.temp_ledger_path, "wb") as temp_file:
            while True:
                block = pickle.load(original_file)
                if str(block.blockHash) == str(block_to_remove.blockHash):
                    # Skip this block
                    block_removed = True
                    continue
                pickle.dump(block, temp_file)
    except EOFError:
        # No more lines to read from file.
        pass

    # Replace the original ledger file with the temporary file
    os.remove(Context.ledger_path)
    os.rename(Context.temp_ledger_path, Context.ledger_path)

    return block_removed