#TODO Deze service implementeren om alles over het netwerk te handelen.
from src.system.blockchain.TxBlock import VALID
from src.system.services.blockchain_service import add_block_to_ledger
from src.system.services.pool_service import add_transaction_to_pool
from src.system.context import Context

def process_received_transaction(transaction):
    result = False, transaction

    if transaction.is_valid():
        transaction.set_valid()
        adding_result = add_transaction_to_pool(transaction)
        
        if adding_result:
            result = True, transaction
        else:
            result = False, transaction

    return result

def process_received_block(block):
    result = False, block

    if block.is_valid():
        block.status = VALID
        block.valid_counter += 1
        block.validated_by.append(Context.current_node)

        adding_result = add_block_to_ledger(block)
        
        if adding_result:
            result = True, block
        else:
            result = False, block

    return result