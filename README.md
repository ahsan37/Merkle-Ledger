# Merkle Ledger

A Merkle tree based idempotent ledger.


## Merkle Tree

Each transaction becomes a leaf in a binary tree where each parent is the hash of its children. The root hash represents the entire ledger state. To prove a transaction exists, you need the leaf and log(n) sibling hashes to recompute the root.

## Persistence & Idempotency

Transactions are persisted to a Write Ahead Log with fsync after each write. On restart, the ledger rebuilds from the WAL. Idempotency keys prevent duplicate transactions when clients retry.

## Installation

```bash
git clone https://github.com/ahsan37/Merkle-Ledger.git
cd Merkle-Ledger


### Commands

```bash
# Add a transaction
python3 main.py add --idempo <KEY> --from <ACCOUNT> --to <ACCOUNT> --amount <AMOUNT>

# Show Merkle root
python3 main.py root

# Generate Merkle proof for a transaction
python3 main.py prove --txid <ID>

# Verify a transaction is in the ledger
python3 main.py verify --txid <ID>

# Show ledger status
python3 main.py status

# Reset the ledger (clear WAL)
python3 main.py reset
```


## Files

- **`txn.py`** - Transaction model with double-entry validation
- **`merkle.py`** - Merkle tree construction, proof generation, and verification
- **`ledger.py`** - Ledger logic with WAL persistence and idempotency
- **`main.py`** - CLI








