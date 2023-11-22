from src.system.blockchain.Signature import *

REWARD_VALUE = 25.0
NORMAL = "NORMAL"
REWARD = "REWARD"
SIGNUP = "SIGNUP"
MINERREWARD = "MINERREWARD"
SIGNUP_REWARD = 50.0
MINERREWARD_VALUE = 50.0

class Tx:
    def __init__(self,id ,owner, receiver, type = NORMAL, transaction_fee = 0):
        self.id = id
        self.owner = owner
        self.receiver = receiver
        self.type = type
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []
        self.is_valid_transaction = False
        self.transaction_fee = transaction_fee

    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private):
        message = self.__gather()
        newsig = sign(message, private)
        self.sigs.append(newsig)
               
    def is_valid(self):
        if self.type == SIGNUP or self.type == MINERREWARD:
            return True
        
        if self.type == REWARD:
            if len(self.inputs)!=0 and len(self.outputs)!=1:
                return False
            return True
        
        else:
            total_in = 0
            total_out = 0
            message = self.__gather()
            for addr,amount in self.inputs:
                found = False
                for s in self.sigs:
                    if verify(message, s, addr):
                        found = True
                if not found:
                    # print ("No good sig found for " + str(message))
                    return False
                if amount < 0:
                    return False
                if self.type == NORMAL:
                    total_in = total_in + amount
            for addr in self.reqd:
                found = False
                for s in self.sigs:
                    if verify(message, s, addr):
                        found = True
                if not found:
                    return False
            for addr,amount in self.outputs:
                if amount < 0:
                    return False
                if self.type == NORMAL:
                    total_out = total_out + amount

            if total_out > total_in:
                # print("Outputs exceed inputs")
                return False        
            return True
        
    def set_valid(self):
        self.is_valid_transaction = True
        return
    
    def set_invalid(self):
        self.is_valid_transaction = False
        return

    def __gather(self):
        data=[]
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return data

    def __repr__(self):
        repr_str = "Id: " + str(self.id) + "\n"
        repr_str += "Owner/Sender: " + str(self.owner) + "\n" if self.owner != None else "Owner/Sender: " + "System" + "\n"
        repr_str += "Receiver: " + str(self.receiver) + "\n"
        repr_str += "Type: " + str(self.type) + "\n"
        repr_str += "Is Valid: " + str(self.is_valid_transaction) + "\n"
        repr_str += "Fee: " + str(self.transaction_fee) + "\n"
        
        return repr_str