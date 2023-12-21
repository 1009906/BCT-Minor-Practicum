from src.system.networking.miner_client import MinerClient
from src.system.networking.wallet_client import WalletClient

def create_wallet_client_and_send_transaction(transaction, client_name = None):
    wallet_client = WalletClient()
    wallet_client.handle_server(transaction, client_name)

def create_miner_client_and_send_block(block):
    miner_client = MinerClient()
    miner_client.handle_server(block)