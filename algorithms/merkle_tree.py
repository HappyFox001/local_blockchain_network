from core.methods.methods import sha256, hash


class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.root = self.build_tree(transactions)

    def build_tree(self, transactions):
        hashes = [self.hash_leaf(tx) for tx in transactions]
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            new_level = []
            for i in range(0, len(hashes), 2):
                new_level.append(self.hash_pair(hashes[i], hashes[i + 1]))
            hashes = new_level
        return hashes[0] if hashes else None

    def hash_leaf(self, data):
        return hash(data)

    def hash_pair(self, left, right):
        return sha256(left + right)

    def get_root(self):
        return self.root
