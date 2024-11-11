from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization


def generate_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1())  # SECP256R1 是常用的椭圆曲线
    public_key = private_key.public_key()
    return private_key, public_key


def sign_data(private_key, data):
    signature = private_key.sign(
        data, ec.ECDSA(hashes.SHA256())  # 使用 ECDSA 和 SHA256 进行签名
    )
    return signature


def verify_signature(public_key_bytes, data, signature):
    try:
        # 将字节形式的公钥反序列化为公钥对象
        public_key = serialization.load_pem_public_key(public_key_bytes)

        # 使用反序列化后的公钥验证签名
        public_key.verify(
            signature, data, ec.ECDSA(hashes.SHA256())  # 使用 ECDSA 和 SHA256 进行验证
        )
        return True
    except Exception:
        return False
