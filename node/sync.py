from core.blockchain.block import Block, BlockHeader
from core.blockchain.transaction import CoinbaseTransaction
from core.blockchain.chain import Chain  # 引用 Chain 类
from core.methods.methods import hash
from algorithms.merkle_tree import MerkleTree
import time


class Sync:
    def __init__(self):
        self.chain = Chain()  # 使用 Chain 实例管理区块链

    # def validate_transaction(self, transaction):
    #     return transaction.validate_transaction() and transaction.validate_utxo()

    def create_block(self, transactions):
        previous_hash = (
            hash(self.chain.blocks[-1].header)
            if len(self.chain.blocks) > 0
            else ("0" * 64)
        )
        header = BlockHeader(
            previous_hash=previous_hash,
            merkle_root=MerkleTree(transactions).get_root(),
            timestamp=int(time.time() * 1000),
        )
        return Block(
            header=header,
            height=self.chain.get_current_height() + 1,
            transactions=transactions,
            # coinbase_transaction=self.create_coinbase_transaction("my_address")
        )

    def add_block(self, block):
        return self.chain.add_block(block)

    # def validate_block(block):
    #     return validate_block(block, self.chain.difficulty)
