#!/usr/bin/env python3

# Leco Hendriks 0993233
# Bram Vermeer 1009906
"""Asymmetric Cryptography -> Digital Signature: Homework 

The goal of this homework is to learn how to store and load asymmetric keys of different users on a disk.
In addition, to sign and verify messages using those keys. Furthermore, it is required to encrypt keys before saving using a password. 
In this implementation the passed message as an argument is a string. Proper encoding and decoding is need before usage.
When signing a message the RSA sign-function requires a specific hash like SHA256, and padding such as PSS.
RSA verify function calculates the message hash. Decrypt the signature then compares both values to verify. 
Be aware that verification must use the same algorithm values as signing to correctly verify the signature.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code 
    * run the test of this tutorial located in same folder.

To test run 'Signature_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
    * visit this url for more information on this topic:
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
"""

from cryptography.exceptions import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import pickle

def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

# TODO 1: Sign a passed message using a given private key
# Make sure the message is encoded correctly before signing
# Signing and verifying algorithms must be the same
def sign(message, private_key):
    mssg = message.encode('utf-8')
    try:
        signature = private_key.sign(
            mssg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
    except:
        return None


# TODO 2: Verify a signature for a message using a given public key
# Make sure the message is decoded correctly before verifying
# Signing and verifying algorithms values must be the same
def verify(message, signature, public_key):
    mssg = bytes(message, 'utf-8')
    try:
        public_key.verify(
            signature,
            mssg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
                ),
            hashes.SHA256()
            )
        return True
    except:
        return False

# TODO 3: Store the list of keys into a given file.
# In this implementation passwords are used for additional security
# Make sure of proper PEM encoding before serialization
def save_keys(keys_file_name, keys, pw):
    keys_ser_list = []
    bpw = bytes(pw, 'utf-8')

    prv_ser = keys[0].private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(bpw)
                )
    pbc_ser = keys[1].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
    
    keys_ser_list.append((prv_ser, pbc_ser))
    
    savefile = open(keys_file_name, "wb")
    pickle.dump(keys_ser_list, savefile)
    savefile.close()

# TODO 4: Load asymmetric keys from a given file and return those keys as a tuple
# In this implementation passwords are used for additional security
# Make sure of proper PEM decoding when deserializing
def load_keys(keys_file_name, pw):
    loadfile = open(keys_file_name, "rb")
    keys_list_ser = pickle.load(loadfile)
    loadfile.close()
    bpw = bytes(pw, 'utf-8')

    for item in keys_list_ser:
        private_key_ser, public_key_ser = item
        private_key = serialization.load_pem_private_key(private_key_ser,password=bpw)
        public_key = serialization.load_pem_public_key(public_key_ser)

    return private_key, public_key
