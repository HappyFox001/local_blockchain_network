import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from core.blockchain.transaction import UTXO
from node.node import Node
from wallet.wallet import Wallet
import time
from api.network_manager import NetworkManager

manager = NetworkManager()


def test_transaction_flow():
    node = Node(name="节点1", manager=manager)
    node.start()  # 启动节点 1
    node.start_mining()
    manager.add_node(node)
    node2 = Node(name="节点2", manager=manager)
    node2.start()  # 启动节点 2
    node2.start_mining()
    manager.add_node(node2)

    send_wallet = Wallet()
    reciver_wallet = Wallet()

    # 添加初始 UTXO 到节点的 UTXO 集合
    initial_utxo = UTXO(
        tx_id="genesis", index=0, amount=100, recipient=send_wallet.address
    )
    node.add_utxo(initial_utxo)
    node2.add_utxo(initial_utxo)
    # time.sleep(5)

    # # 生成交易
    send_wallet.send_transaction(
        recipient=reciver_wallet.address, amount=50, node=node2
    )

    # 开始挖矿

    # 检查余额
    while True:
        time.sleep(2)
        print("从节点1检查余额")
        reciver_wallet.get_balance(node)
        send_wallet.get_balance(node)
        print("从节点2检查余额")
        reciver_wallet.get_balance(node2)
        send_wallet.get_balance(node2)


# 运行测试
test_transaction_flow()
