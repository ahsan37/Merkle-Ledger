# Merkle Ledger

A ledger is surprisingly simple once you understand Merkle trees. Each transaction becomes a leaf, and the leaves form a binary tree where each parent is the hash of its children. The root hash is a fingerprint of the entire ledger. If any transaction changes, the root changes. To prove a transaction exists, you only need the transaction itself and log(n) sibling hashes leading to the root.

The design makes two other choices worth noting. First, transactions are appended to a file with fsync after each write. This Write-Ahead Log means crashes are harmless—on restart, read the file and rebuild the tree. Second, transactions have idempotency keys. Networks fail and clients retry, so the same request might arrive twice. The key prevents duplicates.

That's the whole system. About 300 lines of Python using only the standard library—SHA-256 for hashing, double-entry bookkeeping for consistency, and a binary tree for verification. Small enough to understand completely, but with the properties you'd want in a real ledger.

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







