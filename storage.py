"""
Blockchain storage module - contains all global storage lists.
"""
from classes import User, TransactionTuple, BlockTuple

Users: list[User] = []
Transactions: list[TransactionTuple] = []
Blocks: list[BlockTuple] = []

def get_user_by_address(address: str) -> User | None:
    for user in Users:
        if user.address == address:
            return user
    return None

def clear_all_data():
    Users.clear()
    Transactions.clear()
    Blocks.clear()

def get_stats() -> dict[str, int | float]:
    return {
        'total_users': len(Users),
        'total_transactions': len(Transactions),
        'total_blocks': len(Blocks),
        'total_balance': sum(user.balance for user in Users)
    }

def load_bulk_users(file_path: str = "bulk_users.txt"):
    Users.clear()
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                parts = line.split(",")
                if len(parts) == 2:
                    username = parts[0].strip()
                    try:
                        balance = float(parts[1].strip())
                    except ValueError:
                        balance = 0.0
                    Users.append(User(username, balance))
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def load_bulk_transactions(file_path: str = "bulk_transactions.txt"):
    Transactions.clear()
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                parts = line.split(",")
                if len(parts) == 4:
                    sender = parts[0].strip()
                    receiver = parts[1].strip()
                    try:
                        amount = float(parts[2].strip())
                        energy_rate = float(parts[3].strip())
                    except ValueError:
                        amount = 0.0
                        energy_rate = 0.0
                    # Find sender/receiver addresses
                    sender_obj = next((u for u in Users if u.username == sender), None)
                    receiver_obj = next((u for u in Users if u.username == receiver), None)
                    if sender_obj and receiver_obj:
                        txn = (sender_obj.address, receiver_obj.address, amount, 0.0, energy_rate)
                        Transactions.append(txn)
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def distribute_transactions_across_shards(num_shards: int):
    shard_txns = [[] for _ in range(num_shards)]
    for i, txn in enumerate(Transactions):
        shard_txns[i % num_shards].append(txn)
    return shard_txns
