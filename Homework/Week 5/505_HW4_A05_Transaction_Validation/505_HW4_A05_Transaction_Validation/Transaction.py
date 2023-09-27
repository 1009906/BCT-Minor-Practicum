#!/usr/bin/env python3

# Bram Vermeer 1009906
# Leco Hendriks 0993233

"""
Transaction Class 

The goal of this exercise is to learn how to complete transaction class.
A transaction is composed of a list of Inputs and a list of outputs, and few methods.
add_input() and add_output(), and sign() are already completed in the previous tutorials and exercise.
In this hoemwork, we will add another method is_valid() to the class. With this method, we can
validate a transaction. 

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code 
    * run the test of this tutorial located in same folder.

To test run 'Transactions_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
"""
from Signature import *

class Tx:
    inputs = None
    outputs =None
    data = None
    sigs = None
    reqd = None

    # TODO 1: Complete the method
    # These three methods are already done in the previous tutorials
    # you can copy and paste the previous codes here     
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.data = []
        self.sigs = []
        self.reqd = []      # A placeholder for any other extra required signature (e.g. escrow)

    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr,amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))
    
    # TODO 2: Complete the method
    # We would like to have another method to add extra required signature if needded (e.g. escrow)
    # with this method, we can specify other required signature to the transaction by adding the 
    # public key of the required signature
    # If this signature is needed, later we can check if the transaction is also signed by that person/party.
    def add_reqd(self, addr):
        self.reqd.append(addr) 

    # TODO 3: Complete the method
    # This method is also already done in the previous tutorials.
    # you can copy and paste the previous codes here  
    def sign(self, private):
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        
        sig = sign(data, private)
        self.data.append(data)
        self.sigs.append(sig)

    # TODO 4: Complete the method
    # This method is used to validate a transaction.
    # To validate a transaction, we must check few important things:
    #   1 -  Every entery in inputs need to be signed by the relevant sender, and
    #   2 -  If an extra required signature is needed, the signature need to be verified too, and
    #   3 -  The total amount of outputs must not exceed the total amount of inputs.
    def is_valid(self):
        for (from_addr, amount) in self.inputs:
            valid = False
            for index, sig in enumerate(self.sigs):
                if verify(self.data[index], sig, from_addr):
                    valid = True
                    break
            if not valid:
                return False
        
        for reqd_addr in self.reqd:
            valid = False
            for index, sig in enumerate(self.sigs):
                if verify(self.data[index], sig, reqd_addr):
                    valid = True
                    break
            if not valid:
                return False

        return self.__verifyAmounts()

    def __verifyAmounts(self):
        total_input_amount = 0.0
        for (from_addr, amount) in self.inputs:
            total_input_amount = total_input_amount + float(amount)

        total_output_amount = 0.0
        for (to_addr, amount) in self.outputs:
            total_output_amount = total_output_amount + float(amount)
            
        if total_input_amount < 0.0 or total_output_amount < 0.0:
            return False #TODO Checken of dat deze lijn nodig is.

        if total_output_amount > total_input_amount:
            return False
        
        return True