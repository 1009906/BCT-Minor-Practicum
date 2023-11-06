from datetime import datetime
from src.system.services.pool_service import add_transaction_to_pool, check_pool_invalid_transactions, create_mining_reward, remove_transaction_from_pool
from src.system.context import Context
from src.system.services.blockchain_service import find_block_to_validate, remove_block_in_chain, update_block_in_chain
from src.system.blockchain.TxBlock import INVALID, VALID

#Check the pool for invalid transactions of the logged in user and remove those from the pool.
def check_pool_for_invalid_transactions_of_logged_in_user():
    rejected_transactions = []
    get_all_invalid_transactions = check_pool_invalid_transactions()
    for transaction in get_all_invalid_transactions:
        if transaction.owner == Context.user_name:
            result = remove_transaction_from_pool(str(transaction.id))
            if result:
                #The invalid transaction is from the logged in user and is removed from the pool.
                rejected_transactions.append(transaction)
        else:
            #The invalid transaction is not from the logged in user.
            continue
        
    return rejected_transactions

def check_blockchain_for_block_to_validate():
    result = ""
    block_needs_to_be_removed = False
    block = find_block_to_validate()

    #Check if there are blocks to validate
    if block == None:
        return "During your login, there was no block to validate."
    
    updated_block = block

    if block.miner_of_block == Context.user_name:
        #Skip the block if the logged in user is the miner of the block
        return f"During your login, there was a block to validate, but you are the miner of the block. Block hash: {updated_block.blockHash}. The block still needs {3 - block.valid_counter} succesfull validations to be accepted."
    
    if Context.user_name in block.validated_by:
        #Skip the block if the logged in user has already validated the block
        return f"During your login, there was a block to validate, but you have already validated the block. Block hash: {updated_block.blockHash}."

    #Check if block is valid
    is_valid_block = block.is_valid()

    #If block is valid, flag it as valid
    if is_valid_block:
        updated_block.valid_counter += 1
        updated_block.validated_by.append(Context.user_name)

        #If block is validated by 3 different users, reward the miner
        if updated_block.valid_counter == 3:
            updated_block.status = VALID
            updated_block.creation_date = datetime.now()
            #Create a new transaction to the pool to reward the miner
            create_mining_reward(block.miner_of_block, block.total_fee_for_miner)
            result = f"By your login you accepted a new block to the chain. Block hash: {updated_block.blockHash}."
        else:
            result = f"By your login you increased the valid counter to {updated_block.valid_counter} of a block. Block hash: {updated_block.blockHash}. The block is not yet accepted."
        
        #Update the block in the ledger with the new status and other data
        update_block_in_chain(updated_block)
        
    #If block is invalid, flag it as invalid
    else:
        updated_block.invalid_counter += 1
        updated_block.validated_by.append(Context.user_name)

        #If block is rejected by 3 different users, return all transactions of the rejected block back to the pool and remove the block from the ledger
        if updated_block.invalid_counter == 3:
            updated_block.status = INVALID
            block_needs_to_be_removed = True

        if block_needs_to_be_removed:
            #Remove the block from the ledger and set transactions back to pool
            updated_block = set_transactions_back_to_pool(updated_block)
            remove_block_in_chain(updated_block)
            result = f"By your login you rejected a block. Block hash: {updated_block.blockHash}. The block was removed from the chain and the transactions were returned to the pool."
        else:
            #Update the block in the ledger with the new status and other data
            update_block_in_chain(updated_block)
            result = f"By your login you increased the invalid counter to {updated_block.invalid_counter} of a block. Block hash: {updated_block.blockHash}. The block is not yet rejected."

    return result

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