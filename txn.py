from typing import List, Dict, Optional
import hashlib
import json

class Transaction:
    
    def __init__(self, timestamp: str, idempotency_key: str, postings: List[Dict]):
        self.postings = postings
        self.timestamp = timestamp
        self.idempotency_key = idempotency_key
        self.hash = None
        self.validate_postings()
        self.compute_hash()
    

    def validate_postings(self):
        total_amount = sum(p["amount"] for p in self.postings)
        if total_amount != 0:
            raise ValueError("Postings must balance")

    def to_bytes(self):
        txn_data = {
            "idempotency_key": self.idempotency_key,
            "postings": self.postings,
            "timestamp": self.timestamp,
        }

        txn_data_str = json.dumps(txn_data, sort_keys=True, separators=(",", ":"))
        return txn_data_str.encode('utf-8')
      
    
    def compute_hash(self):
        bytes_data = self.to_bytes()
        self.hash = hashlib.sha256(bytes_data).hexdigest()


        