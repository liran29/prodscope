#!/bin/bash

# Prodscope集成测试脚本

echo "====================================="
echo "     Prodscope 集成测试"
echo "====================================="
echo ""

# 测试API服务状态
echo "1. 测试API服务状态..."
curl -s http://localhost:8000/ | python -m json.tool
echo ""

# 测试健康检查
echo "2. 测试健康检查端点..."
curl -s http://localhost:8000/api/health | python -m json.tool
echo ""

# 测试聊天API
echo "3. 测试聊天API..."
curl -s -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，请介绍一下Prodscope系统", "user_id": "test"}' \
  | python -m json.tool
echo ""

# 测试数据源状态
echo "4. 测试数据源状态API..."
curl -s http://localhost:8000/api/data-sources/status | python -m json.tool | head -30
echo ""

# 测试分析启动
echo "5. 测试分析启动API..."
curl -s -X POST http://localhost:8000/api/analysis/start \
  -H "Content-Type: application/json" \
  -d '{"query": "分析沃尔玛圣诞装饰品市场", "analysis_type": "six_layer_insight"}' \
  | python -m json.tool
echo ""

echo "====================================="
echo "     测试完成！"
echo "====================================="
echo ""
echo "提示："
echo "- API文档: http://localhost:8000/api/docs"
echo "- 前端地址: http://localhost:5173"