import threading
import time
from node.network import Network
from node.sync import Sync
from wallet.wallet import Wallet
from core.blockchain.transaction import UTXO
from core.methods.methods import hash, sha256
from core.blockchain.block import Block
from core.blockchain.transaction import CoinbaseTransaction
from algorithms.encryption import verify_signature
import random


class Node:
    def __init__(self, name, manager):
        self.name = name
        # self.host = host
        # self.port = port
        # self.network = Network(name, host, port, peers)
        # self.target_list = []
        self.manager = manager
        self.sync = Sync()
        self.mempool = []
        self.utxo_set = {}
        self.wallet = Wallet()
        self.miner_address = self.wallet.address
        self.id_pool = []
        self.mineing = False
        self.candidate_block: Block

    def start(self):
        # listener_thread = threading.Thread(
        #     target=self.network.start_listening, args=(self.handle_message,)
        # )
        # listener_thread.start()
        print(f"{self.name}:节点启动成功")
        # self.broadcast_node_info()

    def stop_mining(self):
        """停止当前的挖矿线程"""
        self.mining = False

    def start_mining(self):
        """启动挖矿线程，不断尝试从交易池中挖矿生成区块"""
        self.mineing = True
        mining_thread = threading.Thread(target=self.mine_block)
        mining_thread.start()

    def broadcast_node_info(self):
        """广播节点信息以便其他节点可以将此节点加入到它们的peer列表中"""
        id = self.generate_message_id("node_broadcast")
        message = {
            "type": "node_broadcast",
            "id": id,
            "content": (self.host, self.port),
            "name": self.name,
            # "host": self.host,
            # "port": self.port,
        }
        self.broadcast_gossip(message)

    def broadcast_gossip(self, message):
        for _, node in self.manager.node_list.items():
            if node.name == self.name:
                continue
            time.sleep(0.1)
            node.handle_message(message)

    def generate_message_id(self, message_type):
        """生成唯一消息ID，基于时间戳和节点名称"""
        timestamp = int(time.time() * 1000)  # 毫秒级时间戳
        unique_string = f"{self.name}-{message_type}-{timestamp}"
        return sha256(unique_string)

    def add_to_id_pool(self, message_id):
        """添加消息ID到池中，保持池子大小不超过10"""
        if len(self.id_pool) >= 20:
            self.id_pool.pop(0)  # 移除最旧的ID
        self.id_pool.append(message_id)

    def add_utxo(self, utxo):
        """向 UTXO 集合中添加新 UTXO"""
        utxo_key = (utxo.tx_id, utxo.index)
        self.utxo_set[utxo_key] = utxo

    def handle_message(self, message):
        """控制消息处理"""
        message_id = message.get("id")
        if message_id in self.id_pool:
            # print(f"{self.name}: 消息已处理，跳过")
            return
        self.add_to_id_pool(message_id)
        if message["type"] == "transaction":
            # print(f"{self.name}: <交易同步>")
            self.handle_transaction(message)

        elif message["type"] == "new_block":
            # print(f"{self.name}: <新块同步>")
            self.handle_new_block(message)

        elif message["type"] == "sync_request":
            # print(f"{self.name}: <链同步请求>")
            self.handle_sync_request(message)

        elif message["type"] == "sync_response":
            # print(f"{self.name}: <链同步处理>")
            self.handle_sync_response(message)

        # elif message["type"] == "node_broadcast":
        #     print(f"{self.name}: <接收到节点广播信息>")
        #     self.network.add_peer(message["content"])

    def handle_transaction(self, message):
        if self.validate_transaction(message["content"]):
            self.mempool.append(message["content"])
            # print(f"{self.name}: 接受交易 {hash(message['content'])}，并加入交易池")
            self.broadcast_gossip(message)

    def validate_transaction(self, transaction):
        """验证交易的有效性，并处理交易"""
        selected_utxos, input_amount = self.select_utxos(
            transaction.sender_address, transaction.amount
        )

        if input_amount < transaction.amount:
            print("无效交易：余额不足")
            return False

        # 验证签名
        if not verify_signature(
            transaction.public_key,
            hash(transaction).encode(),
            transaction.signature,
        ):
            print("无效交易：签名验证失败")
            return False

        return True

    def get_balance_for_address(self, address):
        """通过给定的地址计算该地址的总余额"""
        balance = sum(
            utxo.amount for utxo in self.utxo_set.values() if utxo.recipient == address
        )
        return balance

    def select_utxos(self, sender_address, amount):
        """选择足够的 UTXO 满足交易金额"""
        selected_utxos = []
        total = 0
        for utxo_key, utxo in self.utxo_set.items():
            if utxo.recipient == sender_address:
                selected_utxos.append(utxo)
                total += utxo.amount
                if total >= amount:
                    break
        if total < amount:
            raise ValueError("余额不足")
        return selected_utxos, total

    def create_candidate_block(self):
        """创建候选区块，并为每个交易设置 input_utxo 和 output_utxo"""

        # 获取 coinbase 交易（矿工奖励）
        coinbase_tx = CoinbaseTransaction(
            recipient_address=self.miner_address, reward_amount=50
        )

        # 从交易池获取最多10笔交易，并创建候选区块
        current_transactions = [coinbase_tx] + self.mempool[:10]

        # 设置每个交易的 input_utxo 和 output_utxo
        for transaction in current_transactions:
            # 如果是 coinbase 交易，则不需要 input_utxo
            if transaction.sender_address == "coinbase":
                transaction.input_utxo = []
                transaction.output_utxo = [
                    UTXO(
                        tx_id=hash(transaction),
                        index=0,
                        amount=transaction.amount,
                        recipient=transaction.recipient_address,
                    )
                ]
                continue

            # 查找并设置交易的 input_utxo 和 output_utxo
            selected_utxos, input_amount = self.select_utxos(
                transaction.sender_address, transaction.amount
            )
            transaction.input_utxo = selected_utxos
            output_utxo = UTXO(
                tx_id=hash(transaction),
                index=1,
                amount=transaction.amount,
                recipient=transaction.recipient_address,
            )
            transaction.output_utxo = [output_utxo]

            # 如果有找零，生成找零 UTXO 并添加到 output_utxo
            change = input_amount - transaction.amount
            if change > 0:
                change_utxo = UTXO(
                    tx_id=hash(transaction),
                    index=0,
                    amount=change,
                    recipient=transaction.sender_address,
                )
                transaction.output_utxo.append(change_utxo)

        # 创建候选区块
        self.candidate_block = self.sync.create_block(current_transactions)
        self.candidate_block.header.nonce = random.randint(0, 1000000000)

    def mine_block(self):
        self.create_candidate_block()
        while self.mineing:
            # 计算当前 nonce 的哈希值
            block_hash = hash(self.candidate_block.header)

            # 检查哈希值是否符合难度要求
            if (
                block_hash[: self.sync.chain.difficulty]
                == "0" * self.sync.chain.difficulty
            ):
                # 找到符合要求的哈希，添加区块并广播
                if self.sync.add_block(self.candidate_block):
                    # print(f"{self.name}: 挖出新块，哈希值: {block_hash}")

                    # 广播新区块并更新 UTXO 集合
                    block_id = self.generate_message_id("new_block")
                    message = {
                        "type": "new_block",
                        "id": block_id,
                        "content": self.candidate_block,
                        "name": self.name,
                    }
                    self.broadcast_gossip(message)
                    self.id_pool.append(block_id)

                    self.update_utxo_set(self.candidate_block)

                    self.remove_duplicate_transactions(
                        self.candidate_block.transactions
                    )

                    self.create_candidate_block()
            else:
                # 未找到合适的哈希值，增加 nonce
                self.candidate_block.header.nonce += 1

    def handle_new_block(self, message):
        current_height = self.sync.chain.get_current_height()
        if message["content"].height > current_height:
            if message["content"].height == current_height + 1:
                if self.sync.add_block(message["content"]):
                    # print(
                    #     f"{self.name}: 接收到新块{hash(message['content'].header)} 并添加到区块链"
                    # )
                    self.update_utxo_set(message["content"])
                    self.remove_duplicate_transactions(message["content"].transactions)
                    self.broadcast_gossip(message)
                    self.create_candidate_block()
                else:
                    # print(
                    #     f"{self.name}: 区块 {hash(message['content'].header)} 验证失败，放弃添加"
                    # )
                    self.request_sync(
                        message["name"],
                        max(current_height - 10, 1),
                    )
            elif message["content"].height > current_height + 1:
                # print(
                #     f"{self.name}: 检测到更长链的区块，向 {message['name']} 发送请求缺失区块"
                # )
                self.request_sync(
                    message["name"],
                    current_height - 10 if current_height > 10 else 1,
                )
        else:
            pass

    def request_sync(self, name, start_height):
        """向指定节点发送同步请求以获取缺失区块"""
        id = self.generate_message_id("sync_request")
        message = {
            "type": "sync_request",
            "id": id,
            "content": start_height,
            "name": self.name,
        }
        self.manager.node_list[name].handle_message(message)

    def handle_sync_request(self, message):
        """处理其他节点的同步请求，返回最近的区块"""
        if len(self.sync.chain.blocks) <= message["content"]:
            # print(
            #     f"{self.name}: 节点 {requester_address}:{requester_port} 请求的区块高度 {start_height} 不存在"
            # )
            return
        else:
            blocks_to_send = self.sync.chain.blocks
            id = self.generate_message_id("sync_response")
            name = message["name"]
            message = {
                "type": "sync_response",
                "id": id,
                "content": blocks_to_send,
                "name": self.name,
            }
            self.manager.node_list[name].handle_message(message)

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
            else:
                # print(f"{self.name}: 缺失区块 {hash(block.header)} 验证失败，放弃添加")
                break  # 如果一个区块失败，则停止添加后续区块
        self.mineing = True

    def rollback_chain(self, fork_height):
        """回滚链到指定的分叉高度，恢复 UTXO 并重新加入交易池"""
        while len(self.sync.chain.blocks) > fork_height - 1:
            last_block = self.sync.chain.blocks.pop()
            # print(f"{self.name}: 回滚区块 {hash(last_block.header)}")

            # 将区块中的交易恢复到交易池
            for transaction in last_block.transactions:
                self.mempool.append(transaction)

            # 还原 UTXO 集合
            self.revert_utxo_set(last_block)

    def revert_utxo_set(self, block):
        """根据区块中的每个交易撤销 UTXO 集合中的更改"""

        # 遍历区块中的每个交易
        for transaction in block.transactions:

            # 撤销 output_utxo
            for utxo in transaction.output_utxo:
                utxo_key = (utxo.tx_id, utxo.index)
                if utxo_key in self.utxo_set:
                    del self.utxo_set[utxo_key]

            # 恢复 input_utxo
            for utxo in transaction.input_utxo:
                utxo_key = (utxo.tx_id, utxo.index)
                self.utxo_set[utxo_key] = utxo

    def update_utxo_set(self, block):
        """根据新区块更新 UTXO 集合"""
        for transaction in block.transactions:
            # 移除已使用的 input_utxo
            for input_utxo in transaction.input_utxo:
                utxo_key = (input_utxo.tx_id, input_utxo.index)
                if utxo_key in self.utxo_set:
                    del self.utxo_set[utxo_key]

            # 添加新生成的 output_utxo
            for output_utxo in transaction.output_utxo:
                utxo_key = (output_utxo.tx_id, output_utxo.index)
                self.utxo_set[utxo_key] = output_utxo

    def remove_duplicate_transactions(self, block_transactions):
        """从交易池中移除与新区块重复的交易"""
        block_tx_ids = {hash(tx) for tx in block_transactions}
        self.mempool = [tx for tx in self.mempool if hash(tx) not in block_tx_ids]
        self.create_candidate_block()
