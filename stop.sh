#!/bin/bash

# 停止前端
pkill -f "npm run dev"

# 停止 API 服务
pkill -f "python3 api.py"

# 停止主程序
# pkill -f "python3 start.py"
