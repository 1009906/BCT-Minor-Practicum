from datetime import datetime
import os
import pickle
from src.system.context import Context
from src.system.blockchain.TxBlock import PENDING, VALID, TxBlock
from src.system.services.pool_service import check_pool_reward_transactions, check_pool_valid_transactions, load_transaction_by_id, remove_transaction_from_pool, set_transaction_to_invalid_in_pool, set_transactions_back_to_pool
from src.system.util.time_util import difference_in_minutes

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

def tamper_proof_check():
    blocks = explore_chain()
    for block in blocks:
        if block.is_valid() == False:
            return True, "The chain is tamperd. The block with hash: " + str(block.blockHash) + " is not valid!"
        
    return False, "The chain is not tamperd."

def find_last_block_in_chain():
    last_block = None
    try:
        with open(Context.ledger_path, "rb") as f:
            while True:
                block = pickle.load(f)
                last_block = block
    except EOFError:
        # No more lines to read from file.
        pass

    return last_block

def explore_chain_since_date(date):
    blocks = []
    try:
        with open(Context.ledger_path, "rb") as f:
            while True:
                block = pickle.load(f)
                if block.creation_date > date:
                    blocks.append(block)
    except EOFError:
        # No more lines to read from file.
        pass

    return blocks

def succesfull_transactions_since_date(date, transaction_owner):
    transactions = []
    try:
        with open(Context.ledger_path, "rb") as f:
            while True:
                block = pickle.load(f)
                if block.creation_date > date:
                    for transaction in block.data:
                        if transaction.owner == transaction_owner:
                            transactions.append(transaction)
    except EOFError:
        # No more lines to read from file.
        pass

    return transactions

def get_information_of_chain():
    blocks = explore_chain()
    amount_of_blocks = len(blocks)
    amount_of_transactions = 0
    for block in blocks:
        amount_of_transactions += len(block.data)
    return amount_of_blocks, amount_of_transactions

def find_block_to_validate():
    block_to_validate = None
    try:
        with open(Context.ledger_path, "rb") as f:
            while True:
                block = pickle.load(f)
                if block.status == PENDING:
                    block_to_validate = block
    except EOFError:
        # No more lines to read from file.
        pass

    return block_to_validate

def find_block_to_validate_by_hash(block_hash_to_validate):
    block_to_validate = None
    try:
        with open(Context.ledger_path, "rb") as f:
            while True:
                block = pickle.load(f)
                if str(block.blockHash) == block_hash_to_validate:
                    block_to_validate = block
    except EOFError:
        # No more lines to read from file.
        pass

    return block_to_validate

def check_possibility_to_mine():
    #Check if there is no block in pending state.
    find_pending_block = find_block_to_validate()
    if find_pending_block is not None:
        return False, "There is still a block in pending state! Please wait until it is validated."
    
    #No blocks are in pending state.
    if find_pending_block is None:
        last_block = find_last_block_in_chain()
        if last_block is not None:
            #Last block is found. Check if there is a time difference of 3 minutes between the last block and now.
            time_difference_minutes = difference_in_minutes(last_block.creation_date, datetime.now())
            if time_difference_minutes < 3:
                return False, "You can only mine a block every 3 minutes!"
            
    return True, "You can mine a new block!"

def mine_new_block(transaction_ids, amount_of_transactions_user_want_to_add):
    try:
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

        #Remove transactions from pool, the user choose to add to the block
        for transaction_id in transactions_to_remove:
            remove_transaction_from_pool(transaction_id)

        transactions_to_remove = [] #Reset list
        
        #Set transactions to invalid in pool the user choose to add to the block
        for transaction_id in transactions_to_set_invalid:
            set_transaction_to_invalid_in_pool(transaction_id)

        #Check if there are reward transactions in the pool (signup or mining reward). Priority to add reward transactions to the block
        get_reward_transactions_from_pool = check_pool_reward_transactions() #Gets all reward and valid transactions from the pool
        if len(get_reward_transactions_from_pool) > 0:
            for transaction in get_reward_transactions_from_pool:
                if len(newBlock.data) < amount_of_transactions_user_want_to_add:
                    newBlock.addTx(transaction)
                    transactions_to_remove.append(str(transaction.id))
                    total_fee_for_miner += transaction.transaction_fee
                else:
                    break

        #Remove added reward transactions from pool
        for transaction_id in transactions_to_remove:
            remove_transaction_from_pool(transaction_id)

        transactions_to_remove = [] #Reset list

        #Check if there are valid transactions in the pool
        #Add transactions to block with a maximum of amount_of_transactions_user_want_to_add transactions in the block
        get_valid_transactions_from_pool = check_pool_valid_transactions()
        if len(get_valid_transactions_from_pool) > 0:
            for transaction in get_valid_transactions_from_pool:
                if len(newBlock.data) < amount_of_transactions_user_want_to_add:
                    newBlock.addTx(transaction)
                    transactions_to_remove.append(str(transaction.id))
                    total_fee_for_miner += transaction.transaction_fee
                else:
                    break

        #Remove later added transactions from pool
        for transaction_id in transactions_to_remove:
            remove_transaction_from_pool(transaction_id)

        #Find nonce for block
        amount_of_transactions = len(newBlock.data)
        newBlock.find_nonce(amount_of_transactions)

        #Set miner of the block
        newBlock.miner_of_block = Context.user_name

        #Set total fee for miner
        newBlock.total_fee_for_miner = total_fee_for_miner

        new_block_is_valid = newBlock.is_valid()
        if new_block_is_valid == False:
            set_transactions_back_to_pool(newBlock)
            return False, "The new block is not valid!"

        #Add block to ledger
        savefile = open(Context.ledger_path, "ab")
        pickle.dump(newBlock, savefile)
        savefile.close()
        
        return True, "New block is created and added to the chain, waiting for validation."
    
    except Exception:
        return False, "Error occurred while creating a new block."

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