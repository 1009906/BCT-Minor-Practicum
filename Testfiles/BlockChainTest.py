from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class Block:
    def __init__(self, index, previous_hash, data, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce

    def calculate_hash(self):
        data = str(self.index) + str(self.previous_hash) + str(self.data) + str(self.nonce)
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data.encode())
        return digest.finalize()

def mine_block(previous_block, data):
    index = previous_block.index + 1
    previous_hash = previous_block.calculate_hash()
    nonce = 0

    while True:
        block = Block(index, previous_hash, data, nonce)
        hash_result = block.calculate_hash()
        print(hash_result)
        if hash_result[:4] == b'\x00\x00\x00\x00':  # Adjust difficulty by changing number of leading zeros
            return block
        nonce += 1

def validate_block(previous_block, block):
    if block.index != previous_block.index + 1:
        return False
    if block.previous_hash != previous_block.calculate_hash():
        return False
    if block.calculate_hash()[:4] != b'\x00\x00\x00\x00':  # Adjust difficulty here as well
        return False
    return True

# Example usage:
genesis_block = Block(0, b'genesis', 'Genesis Block', 0)
block1 = mine_block(genesis_block, 'Block 1 Data')
print(f"Block 1: Index {block1.index}, Nonce {block1.nonce}, Previous Hash {block1.previous_hash.hex()}")
print(f"Valid: {validate_block(genesis_block, block1)}")
