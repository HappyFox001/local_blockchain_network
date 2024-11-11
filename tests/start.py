import os
import sys
import time


# 设置项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from node.node import Node
from core.methods.methods import hash
from api.network_manager import NetworkManager
from api.api import manager

nodes = []


def start_nodes(num_nodes=5):
    for i in range(num_nodes):
        node = Node(name=f"节点{i}", manager=manger)
        manger.add_node(node)
        node.start()
        manger.start_node_mining(node.name)
        nodes.append(node)
    return nodes


# def print_chain_status(nodes):
#     """每5秒打印每个节点的链状态"""
#     while True:
#         time.sleep(5)
#         print("\n当前区块链状态:")
#         for node in nodes:
#             chain = node.sync.chain.blocks
#             print(f"{node.name} 的区块链:")
#             for block in chain:
#                 print(f"  - 高度: {block.height}, 哈希: {hash(block.header)}")

#         print("-" * 40)


# 启动5个节点
if __name__ == "__main__":
    nodes = start_nodes()
    # 启动链状态打印线程
    # threading.Thread(target=print_chain_status, args=(nodes,), daemon=True).start()

    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
            # manger.store_block_info()
    except KeyboardInterrupt:
        print("终止节点...")
