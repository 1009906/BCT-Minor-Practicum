from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class CBlock:

    data = None
    previousHash = None
    previousBlock = None
    nonce = None
    def __init__(self, data, previousBlock):
        self.data = data
        self.blockHash = None
        self.previousBlock = previousBlock
        self.nonce = 0
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()
    
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        digest.update(str(self.nonce).encode('utf-8'))
        return digest.finalize()

    def is_valid(self):
        if self.previousBlock == None:
            return True
        return self.previousBlock.computeHash() == self.previousHash
    
    def __repr__(self):
        #TODO: Implement this function to return the data stored inside the block.
        pass
    