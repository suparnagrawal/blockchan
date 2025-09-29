from storage import Users, Transactions, load_bulk_users, load_bulk_transactions, distribute_transactions_across_shards, get_stats, Blocks
from functions import select_committee
import random
import time

# Load users and transactions from bulk files
load_bulk_users()
load_bulk_transactions()

print("User-Stake List:")
Stake = []
for user in Users:
    # 30% chance to stake, otherwise stake is zero
    if random.random() < 0.3:
        stake = random.randint(1, int(user.balance))
    else:
        stake = 0
    Stake.append(stake)
    print(f"{user.username}: {stake}")

# Distribute transactions across shards
block_size = 25  # Increased block size for fewer blocks
num_blocks = (len(Transactions) + block_size - 1) // block_size if Transactions else 2
shard_txns = distribute_transactions_across_shards(num_blocks)
print(f"\nTotal blocks to verify: {num_blocks}")

# Simulate user willingness to be validator
willingness = {}
for user in Users:
    # 60% chance user wants to be a validator
    willingness[user.username] = random.random() < 0.6

print("\nUsers willing to be validators:")
for user in Users:
    if willingness[user.username]:
        print(user.username)

# Only allow willing users with positive stake in committee selection
available_users = [u for u in Users if willingness[u.username] and Stake[Users.index(u)] > 0]
available_stakes = [Stake[Users.index(u)] for u in available_users]
committee_size = min(4, len(available_users) // num_blocks) if num_blocks else len(available_users)

for block_num in range(num_blocks):
    print(f"\nBlock {block_num+1}:")
    print("Transactions:")
    for txn in shard_txns[block_num]:
        print(txn)
    # Print balances before block validation
    print("Balances before block:")
    for user in Users:
        print(f"{user.username}: {user.balance}")
    # Simulate block validation: apply transactions
    for txn in shard_txns[block_num]:
        sender = next((u for u in Users if u.address == txn[0]), None)
        receiver = next((u for u in Users if u.address == txn[1]), None)
        amount = txn[2]
        if sender and receiver and sender.balance >= amount:
            sender.balance -= amount
            receiver.balance += amount
    # Print balances after block validation
    print("Balances after block:")
    for user in Users:
        print(f"{user.username}: {user.balance}")
    # Select committee from available users
    committee = select_committee(available_users, available_stakes, committee_size)
    print("Committee members:", [u.username for u in committee])
    # Remove assigned users from available pool
    for user in committee:
        idx = available_users.index(user)
        available_users.pop(idx)
        available_stakes.pop(idx)
    # Run BFT to elect validator for this block
    if committee:
        while len(committee) > 1:
            if len(committee) == 2:
                committee = [committee[random.randint(0, 1)]]
            else:
                remove_count = max(1, len(committee) // 3)
                committee = committee[remove_count:]
        validator = committee[0]
        print(f"Validator for Block {block_num+1}: {validator.username}")
    else:
        validator = None
        print(f"No validator selected for Block {block_num+1} (no eligible committee members)")
    # Add block to Blocks storage
    block = (
        block_num+1,
        time.time(),
        validator.username if validator else "None",
        shard_txns[block_num],
        "prev_hash_placeholder",
        "hash_placeholder"
    )
    Blocks.append(block)
    print(f"Block {block_num+1} added: {block}")

# Display results
print("Users:", Users)
print("Transactions:", Transactions)
print("Blocks:", len(Blocks), "block(s) created")
print("Stats:", get_stats())

# Print clean summary at the end
print("\n--- Blockchain Summary ---")
print(f"Total blocks: {len(Blocks)}")
print("Block Validators:")
for i, block in enumerate(Blocks):
    print(f"Block {block[0]}: Validator = {block[2]}")

# Track initial and final balances for change summary
print("\nUser Balance Changes:")
for user in Users:
    # Initial balance can be reconstructed from bulk_users.txt
    # For demo, print only final balance
    print(f"{user.username}: Final Balance = {user.balance}")

print("\nTransaction Summary:")
for block in Blocks:
    block_num = block[0]
    for txn in block[3]:
        sender_addr, receiver_addr, amount, _, _ = txn
        sender = next((u.username for u in Users if u.address == sender_addr), sender_addr)
        receiver = next((u.username for u in Users if u.address == receiver_addr), receiver_addr)
        print(f"Block {block_num}: {sender} -> {receiver}, Amount: {amount}")

print("\n--- Block Transactions Summary ---")
for block in Blocks:
    print(f"Block {block[0]}: transactions list:")
    txns = block[3]
    if txns:
        for txn in txns:
            sender_addr, receiver_addr, amount, _, _ = txn
            sender = next((u.username for u in Users if u.address == sender_addr), sender_addr)
            receiver = next((u.username for u in Users if u.address == receiver_addr), receiver_addr)
            print(f"  ({sender}, {receiver}, {amount})")
    else:
        print("  No transactions in this block.")