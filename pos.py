from storage import Users, Transactions, Blocks, load_bulk_users
from functions import get_stakes, select_committee
import random
from classes import User, TransactionTuple, BlockTuple

# Load users from bulk file
load_bulk_users()

if __name__ == "__main__":
    print("User-Stake List:")
    Stake = get_stakes(Users)
    for user, stake in zip(Users, Stake):
        print(f"{user.username}: {stake}")

    block_size = 3
    num_blocks = (len(Transactions) + block_size - 1) // block_size if Transactions else 2
    print(f"\nTotal blocks to verify: {num_blocks}")

    # Track available users for committee assignment
    available_users = Users[:]
    available_stakes = Stake[:]
    committee_size = min(4, len(Users) // num_blocks) if num_blocks else len(Users)

    for block_num in range(num_blocks):
        print(f"\nBlock {block_num+1}:")
        # Select committee from available users
        committee = select_committee(available_users, available_stakes, committee_size)
        print("Committee members:", [u.username for u in committee])
        # Remove assigned users from available pool
        for user in committee:
            idx = available_users.index(user)
            available_users.pop(idx)
            available_stakes.pop(idx)
        # Run BFT to elect validator for this block
        while len(committee) > 1:
            if len(committee) == 2:
                committee = [committee[random.randint(0, 1)]]
            else:
                remove_count = max(1, len(committee) // 3)
                committee = committee[remove_count:]
        validator = committee[0]
        print(f"Validator for Block {block_num+1}: {validator.username}")