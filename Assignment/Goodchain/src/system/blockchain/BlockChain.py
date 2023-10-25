from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from src.system.services.node_menu_service import check_pool
from src.system.blockchain.TxBlock import TxBlock

class CBlock:    
    previousBlock = None
    previousHash = None
    data = None
    nonce = 0
    blockHash = None

    # Initialize the values of a block
    # Make sure you distinguish between the genesis block and other blocks
    def __init__(self, data, previousBlock=None):
        self.data = data
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = (CBlock)(previousBlock).computeHash()


    # Compute the cryptographic hash of the current block. 
    # Be sure which values must be considered to compute the hash properly.
    # return the digest value
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(self.data if isinstance(self.data, bytes) else str(self.data).encode('utf-8'))

        if (self.previousHash != None):
            digest.update(str(self.previousHash).encode('utf-8'))
        else:
            digest.update("Genesis".encode('utf-8'))

        digest.update(str(self.nonce).encode('utf-8'))

        return digest.finalize() 
    
    # Mine the current value of a block
    # Calculates a digest based on required values from the block, such as:
    # data, previousHash, nonce
    # Make sure to compute the hash value of the current block and store it properly 
    def mine(self, leading_zeros):
        # create TxBlock if there are 5 or more transactions in pooltx.dat file
        pool_tx = check_pool()
        # TODO check blocks and get last block in the chain. 
        tx_block = TxBlock()
        if len(pool_tx) >= 5:
            for index in range(10):
                if pool_tx[index] != None:

                    self.addTx(pool_tx[index])
                if index == len(pool_tx) - 1:   
                    break


        while True:
            hashTry = self.computeHash()
            if hashTry.startswith(b'0' * leading_zeros):
                print(self.nonce)
                self.blockHash = hashTry
                return hashTry
            
            self.nonce += 1
    
    # Check if the current block contains valid hash digest values 
    # Make sure to distinguish between the genesis block and other blocks
    # Make sure to compare both hash digest values:
    # The computed digest of the current block
    # The stored digest of the previous block
    # return the result of all comparisons as a boolean value 
    def is_valid_hash(self):
        return self.computeHash() == self.blockHash and (self.previousHash == None or self.previousBlock.is_valid_hash())