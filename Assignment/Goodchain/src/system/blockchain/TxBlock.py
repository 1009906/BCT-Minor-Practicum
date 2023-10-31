from src.system.blockchain.BlockChain import CBlock
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

REWARD_VALUE = 25.0
leading_zeros = 2
next_char_limit = 20

class TxBlock (CBlock):

    def __init__(self, previousBlock):
        # self.nonce = "A random nonce"
        self.nonce = 0
        super(TxBlock, self).__init__([], previousBlock)
        # TODO toevoegen van een counter voor het aantal keer validaten door ingelogde gebruikers (valid counter)
        self.valid_counter = 0
        # TODO toevoegen van een counter voor het aantal keer validaten door ingelogde gebruikers (invalid counter)
        self.invalid_counter = 0
        # TODO AssignedToPreviousBlock toevoegen aan de TxBlock class boolean
        self.assigned_to_previous_block = False
        # TODO MinerOfBlock toevoegen aan de TxBlock class string, die kan je pakken uit context.user_name
        self.miner_of_block = None

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def __count_totals(self):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr, amt in tx.inputs:
                total_in = total_in + amt
            for addr, amt in tx.outputs:
                total_out = total_out + amt
        return total_in, total_out

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        
        total_in, total_out = self.__count_totals()
        
        Tx_Balance = round(total_out - total_in, 10)
        
        if Tx_Balance > REWARD_VALUE:
            return False
        return True
    
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        digest.update(bytes(str(self.nonce),'utf8'))
        return digest.finalize()

    def good_nonce(self, new_hash = None):
        if new_hash is None:
            new_hash = self.computeHash()
        if new_hash.startswith(b'0' * leading_zeros):
            return True
        else:
            return False

    def find_nonce(self):
        while True:
            hashTry = self.computeHash()
            # print(self.nonce, hashTry)
            if self.good_nonce(hashTry):
                print(f"Nonce found: {self.nonce}")
                self.blockHash = hashTry
                return hashTry
            
            self.nonce += 1
    
    def __repr__(self):
        #TODO Check what we want to represent
        repr_str = super().__repr__()
        repr_str += "Nonce: " + str(self.nonce) + "\n"
        repr_str += "END\n"
        return repr_str
        

    #TODO REMOVE THIS CODE is van Chris
    # def good_nonce(self):
    #     if self.nonce is None:
    #         return False

    #     # Check if the hash of the block with the current nonce has the required number of leading zeros
    #     self.blockHash = self.computeHash()
    #     prefix = self.blockHash[:2]
    
    #     # Check if the first 2 bytes are '0' and the 3rd byte is less than possibilities_for_leading_byte (0 to possibilities_for_leading_byte)
    #     if prefix.startswith(b'0' * leading_zeros):
    #         return True

    #     return False

    # def find_nonce(self):
    #     while True:
    #         # Generate a random nonce (or you can implement a more sophisticated nonce generation strategy)
    #         self.nonce = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=next_char_limit))
    #         #self.nonce = non.encode('utf-8')
    #         #print(self.nonce)
    #         # Check if the current nonce results in a valid block
    #         if self.good_nonce():
    #             return self.nonce  