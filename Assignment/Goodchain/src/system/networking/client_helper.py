from src.system.networking.database_client import DatabaseClient
from src.system.networking.miner_client import MinerClient
from src.system.networking.wallet_client import WalletClient

# WalletClient
def create_wallet_client_and_send_transaction(transaction, client_name = None):
    wallet_client = WalletClient()
    wallet_client.handle_server_send_tx(transaction, client_name)

def create_wallet_client_and_send_remove_txs(tx_ids, client_name = None):
    wallet_client = WalletClient()
    wallet_client.handle_server_send_remove_txs(tx_ids, client_name)

def create_wallet_client_and_send_set_invalid_txs(tx_ids, client_name = None):
    wallet_client = WalletClient()
    wallet_client.handle_server_send_set_invalid_txs(tx_ids, client_name)

# MinerClient
def create_miner_client_and_send_block(block):
    miner_client = MinerClient()
    miner_client.handle_server(block)

# DatabaseClient
def create_database_client_and_send_test_message(client_name = None): #TODO remove
    database_client = DatabaseClient()
    database_client.handle_server(client_name)