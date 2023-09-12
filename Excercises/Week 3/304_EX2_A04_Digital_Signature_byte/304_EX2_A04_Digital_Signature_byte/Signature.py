#!/usr/bin/env python3
"""Asymmetric Cryptography -> Digital Signature: Exercise 1

The goal of this exercise is to learn how to sign and verify messages using asymmetric keys.
In this implementation the passed message as an argument is a string converted to a byte object.
When signing a message the RSA sign-function requires a specific hash like SHA256, and padding such as PSS. 
Be aware that verification must use the same algorithms to correctly verify the signature.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code 
    * run the test of this exercise located in same folder.

To test run 'Signature_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
    * visit this url for more information on this topic:
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
"""

# TODO 1: Generate first a private key, then a public key. As a result return both values.
# Make sure you generate the keys in the correct order. 
# Use recommended algorithms values where possible
def generate_keys():
    private = 'private'
    public = 'public'
    return private, public

# TODO 2: Sign a passed message using the passed private key
# Signing and verifying algorithms must be the same
def sign(message, private):
    sig = 'signature'
    return sig


# TODO 3: Verify a signature for a message with the passed public key
# Signing and verifying algorithms values must be the same
# Make sure to handle exception properly if verification fails 
def verify(message, sig, public):
    return False

