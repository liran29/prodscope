#!/usr/bin/env python3
"""
Prodscope FastAPI 服务启动脚本
使用方法: python start_api.py
"""

import uvicorn
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """启动FastAPI服务"""
    print("🚀 启动 Prodscope FastAPI 服务...")
    print("📍 API文档地址: http://localhost:8000/api/docs")
    print("🔄 重新加载模式: 已启用")
    print("🌐 CORS支持: 已启用 (允许前端访问)")
    print("-" * 50)
    
    # 启动服务 - 使用模块导入字符串格式
    uvicorn.run(
        "src.api.main:app",  # 模块导入字符串
        host="0.0.0.0",
        port=8000,
        reload=True,         # 启用自动重载
        log_level="debug",
        access_log=True
    )

if __name__ == "__main__":
    main()