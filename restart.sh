#!/bin/bash

# 停止 API 服务
pkill -f "python3 api.py"

python3 api.py &
