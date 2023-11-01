from src.system.services.pool_service import check_pool_invalid_transactions, create_mining_reward, remove_transaction_from_pool
from src.system.context import Context
from src.system.services.blockchain_service import find_blocks_to_validate, update_block_in_chain
from src.system.blockchain.TxBlock import INVALID, VALID

#Check the pool for invalid transactions of the logged in user and remove those from the pool.
def check_pool_for_invalid_transactions_of_logged_in_user():
    get_all_invalid_transactions = check_pool_invalid_transactions()
    for transaction in get_all_invalid_transactions:
        if transaction.owner == Context.user_name:
            remove_transaction_from_pool(str(transaction.id))
        else:
            #The invalid transaction is not from the logged in user.
            continue

"""
TODO:
Once a block is created by a node, the next three logged in users (nodes) must check the validity of the created block. 
These nodes will fully check the block to ensure a valid block is created by the miner. If the block is valid, they flag it as valid, otherwise they flag it as invalid.

■ If the new block is flagged as valid by these three nodes (three different logged in users), then the third validator node is responsible to create a new transaction to reward the miner of the block. 
This reward transaction could be included in the next mining process. If a block successfully got validated by three other nodes, it does not need to be validated by any other nodes later. 
(Note that the block cannot be validated by the creator of the block.)

■ If the new block is flagged as invalid (rejected) by at least three other nodes, before getting three valid flags, then the third rejector node is also responsible to return all the transactions of the rejected block back to the pool. 
In this case, if the block is rejected because of some invalid transactions, those invalid transactions must be also flagged as invalid on the pool to be nullified by the creator of the transaction upon login. 
Other valid transactions in the rejected block must be returned to the pool, waiting for the next mining process to be included in a new block again. 
"""
def check_blockchain_for_blocks_to_validate():
    blocks_to_validate = find_blocks_to_validate()

    #Check if there are blocks to validate
    if len(blocks_to_validate) <= 0:
        return
    
    for block in blocks_to_validate:
        block_needs_to_be_removed = False
        updated_block = block

        if block.miner_of_block == Context.user_name:
            #Skip the block if the miner of the block is the logged in user
            continue

        #Check if block is valid
        is_valid_block = block.is_valid()

        #If block is valid, flag it as valid
        if is_valid_block:
            updated_block.valid_counter += 1
            updated_block.validated_by.append(Context.user_name)

            #If block is validated by 3 different users, reward the miner
            if updated_block.valid_counter == 3:
                updated_block.status = VALID
                #Create a new transaction to the pool to reward the miner
                create_mining_reward(block.miner_of_block, block.total_fee_for_miner)
            
            #Update the block in the ledger with the new status and other data
            update_block_in_chain(updated_block)
            
        #TODO If block is invalid, flag it as invalid
        else:
            updated_block.invalid_counter += 1
            updated_block.validated_by.append(Context.user_name)

            #TODO If block is rejected by 3 different users, return all transactions of the rejected block back to the pool
            if updated_block.invalid_counter == 3:
                updated_block.status = INVALID
                block_needs_to_be_removed = True
                #TODO Return all transactions of the rejected block back to the pool
                #TODO if the block is rejected because of some invalid transactions, those invalid transactions must be also flagged as invalid on the pool to be nullified by the creator of the transaction upon login. 
                # Other valid transactions in the rejected block must be returned to the pool, waiting for the next mining process to be included in a new block again.

            #TODO Update the block in the ledger with the new status and other data
            #TODO If the block is set to invalid 3 times, remove the block from the ledger. LET OP! Het kan zijn dat er al een ander block vast zit aan dit block dat verwijderd wordt. Dus dat gaat dan fout met de hash van previousblock en previousblock variable.
            if block_needs_to_be_removed:
                #TODO Remove the block from the ledger
                print() #TODO Deze print weghalen.
            else:
                update_block_in_chain(updated_block)
