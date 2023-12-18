#TODO Deze service implementeren om alles over het netwerk te handelen.
def process_received_transaction(transaction):
    result = False
    if transaction.is_valid():
        result = True

    return result