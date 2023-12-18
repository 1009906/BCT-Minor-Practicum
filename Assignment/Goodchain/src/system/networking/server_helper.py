import importlib
# import pickle
import sys

#C:\Users\freer\AppData\Local\Programs\Python\Python310\Lib\pickle.py

spec = importlib.util.spec_from_file_location("pickle", "C:/Users/freer/AppData/Local/Programs/Python/Python310/Lib/pickle.py")
foo = importlib.util.module_from_spec(spec)
sys.modules["pickle"] = foo
spec.loader.exec_module(foo)
pickle = foo

bla = ''

def load_transaction_from_network(transaction):
    return pickle.loads(transaction)