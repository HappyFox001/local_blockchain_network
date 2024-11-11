import socket
import pickle
import random
import threading


class Network:
    def __init__(self, name, host, port, peers=[]):
        self.name = name
        self.host = host
        self.port = port
        self.peers = peers

    def add_peer(self, peer_address):
        if peer_address not in self.peers:
            self.peers.append(peer_address)
            print(self.peers)

    def send_message(self, message, peer_address):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(peer_address)
                s.sendall(pickle.dumps(message))
        except Exception as e:
            print(f"无法发送消息到 {peer_address}: {e}")

    def broadcast_gossip(self, message, exclude=[]):
        target_peers = [peer for peer in self.peers if peer not in exclude]
        random.shuffle(target_peers)

        for peer in target_peers[: len(target_peers)]:
            self.send_message(message, peer)

    def start_listening(self, handle_message):
        def listen():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                print(f"节点{self.name}正在监听 {self.host}:{self.port}")
                while True:
                    conn, _ = s.accept()
                    data = b""
                    while True:
                        part = conn.recv(1024)
                        data += part
                        if len(part) < 1024:
                            break
                    try:
                        message = pickle.loads(data)
                    except EOFError:
                        print("接收到不完整的数据，可能连接已关闭。")
                    except Exception as e:
                        print(f"反序列化消息时出错: {e}")
                    handle_message(message)
                    conn.close()

        listen_thread = threading.Thread(target=listen)
        listen_thread.start()
