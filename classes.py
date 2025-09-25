import os
from hashlib import sha256
import time
from typing import Tuple, List

def generate_keys(username: str) -> Tuple[str, str, str]:
    seed = os.urandom(32)
    private_key = sha256(seed).hexdigest()
    timestamp = str(time.time())
    public_input = (private_key + username + timestamp).encode()
    public_key = sha256(public_input).hexdigest()
    address = sha256(public_key.encode()).hexdigest()[:40]
    return private_key, public_key, address

class User:
    def __init__(self, username: str, balance: float = 0.0):
        self.username = username
        self.balance = balance
        self.private_key, self.public_key, self.address = generate_keys(username)
        self.signature = ""
        
TransactionTuple = Tuple[str, str, float, float, float]
BlockTuple = Tuple[int, float, str, List[TransactionTuple], str, str]
