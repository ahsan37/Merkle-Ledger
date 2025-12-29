import hashlib
from typing import List
    
class Node:
    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value

    
def hash_bytes(data: bytes):
    return hashlib.sha256(data).digest()

def build_merkle_tree(leaves: list[bytes]):

    if not leaves:
        return None

    nodes = [Node(None, None, hash_bytes(leaf)) for leaf in leaves]

    while len(nodes) > 1:
        #if odd number duplicate last
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1]) 

        next_level = []
        for i in range(0, len(nodes), 2):
            left_node, right_node = nodes[i], nodes[i+1]
            parent_hash = hash_bytes(left_node.value + right_node.value)

            parent_node = Node(left=left_node, right=right_node, value=parent_hash)
            next_level.append(parent_node)
        
        nodes = next_level


    return nodes[0]


def merkle_proof(leaves: List[bytes], index: int):

    # build merkle proof from a given index 
    
    if index < 0 or index >= len(leaves):
        raise ValueError("Index out of range")
    
    level = [hash_bytes(leaf) for leaf in leaves]
    idx = index
    proof = []

    while len(level) > 1:
        if len(level) % 2 != 0:
            level.append(level[-1])
        
        #if current is left hash right else left 
        if idx % 2 == 0:
            sib = level[idx + 1] if idx + 1 < len(level) else level[idx]
            proof.append(("R", sib))
        else:
            sib = level[idx - 1] if idx - 1 >= 0 else level[idx]
            proof.append(("L", sib))
        
        next_level = []

        for i in range(0, len(level), 2):
            left, right = level[i], level[i+1]
            next_level.append(hash_bytes(left + right))

        level = next_level
        idx //= 2
    
    return proof


#given leaf, proof, root verify if leaf is in the tree
def verify_merkle_proof(leaf, proof, root):

    acc = hash_bytes(leaf)
    for direction, sibling_hash in proof:
        if direction == "L":    
            acc = hash_bytes(sibling_hash + acc)
        else:
            acc = hash_bytes(acc + sibling_hash)
    
    return acc == root






        
