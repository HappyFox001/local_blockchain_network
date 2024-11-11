class BlockHeader:
    def __init__(self, previous_hash, merkle_root, timestamp=None, nonce=0):
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.nonce = nonce

    # def hash(self):  # 每2016个区块调整一次

    #     header_string = (
    #         str(self.previous_hash)
    #         + str(self.merkle_root)
    #         + str(self.timestamp)
    #         + str(self.nonce)
    #     )
    #     return sha256(header_string)


class Block:
    def __init__(self, header: BlockHeader, height, transactions):
        self.header = header
        self.height = height
        self.transactions = transactions
        # self.coinbase_transaction = coinbase_transaction

    # def calculate_merkle_root(self):
    #     return MerkleTree(self.transactions).get_root()

    # def validate_merkle_root(self):
    #     return self.calculate_merkle_root() == self.header.merkle_root

    # def hash(self):
    #     block_data = (
    #         self.header.hash()
    #         + "".join([tx.hash() for tx in self.transactions])
    #         + self.coinbase_transaction.hash()
    #     )
    #     return sha256(block_data)
