import sqlite3
from core.methods.methods import hash
from node.node import Node


class SeedNode(Node):
    def __init__(self, name, manager):
        super().__init__(name, manager)
        # 初始化数据库连接
        # self.db_connection = sqlite3.connect("../db/blockchain.db")
        self.db_path = "../db/blockchain.db"
        self.create_block_table()

    def create_block_table(self):
        # 创建区块表，存储区块信息
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DROP TABLE IF EXISTS blocks")
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS blocks (
                        height INTEGER,
                        block_hash TEXT UNIQUE,
                        previous_hash TEXT,
                        type TEXT
                    )
                """
            )

    def handle_new_block(self, message):
        """接收新块并处理，标记为‘确认区块’并存入数据库"""
        super().handle_new_block(message)  # 调用父类方法处理正常区块逻辑

        # 如果区块被成功添加到链中，将其存入数据库并标记为‘确认区块’
        block = message["content"]
        if self.sync.chain.get_block_by_hash(hash(block.header)):
            self.store_or_update_block(block, "确认区块")

    def handle_sync_response(self, message):
        """处理同步响应中的区块数据，从第一个不匹配的区块高度开始添加"""

        fork_height = 1
        start_index = 0
        for i, block in enumerate(message["content"]):
            if block.height <= len(self.sync.chain.blocks):
                local_block = self.sync.chain.blocks[block.height - 1]
                if hash(local_block.header) != hash(block.header):
                    fork_height = block.height
                    start_index = i
                    break

        # 回滚到分叉点
        self.rollback_chain(fork_height)
        self.mineing = False

        # 从起点区块开始添加新区块
        for block in message["content"][start_index:]:
            if self.sync.add_block(block):
                # print(f"{self.name}: 添加缺失的区块 {hash(block.header)} 到链中")
                self.update_utxo_set(block)
                self.remove_duplicate_transactions(block.transactions)
                self.store_or_update_block(block, "确认区块")
            else:
                # print(f"{self.name}: 缺失区块 {hash(block.header)} 验证失败，放弃添加")
                break  # 如果一个区块失败，则停止添加后续区块
        self.mineing = True

    def rollback_chain(self, fork_height):
        """回滚链到指定的分叉高度，并将被回滚的区块标记为‘废弃区块’"""
        while len(self.sync.chain.blocks) > fork_height - 1:
            last_block = self.sync.chain.blocks.pop()
            # print(f"{self.name}: 回滚区块 {hash(last_block.header)}")

            # 将回滚区块标记为‘废弃区块’
            self.mark_block_as_discarded(last_block)

            # 将区块中的交易恢复到交易池
            for transaction in last_block.transactions:
                self.mempool.append(transaction)

            # 还原 UTXO 集合
            self.revert_utxo_set(last_block)

    def store_or_update_block(self, block, block_type):
        """检查并将区块存入数据库，如果存在则更新类型"""
        block_hash = hash(block.header)
        with sqlite3.connect(self.db_path) as conn:
            # 检查区块是否已经在数据库中
            cursor = conn.execute(
                "SELECT 1 FROM blocks WHERE block_hash = ?", (block_hash,)
            )
            if cursor.fetchone():
                # 如果区块已存在，更新类型为“确认区块”
                conn.execute(
                    """
                    UPDATE blocks
                    SET type = ?
                    WHERE block_hash = ?
                """,
                    (block_type, block_hash),
                )
            else:
                # 如果区块不存在，则插入新的记录
                conn.execute(
                    """
                    INSERT INTO blocks (height, block_hash, previous_hash, type)
                    VALUES (?, ?, ?, ?)
                """,
                    (block.height, block_hash, block.header.previous_hash, block_type),
                )

    def mark_block_as_discarded(self, block):
        """将指定区块在数据库中标记为‘废弃区块’"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE blocks
                SET type = '废弃区块'
                WHERE block_hash = ?
            """,
                (hash(block.header),),
            )
