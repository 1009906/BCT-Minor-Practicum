import hashlib
import os

from src.system.context import Context

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def save_hashes_to_file():
    with open(Context.hash_file_path, "w") as f:
        f.write(f"database_hash:{calculate_file_hash(Context.database_path)}\n")
        f.write(f"ledger_hash:{calculate_file_hash(Context.ledger_path)}\n")
        f.write(f"pool_hash:{calculate_file_hash(Context.pool_path)}\n")

def load_hashes_from_file():
    if not os.path.exists(Context.hash_file_path):
        return {}, {}, {}
    with open(Context.hash_file_path, "r") as f:
        lines = f.readlines()
    file_hashes = {}
    for line in lines:
        key, value = line.strip().split(":")
        file_hashes[key] = value
    return file_hashes.get("database_hash", ""), file_hashes.get("ledger_hash", ""), file_hashes.get("pool_hash", "")