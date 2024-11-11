from core.methods.methods import hash


class Chain:
    def __init__(self):
        self.blocks = []
        self.difficulty = 5
        self.block_time_target = 3 * 1000  # 目标区块生成时间（秒）

    def add_block(self, block):
        # 验证区块，如果有效则添加到链
        if self.validate_block(block, self.difficulty):
            self.blocks.append(block)
            # 每10个区块调整一次难度
            if len(self.blocks) % 10 == 0:
                self.adjust_difficulty(
                    self.blocks[-5], block.header.timestamp, self.block_time_target
                )
            return True
        else:
            return False

    def validate_block(self, block, difficulty):
        # 检查区块哈希是否满足当前难度
        if hash(block.header)[:difficulty] != "0" * difficulty:
            return False

        # 验证区块链接（不是创世区块时）
        if len(self.blocks) > 0:
            previous_block = self.blocks[-1]
            if block.header.previous_hash != hash(previous_block.header):
                return False
        else:
            if block.header.previous_hash != "0" * 64:
                return False
        return True

    # def resolve_conflicts(self, other_chain):
    #     """
    #     解决分叉冲突：如果检测到较长的链，则采用较长链。
    #     """
    #     # 使用最长链规则，选择较长的链
    #     if len(other_chain.blocks) > len(self.blocks):
    #         print("检测到更长链，切换到更长链")
    #         self.blocks = other_chain.blocks
    #         self.difficulty = other_chain.difficulty  # 同步难度
    #     else:
    #         print("保持当前链，不进行替换")

    def adjust_difficulty(self, last_block, current_timestamp, target_time):
        """
        根据区块生成时间间隔调整挖矿难度。
        """
        actual_time_taken = (current_timestamp - last_block.header.timestamp) / 4

        # 调整难度
        if actual_time_taken < target_time:
            # 实际生成时间低于目标时间，提高难度
            self.difficulty = self.difficulty + 1
            # print("区块难度提高，难度为", self.difficulty)
        elif actual_time_taken > target_time:
            # 实际生成时间高于目标时间，降低难度
            self.difficulty = max(1, self.difficulty - 1)
            # print("区块难度降低，难度为", self.difficulty)
        else:
            # 如果时间刚好相等，保持当前难度
            pass

    def get_current_height(self):
        return len(self.blocks)

    def get_block_by_hash(self, hash_data):
        for block in self.blocks:
            if hash(block.header) == hash_data:
                return True
        return False
