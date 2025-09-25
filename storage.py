"""
Blockchain storage module - contains all global storage lists.
"""
from typing import List
from classes import User, TransactionTuple, BlockTuple

Users: List[User] = []
Transactions: List[TransactionTuple] = []
Blocks: List[BlockTuple] = []

def get_user_by_address(address: str) -> User | None:
    for user in Users:
        if user.address == address:
            return user
    return None

def clear_all_data():
    Users.clear()
    Transactions.clear()
    Blocks.clear()

def get_stats():
    return {
        'total_users': len(Users),
        'total_transactions': len(Transactions),
        'total_blocks': len(Blocks),
        'total_balance': sum(user.balance for user in Users)
    }