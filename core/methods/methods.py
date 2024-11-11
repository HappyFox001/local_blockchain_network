import time

import hashlib
import json

from core.blockchain.block import BlockHeader, Block
from core.blockchain.transaction import Transaction, CoinbaseTransaction
from typing import List


def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


def hash(data):
    if isinstance(data, BlockHeader):
        header_string = (
            str(data.previous_hash)
            + str(data.merkle_root)
            + str(data.timestamp)
            + str(data.nonce)
        )
        return sha256(header_string)
    elif isinstance(data, (Transaction, CoinbaseTransaction)):
        tx_data = json.dumps(
            {
                "sender": data.sender_address,
                "recipient": data.recipient_address,
                "amount": data.amount,
            },
            sort_keys=True,
        )
        return sha256(tx_data)

    else:
        print(f"不支持的数据类型: {type(data)}")
        time.sleep(3)
        return sha256(data)


def calculate_merkle_root(transactions: List[Transaction]):
    return MerkleTree(transactions).get_root()


def validate_merkle_root(block: Block):
    return calculate_merkle_root(block.transactions) == block.header.merkle_root
