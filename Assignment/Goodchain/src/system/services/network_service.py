#TODO Deze service implementeren om alles over het netwerk te handelen.
from src.system.services.pool_service import add_transaction_to_pool

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