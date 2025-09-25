import time
from typing import Optional
from classes import User, TransactionTuple, BlockTuple
from storage import Users, Transactions, Blocks

def create_user(username: str, balance: float = 0.0) -> User:
    user = User(username, balance)
    Users.append(user)
    return user

def add_transaction(sender: User, receiver: User, amount: float, energy_rate: float = 0.0) -> Optional[TransactionTuple]:
    if sender.balance < amount:
        return None
    
    sender.balance -= amount
    receiver.balance += amount
    
    txn: TransactionTuple = (sender.address, receiver.address, amount, time.time(), energy_rate)
    Transactions.append(txn)
    return txn
