#!/bin/bash

# 启动 API 服务
cd api
python3 api.py &

# 启动主程序
# cd ../tests
# python3 start.py &

# 启动前端
cd ../frontend
npm run dev &
