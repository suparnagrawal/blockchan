import time
import random
from storage import Users, Transactions, Blocks
from classes import User, TransactionTuple, BlockTuple

def create_user(username: str, balance: float = 0.0) -> User:
    user = User(username, balance)
    Users.append(user)
    return user

def add_transaction(sender: User, receiver: User, amount: float, energy_rate: float = 0.0):
    if sender.balance < amount:
        return None
    
    sender.balance -= amount
    receiver.balance += amount
    
    txn: TransactionTuple = (sender.address, receiver.address, amount, time.time(), energy_rate)
    Transactions.append(txn)
    return txn

def get_stakes(users):
    stakes = []
    for usr in users:
        t = int(input(f"Enter stake amount for {usr.username}: "))
        stake = min(t, usr.balance)
        stakes.append(stake)
    return stakes

def pdf(stakes: list[float], users: list[User]):
    total_stake = sum(stakes)
    if total_stake == 0:
        return None
    pick = random.uniform(0, total_stake)
    current = 0
    for i, stake in enumerate(stakes):
        current += stake
        if current > pick:
            return users[i]
    return None

# Select committee from users and stakes
def select_committee(users, stakes, committee_size):
    selected = set()
    stakes_copy = stakes[:]
    while len(selected) < min(committee_size, len(users)):
        user = pdf(stakes_copy, users)
        if user is not None:
            selected.add(user)
            idx = users.index(user)
            stakes_copy[idx] = 0  # Prevent reselection
    return list(selected)
