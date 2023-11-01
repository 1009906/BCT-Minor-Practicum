from src.system.services.pool_service import check_pool_invalid_transactions, remove_transaction_from_pool
from src.system.context import Context

#Check the pool for invalid transactions of the logged in user and remove those from the pool.
def check_pool_for_invalid_transactions_of_logged_in_user():
    get_all_invalid_transactions = check_pool_invalid_transactions()
    for transaction in get_all_invalid_transactions:
        if transaction.owner == Context.user_name:
            remove_transaction_from_pool(str(transaction.id))
        else:
            #The invalid transaction is not from the logged in user.
            continue
