from node.seed_node import SeedNode
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict


class NetworkManager:
    # _instance = None  # 用于存储单例实例

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super(NetworkManager, cls).__new__(cls)
    #         cls._instance.__initialized = False
    #     return cls._instance

    def __init__(self):
        self.node_list = {}
        self.mining_threads_pool = ThreadPoolExecutor(max_workers=10)
        self.seed_node = SeedNode("seed_node", self)
        self.add_node(self.seed_node)

    # def create_block_table(self):
    #     # 创建区块表前先删除同名表，确保不重复
    #     with self.db_connection as conn:
    #         conn.execute("DROP TABLE IF EXISTS blocks")
    #         conn.execute(
    #             """
    #             CREATE TABLE blocks (
    #                 height INTEGER,
    #                 block_hash TEXT UNIQUE,
    #                 previous_hash TEXT,
    #                 type TEXT
    #             )
    #         """
    #         )

    def add_node(self, node):
        """将新的 Node 加在 node_list 的前面"""
        # 使用 OrderedDict 来支持在前面插入
        self.node_list = OrderedDict([(node.name, node)] + list(self.node_list.items()))

    def remove_node(self, name):
        del self.node_list[name]

    def start_all_nodes_mining(self):
        for node in self.node_list.values():
            self.start_node_mining(node.name)

    def stop_all_nodes_mining(self):
        for node in self.node_list.values():
            self.stop_node_mining(node.name)

    def restart_all_nodes(self):
        for node in self.node_list.values():
            node.sync.chain.blocks = []
        self.seed_node.create_block_table()

    def start_node_mining(self, name):
        if not self.node_list[name].mineing:
            self.node_list[name].start_mining()
        else:
            pass

    def stop_node_mining(self, name):
        self.node_list[name].stop_mining()

    def shutdown(self):
        for node in self.node_list.values():
            node.stop_mining()
        self.mining_threads_pool.shutdown()

    def calculate_chain(self):
        """计算网络中的区块链状态，标记确认区块和竞争区块"""

    def get_history_transactions(self):
        # 获取历史tranasactions
        pass

    def get_history_blocks(self):
        # 获取历史blocks
        pass

    def send_transaction(self):
        # 发送交易
        pass
