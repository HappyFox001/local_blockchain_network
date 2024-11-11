bitcoin_local_network_platform/
├── core/
│   ├── blockchain/
│   │   ├── __init__.py
│   │   ├── block.py         # 区块结构
│   │   ├── chain.py         # 链结构
│   │   ├── transaction.py   # 交易结构
│   ├── methods/
│   │   ├── __init__.py
│   │   ├── methods.py       # blockchain文件中三种类的方法
├── node/
│   ├── __init__.py
│   ├── network.py           # 节点间通信逻辑
│   ├── node.py              # 单个节点的逻辑和生命周期管理
│   └── sync.py              # 管理节点存储的区块链
│
├── algorithms/
│   ├── __init__.py
│   ├── encryption.py        # 加密算法和数字签名
│   └── merkle_tree.py       # Merkle树算法
|
├── wallet/
│   ├── __init__.py
│   ├── wallet.py           # 钱包主逻辑，创建钱包，签名交易，发送交易，代币查询
|
├── frontend/
│   ├── static/              # 静态资源，如CSS、JavaScript、图标等
│   ├── templates/           # HTML模板
│   ├── src/                 # 前端源代码
│   │   ├── App.vue           # 主应用文件
│   │   ├── components/      # 前端组件
│   │   ├── services/        # 前端与后端通信的服务（如API调用）
│   └── public/              # 前端公开资源
│
├── api/
│   ├── __init__.py
│   ├── routes.py            # 路由和API接口
│   ├── auth.py              # 用户认证相关的API逻辑
│   ├── transaction.py       # 交易API
│   └── block.py             # 区块和链相关的API
│
├── config/
│   ├── settings.py          # 平台的配置文件（网络设置、数据库连接等）
│   ├── logging.py           # 日志相关配置
│   └── network.json         # 网络节点的配置信息
│
├── docs/
│   ├── README.md            # 项目概述
│   ├── API_DOCS.md          # API文档
│   ├── INSTALLATION.md      # 安装和使用说明
│   └── ARCHITECTURE.md      # 系统架构和设计文档
│
├── scripts/
│   ├── start_node.sh        # 启动节点的脚本
│   ├── stop_node.sh         # 停止节点的脚本
│   └── reset_chain.sh       # 重置区块链数据的脚本
│
├── tests/
│   ├── unit/                # 单元测试
│   ├── integration/         # 集成测试
│   └── functional/          # 功能测试
|   └── start.py/            # 启动测试
│
└── utils/
    ├── __init__.py
    ├── helpers.py           # 辅助工具函数
    └── logger.py            # 日志记录工具
    