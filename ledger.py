from typing import List, Optional
from merkle import build_merkle_tree, merkle_proof
from txn import Transaction
import json
import os

class Ledger:

    def __init__(self, wal_path: str = "transactions.log"):
        self.idempotent = {}
        self.txns: List[Transaction] = []
        self.wal_path = wal_path

        self.load_from_wal()

    # {{ wal for persistentance / durability

    def load_from_wal(self):
        if not os.path.exists(self.wal_path):
            return
        
        with open(self.wal_path, 'r') as f:
            for line in f:
                if line.strip():
                    txn_data = json.loads(line.strip())

                    txn = Transaction(
                        timestamp = txn_data['timestamp'],
                        idempotency_key = txn_data['idempotency_key'],
                        postings = txn_data['postings']
                    )

                    self.append_to_mem(txn)

    def append_to_wal(self, transaction: Transaction):
        txn_data = {
            'timestamp': transaction.timestamp,
            'idempotency_key': transaction.idempotency_key,
            'postings': transaction.postings
        }

        with open(self.wal_path, 'a') as f:
            f.write(json.dumps(txn_data) + '\n')
            f.flush()
            os.fsync(f.fileno())

    # }}


    # {{ append_to_memory function does not append to wal just self.txns and self.idempotent

    def append_to_mem(self, transaction: Transaction):

        self.txns.append(transaction)
        txid = len(self.txns) - 1
        self.idempotent[transaction.idempotency_key] = txid
        return txid
    
    def append(self, transaction: Transaction):

        if transaction.idempotency_key in self.idempotent:
            return self.idempotent[transaction.idempotency_key], True
        
        self.append_to_wal(transaction)

        txid = self.append_to_mem(transaction)
        return txid, False

    # }}



    def _leaves(self):
        # convert object to bytes for merkle 
        return [txn.to_bytes() for txn in self.txns]
    
    def get_merkle_root(self):
        tree = build_merkle_tree(self._leaves())
        return tree.value if tree else None

    def prove(self, txid):
        leaves = self._leaves()
        proof = merkle_proof(leaves, txid)
        root = self.get_merkle_root()
        leaf = leaves[txid]
        return leaf, proof, root


