import argparse
import time
from ledger import Ledger
from txn import Transaction
from merkle import verify_merkle_proof


LEDGER = Ledger()

def now_ms():
    return str(int(time.time() * 1000))

def cmd_add(args):
    postings = [
        {"account": f"cash:{args.from_acct}", "amount": -args.amount},
        {"account": f"cash:{args.to_acct}", "amount": args.amount},
    ]

    txn = Transaction(
        timestamp=now_ms(),
        idempotency_key=args.idempo,
        postings=postings
    )

    txid, replayed = LEDGER.append(txn)
    root = LEDGER.get_merkle_root()

    print("idempotent replay:" if replayed else "new transaction:")
    print("txid:", txid)
    print("txn_hash:", txn.hash)
    print("merkle_root:", root.hex() if root else "None")

def cmd_root(args):
    root = LEDGER.get_merkle_root()
    print(root.hex() if root else "None")

def cmd_prove(args):
    leaf, proof, root = LEDGER.prove(args.txid)
    print("txid:", args.txid)
    print("root:", root.hex() if root else "None")
    print("leaf_hash:", __import__("hashlib").sha256(leaf).hexdigest())
    print("proof:")

    for direction, sib in proof:
        print(f"  {direction} {sib.hex()}")

def cmd_verify(args):
    leaf, proof, root = LEDGER.prove(args.txid)
    ok = verify_merkle_proof(leaf, proof, root)

    print("We GUCCI (PASS)" if ok else "YOU MESSED UP")

def cmd_reset(args):
    import os
    if os.path.exists(LEDGER.wal_path):
        os.remove(LEDGER.wal_path)
        print(f"Ledger reset: deleted {LEDGER.wal_path}")
    else:
        print(f"No WAL file found {LEDGER.wal_path}")

def cmd_status(args):
    print(f"WAL file: {LEDGER.wal_path}")
    print(f"Total transactions: {len(LEDGER.txns)}")
    print(f"Merkle root: {LEDGER.get_merkle_root().hex() if LEDGER.get_merkle_root() else 'None'}")
        
        
def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(required=True)

    a = sub.add_parser("add")
    a.add_argument("--idempo", required=True)
    a.add_argument("--from", dest="from_acct", required=True)
    a.add_argument("--to", dest="to_acct", required=True)
    a.add_argument("--amount", type=int, required=True)
    a.set_defaults(func=cmd_add)

    r = sub.add_parser("root")
    r.set_defaults(func=cmd_root)

    pr = sub.add_parser("prove")
    pr.add_argument("--txid", type=int, required=True)
    pr.set_defaults(func=cmd_prove)

    v = sub.add_parser("verify")
    v.add_argument("--txid", type=int, required=True)
    v.set_defaults(func=cmd_verify)

    reset = sub.add_parser("reset", help="Clear the WAL and reset ledger")
    reset.set_defaults(func=cmd_reset)

    status = sub.add_parser("status", help="Show ledger status")
    status.set_defaults(func=cmd_status)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()









