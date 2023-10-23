from src.system.context import Context
from src.system.blockchain.Transaction import Tx
import pickle

def transfer_coins(reciever, amountCoins, transactionFee):
    newTx = Tx()
    newTx.add_input(Context.user_name, amountCoins)
    newTx.add_output(reciever, amountCoins)
    newTx.sign(Context.private_key)

    if newTx.is_valid():
        #Transaction is valid
        savefile = open("src\pool\pooltx.dat", "wb")
        pickle.dump(newTx, savefile)
        savefile.close()
        return True
    else:
        #Transaction is not valid
        return False