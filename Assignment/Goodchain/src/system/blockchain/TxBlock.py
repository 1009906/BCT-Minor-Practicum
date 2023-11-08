import secrets
from src.system.blockchain.BlockChain import CBlock
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from datetime import datetime
from src.user_interface.util.stopwatch import Stopwatch

REWARD_VALUE = 25.0
leading_zeros = 2
next_char_limit = 20

VALID = "VALID"
INVALID = "INVALID"
PENDING = "PENDING"

class TxBlock (CBlock):

    def __init__(self, previousBlock):
        self.nonce = secrets.randbelow(2**256)
        super(TxBlock, self).__init__([], previousBlock)
        self.valid_counter = 0
        self.invalid_counter = 0
        self.validated_by = []
        self.status = PENDING
        self.miner_of_block = None
        self.total_fee_for_miner = 0
        self.creation_date = datetime.now()


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
        
        #TODO Check wat reward value is nu is tx balance 250 en reward value 25 waardoor die false returned
        if Tx_Balance > REWARD_VALUE:
            return False
        return True
    
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        digest.update(bytes(str(self.nonce),'utf8'))
        return digest.finalize()

    def good_nonce(self, new_hash = None, adjusted_third_char = 16):
        if new_hash is None:
            new_hash = self.computeHash()

        if new_hash.startswith(b'0' * leading_zeros) and new_hash[leading_zeros] <= adjusted_third_char:
            return True
        else:
            return False
        
        # bytes(str(message), 'utf-8')
        
    def find_nonce(self):
        stopwatch = Stopwatch()
        stopwatch.start()
        third_char = 8
        hashTry = self.computeHash()
        interval = 2
        while not self.good_nonce(hashTry, third_char):
            self.nonce = secrets.randbelow(2**256)
            hashTry = self.computeHash()
            if stopwatch.get_elapsed_time() > interval:
                print("Interval: ", interval) #TODO deze prints verwijderen
                print("Third char: ", third_char)
                print("Elapsed time: ", stopwatch.get_elapsed_time())
                third_char = third_char * 2 if third_char * 2 <= 256 else 256
                interval += 2
            
        #Hier komt die als de nonce goed is
        self.blockHash = hashTry
        print(hashTry, self.nonce)
        stopwatch.stop()
        stopwatch.print_elapsed_time()

        return hashTry, self.nonce #Maakt niet uit, doen we toch niks mee.

    #TODO Dit is de oude code van good_nonce en find_nonce
    # def good_nonce(self, new_hash = None):
    #     if new_hash is None:
    #         new_hash = self.computeHash()
    #     if new_hash.startswith(b'0' * leading_zeros):
    #         return True
    #     else:
    #         return False

    # def find_nonce(self):
    #     while True:
    #         hashTry = self.computeHash()
    #         # print(self.nonce, hashTry)
    #         if self.good_nonce(hashTry):
    #             # print(f"Nonce found: {self.nonce}")
    #             self.blockHash = hashTry
    #             return hashTry
            
    #         self.nonce += 1
    # TODO
    # def find_nonce(self):
    #     stopwatch = Stopwatch()
    #     stopwatch.start()
    #     hash = None
    #     nonce = None
    #     while stopwatch.get_elapsed_time() < 20: 
    #         while True:
    #             hashTry = self.computeHash()
    #             if self.good_nonce(hashTry):
    #                 self.blockHash = hashTry
    #                 hash = hashTry
    #                 nonce = self.nonce
    #                 break
    #             self.nonce += 1
        
    #     stopwatch.stop()
    #     stopwatch.print_elapsed_time()
    #     return hash, nonce
    
    def __repr__(self):
        #TODO Check what we want to represent
        repr_str = super().__repr__()
        repr_str += "Nonce: " + str(self.nonce) + "\n"
        repr_str += "Creation date: " + str(self.creation_date) + "\n"
        repr_str += "Valid counter: " + str(self.valid_counter) + "\n"
        repr_str += "Invalid counter: " + str(self.invalid_counter) + "\n"
        repr_str += "Validated by: " + str(self.validated_by) + "\n"
        repr_str += "Status: " + str(self.status) + "\n"
        repr_str += "Miner of block: " + str(self.miner_of_block) + "\n"
        repr_str += "Total fee for miner: " + str(self.total_fee_for_miner) + "\n"
        return repr_str