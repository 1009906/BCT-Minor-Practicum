class CBlock:
    data = None
    previousHash = None
    previousBlock = None

    def __init__(self, data, previousBlock):
        self.data = data
        self.blockHash = None
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()

    def is_valid(self):
        if self.previousBlock == None:
            return True
        tamperCheck = True
        if self.blockHash is not None: #is already mined
            tamperCheck = self.blockHash == self.computeHash()
        return tamperCheck and (self.previousBlock.computeHash() == self.previousHash) and CBlock.is_valid(self.previousBlock)
    
    def __repr__(self):
        repr_str = "Blockhash: " + str(self.blockHash) + "\n"
        repr_str += "Previous hash: " + str(self.previousHash) + "\n"
        repr_str += "Amount of transactions: " + str(len(self.data)) + "\n"
        repr_str += "Data: \n\n"
        for transaction in self.data:
            repr_str += transaction.__repr__() + "\n"
        return repr_str