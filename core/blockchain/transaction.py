class UTXO:
    """未花费交易输出 (UTXO) 类"""

    def __init__(self, tx_id, index, amount, recipient):
        self.tx_id = tx_id  # 交易ID
        self.index = index  # 输出索引
        self.amount = amount  # 输出金额
        self.recipient = recipient  # 收款方地址

    def __repr__(self):
        return f"UTXO(tx_id={self.tx_id}, index={self.index}, amount={self.amount}, recipient={self.recipient})"


class Transaction:
    """简化的交易类，包含发送者地址、接收者地址和金额"""

    def __init__(self, sender_address, public_key, recipient_address, amount):
        self.sender_address = sender_address  # 发送方地址
        self.public_key = public_key
        self.recipient_address = recipient_address  # 接收方地址
        self.amount = amount  # 交易金额
        self.signature = None  # 签名
        self.input_utxo = []
        self.output_utxo = []

    # def hash(self):
    #     """生成交易的哈希值"""
    #     tx_data = json.dumps(
    #         {
    #             "sender": self.sender_address,
    #             "recipient": self.recipient_address,
    #             "amount": self.amount,
    #         },
    #         sort_keys=True,
    #     )
    #     return sha256(tx_data)


class CoinbaseTransaction(Transaction):
    """区块奖励交易类，仅包含接收者地址和奖励金额"""

    def __init__(self, recipient_address, reward_amount):
        super().__init__(
            sender_address="coinbase",
            public_key=None,
            recipient_address=recipient_address,
            amount=reward_amount,
        )
        # 设置 coinbase 特定属性
        self.signature = "coinbase"  # coinbase交易不需验证签名
        self.input_utxo = []
        self.output_utxo = []

    # def hash(self):
    #     """生成 coinbase 交易的唯一哈希值"""
    #     tx_data = json.dumps(
    #         {
    #             "sender": self.sender_address,
    #             "recipient": self.recipient_address,
    #             "amount": self.amount,
    #         },
    #         sort_keys=True,
    #     )
    #     return sha256(tx_data)
