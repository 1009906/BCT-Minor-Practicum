from BlockChain import CBlock
from Signature import generate_keys, sign, verify
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import random

REWARD_VALUE = 25.0
leading_zeros = 1
next_char_limit = 20

class TxBlock (CBlock):

    def __init__(self, previousBlock):
        super(TxBlock, self).__init__([], previousBlock)
        # TODO toevoegen van een counter voor het aantal keer validaten door ingelogde gebruikers (valid counter)
        # TODO toevoegen van een counter voor het aantal keer validaten door ingelogde gebruikers (invalid counter)
        # TODO AssignedToPreviousBlock toevoegen aan de TxBlock class boolean
        # TODO MinerOfBlock toevoegen aan de TxBlock class string, die kan je pakken uit context.user_name

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

    def good_nonce(self):
        block_hash = self.computeHash()
        if block_hash.startswith(b'0' * leading_zeros):
            return True
        else:
            return False

    def find_nonce(self):
        while True:
            hashTry = self.computeHash()
            print(self.nonce, hashTry)
            if self.good_nonce():
                print(self.nonce)
                self.blockHash = hashTry
                return hashTry
            
            self.nonce += 1