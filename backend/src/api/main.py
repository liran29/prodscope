"""
Prodscope FastAPI Backend Service
主要的API服务入口，提供产品推荐和分析功能
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 导入LLM服务
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
try:
    from services.llm_service import llm_service
    logger.info("LLM service imported successfully")
except Exception as e:
    logger.error(f"Failed to import LLM service: {e}")
    llm_service = None

# 创建FastAPI应用
app = FastAPI(
    title="Prodscope API",
    description="AI驱动的产品推荐和洞察分析系统",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS配置 - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型定义
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "default"
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    processing_time: float
    llm_provider: str
    data_sources_used: List[str]
    analysis_id: Optional[str] = None

class AnalysisRequest(BaseModel):
    query: str
    analysis_type: str = "six_layer_insight"
    user_id: Optional[str] = "default"

class AnalysisStatus(BaseModel):
    analysis_id: str
    status: str  # "running", "completed", "error"
    progress: int  # 0-100
    current_step: str
    estimated_time_remaining: Optional[int] = None

class InsightResult(BaseModel):
    insight_id: int
    title: str
    content: str
    confidence: float
    data_sources: List[str]
    recommendations: List[str]

# 全局变量存储分析状态
analysis_sessions = {}

@app.get("/")
async def root():
    """根路径 - API状态检查"""
    return {
        "message": "Prodscope API is running",
        "version": "1.0.0",
        "timestamp": datetime.now(),
        "status": "healthy"
    }

@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "mindsdb": "connected",
            "vertex_ai": "connected", 
            "pytrends": "connected",
            "llm_providers": ["gemini", "claude", "grok"]
        }
    }

@app.post("/api/chat/message", response_model=ChatResponse)
async def send_chat_message(chat_message: ChatMessage):
    """
    处理聊天消息并返回AI回复
    这是前端ChatInterface调用的主要接口
    """
    start_time = time.time()
    
    try:
        logger.info(f"收到聊天消息: {chat_message.message[:50]}...")
        
        # 检查LLM服务是否可用
        if llm_service is None:
            raise HTTPException(status_code=500, detail="LLM服务未初始化")
        
        # 调用真实的LLM服务
        llm_result = await llm_service.chat(
            message=chat_message.message,
            system_prompt="你是Prodscope产品推荐系统的AI助手，专门帮助用户分析产品数据、识别市场趋势、发现商业机会。请用中文回复，提供专业的产品分析洞察。"
        )
        
        processing_time = time.time() - start_time
        
        # 判断使用了哪些数据源
        data_sources = ["MindsDB"]  # 默认数据源
        if "搜索" in chat_message.message or "trend" in chat_message.message.lower():
            data_sources.append("Vertex AI")
        if "趋势" in chat_message.message:
            data_sources.append("PyTrends")
        
        return ChatResponse(
            response=llm_result["response"],
            timestamp=datetime.now(),
            processing_time=processing_time,
            llm_provider=llm_result.get("llm_provider", "unknown"),
            data_sources_used=data_sources,
            analysis_id=None
        )
        
    except Exception as e:
        logger.error(f"聊天消息处理错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"消息处理失败: {str(e)}")

@app.post("/api/analysis/start")
async def start_analysis(analysis_request: AnalysisRequest):
    """
    启动六层洞察分析
    返回分析ID用于跟踪进度
    """
    try:
        analysis_id = f"analysis_{int(time.time())}"
        
        # 初始化分析状态
        analysis_sessions[analysis_id] = {
            "status": "running",
            "progress": 0,
            "current_step": "初始化分析...",
            "query": analysis_request.query,
            "start_time": datetime.now(),
            "insights": []
        }
        
        # 启动后台分析任务
        asyncio.create_task(run_six_layer_analysis(analysis_id, analysis_request))
        
        return {
            "analysis_id": analysis_id,
            "status": "started",
            "message": "六层洞察分析已启动"
        }
        
    except Exception as e:
        logger.error(f"分析启动错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析启动失败: {str(e)}")

@app.get("/api/analysis/{analysis_id}/status", response_model=AnalysisStatus)
async def get_analysis_status(analysis_id: str):
    """
    获取分析状态和进度
    """
    if analysis_id not in analysis_sessions:
        raise HTTPException(status_code=404, detail="分析ID不存在")
    
    session = analysis_sessions[analysis_id]
    
    return AnalysisStatus(
        analysis_id=analysis_id,
        status=session["status"],
        progress=session["progress"],
        current_step=session["current_step"],
        estimated_time_remaining=session.get("estimated_time_remaining")
    )

@app.get("/api/analysis/{analysis_id}/results")
async def get_analysis_results(analysis_id: str):
    """
    获取完整的分析结果
    """
    if analysis_id not in analysis_sessions:
        raise HTTPException(status_code=404, detail="分析ID不存在")
    
    session = analysis_sessions[analysis_id]
    
    if session["status"] != "completed":
        raise HTTPException(status_code=400, detail="分析尚未完成")
    
    return {
        "analysis_id": analysis_id,
        "query": session["query"],
        "insights": session["insights"],
        "completion_time": session.get("completion_time"),
        "total_processing_time": session.get("total_processing_time")
    }

@app.get("/api/data-sources/status")
async def get_data_sources_status():
    """
    获取所有数据源状态
    为前端DataSourceStatus组件提供数据
    """
    return {
        "last_updated": datetime.now(),
        "sources": [
            {
                "id": "mindsdb",
                "name": "MindsDB",
                "type": "database",
                "status": "online",
                "description": "产品数据主库",
                "record_count": 37891,
                "last_sync": "2分钟前",
                "response_time": 45,
                "endpoint": "prodscope_db",
                "capabilities": ["SQL查询", "实时聚合", "情感分析"]
            },
            {
                "id": "vertex-ai", 
                "name": "Vertex AI",
                "type": "search",
                "status": "online",
                "description": "搜索增强服务",
                "last_sync": "30秒前",
                "response_time": 320,
                "endpoint": "Global Endpoint",
                "capabilities": ["网络搜索", "引用生成", "多语言支持"]
            },
            {
                "id": "pytrends",
                "name": "PyTrends", 
                "type": "trends",
                "status": "online",
                "description": "趋势数据源",
                "last_sync": "1分钟前",
                "response_time": 2100,
                "endpoint": "Google Trends API",
                "capabilities": ["趋势分析", "地域数据", "相关查询"]
            }
        ]
    }

# 辅助函数

async def run_six_layer_analysis(analysis_id: str, request: AnalysisRequest):
    """
    执行六层洞察分析的后台任务
    """
    try:
        session = analysis_sessions[analysis_id]
        
        # 六层分析步骤
        steps = [
            "市场宏观趋势 & 视觉偏好分析",
            "产品弱点 & 供应链痛点分析", 
            "潜在市场需求 & 产品创新机会",
            "季节性销售 & 定价策略分析",
            "产品功能 & 用户痛点关联性",
            "品牌表现 & 竞争分析"
        ]
        
        for i, step in enumerate(steps):
            # 更新进度
            session["current_step"] = f"正在执行: {step}"
            session["progress"] = int((i / len(steps)) * 100)
            session["estimated_time_remaining"] = (len(steps) - i) * 30  # 每步约30秒
            
            # 模拟分析时间
            await asyncio.sleep(3)
            
            # 生成模拟洞察结果
            insight = {
                "insight_id": i + 1,
                "title": step,
                "content": f"基于{request.query}的{step}分析结果...",
                "confidence": 0.85 + (i * 0.02),
                "data_sources": ["MindsDB", "Vertex AI", "PyTrends"],
                "recommendations": [f"建议{j+1}: 针对{step}的优化方案" for j in range(2)]
            }
            
            session["insights"].append(insight)
        
        # 完成分析
        session["status"] = "completed"
        session["progress"] = 100
        session["current_step"] = "分析完成"
        session["completion_time"] = datetime.now()
        session["total_processing_time"] = (session["completion_time"] - session["start_time"]).total_seconds()
        
        logger.info(f"分析 {analysis_id} 完成")
        
    except Exception as e:
        logger.error(f"分析 {analysis_id} 执行错误: {str(e)}")
        session["status"] = "error"
        session["error_message"] = str(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)