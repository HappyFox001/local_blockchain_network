import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from core.blockchain.transaction import Transaction
from core.methods.methods import hash
from algorithms.encryption import sign_data  # 用于签名


class Wallet:
    def __init__(self, private_key=None):
        if private_key:
            # 加载已有私钥
            self.private_key = serialization.load_pem_private_key(
                private_key.encode(), password=None
            )
        else:
            # 生成新的私钥和公钥对
            self.private_key = ec.generate_private_key(ec.SECP256K1())

        self.public_key = self.private_key.public_key()
        self.encode_public_key = self.get_public_key()
        self.address = self.generate_address()  # 生成钱包地址

    def generate_address(self):

        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.CompressedPoint,
        )
        sha256_hash = hashlib.sha256(public_bytes).digest()
        ripemd160 = hashlib.new("ripemd160")
        ripemd160.update(sha256_hash)
        return ripemd160.hexdigest()

    def sign_transaction(self, transaction):
        """使用私钥对交易哈希进行签名"""
        transaction.signature = sign_data(self.private_key, hash(transaction).encode())

    def get_private_key(self):
        """导出私钥为 PEM 格式，便于存储"""
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

    def get_public_key(self):
        """导出公钥为 PEM 格式"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def get_balance(self, node):
        """查询当前钱包地址的余额"""
        balance = node.get_balance_for_address(self.address)
        print(f"当前余额: {balance}")
        return balance

    def send_transaction(self, recipient, amount, node):
        transaction = Transaction(
            self.address, self.encode_public_key, recipient, amount
        )
        self.sign_transaction(transaction)
        transaction_id = node.generate_message_id(message_type="transaction")
        message = {
            "type": "transaction",
            "id": transaction_id,
            "content": transaction,
            "name": node.name,
        }
        node.handle_message(message)
