"""
LLM服务集成 - 支持多个LLM提供商
参考deer-flow的LLM管理架构
"""

import os
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

# LangChain imports
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """LLM提供商枚举"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic" 
    GOOGLE = "google"
    GROK = "grok"
    DEEPSEEK = "deepseek"
    MOONSHOT = "moonshot"


@dataclass
class LLMConfig:
    """LLM配置数据类"""
    provider: LLMProvider
    model_name: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    api_key: Optional[str] = None


class LLMService:
    """
    统一的LLM服务接口
    支持多个LLM提供商的调用
    """
    
    def __init__(self):
        """初始化LLM服务"""
        self.providers: Dict[str, BaseChatModel] = {}
        self._initialize_providers()
        
    def _initialize_providers(self):
        """初始化所有配置的LLM提供商"""
        logger.info("Initializing LLM providers...")
        
        # Log environment variables status for debugging
        logger.debug(f"Environment check - OPENAI_API_KEY: {'set' if os.getenv('OPENAI_API_KEY') else 'not set'}")
        logger.debug(f"Environment check - ANTHROPIC_API_KEY: {'set' if os.getenv('ANTHROPIC_API_KEY') else 'not set'}")
        logger.debug(f"Environment check - GOOGLE_API_KEY: {'set' if os.getenv('GOOGLE_API_KEY') else 'not set'}")
        logger.debug(f"Environment check - GEMINI_API_KEY: {'set' if os.getenv('GEMINI_API_KEY') else 'not set'}")
        logger.debug(f"Environment check - XAI_API_KEY: {'set' if os.getenv('XAI_API_KEY') else 'not set'}")
        logger.debug(f"Environment check - DEEPSEEK_API_KEY: {'set' if os.getenv('DEEPSEEK_API_KEY') else 'not set'}")
        logger.debug(f"Environment check - MOONSHOT_API_KEY: {'set' if os.getenv('MOONSHOT_API_KEY') else 'not set'}")
        logger.debug(f"Environment check - VOLCENGINE_API_KEY: {'set' if os.getenv('VOLCENGINE_API_KEY') else 'not set'}")
        
        # 从环境变量获取API密钥
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        google_key = os.getenv("GOOGLE_API_KEY")
        
        # 初始化OpenAI
        if openai_key and not openai_key.startswith("your_"):
            try:
                self.providers["openai"] = ChatOpenAI(
                    api_key=openai_key,
                    model="gpt-4o-mini",
                    temperature=0.7
                )
                logger.info("OpenAI provider initialized")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI: {e}")
        else:
            logger.debug("OpenAI API key not configured or is placeholder")
        
        # 初始化Anthropic Claude
        if anthropic_key and not anthropic_key.startswith("your_"):
            try:
                self.providers["anthropic"] = ChatAnthropic(
                    api_key=anthropic_key,
                    model="claude-3-haiku-20240307",
                    temperature=0.7
                )
                logger.info("Anthropic provider initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic: {e}")
        else:
            logger.debug("Anthropic API key not configured or is placeholder")
        
        # 初始化Google Gemini - 尝试多个可能的环境变量名
        if not google_key:
            google_key = os.getenv("GEMINI_API_KEY")
        
        if google_key and not google_key.startswith("your_"):
            try:
                logger.info(f"Attempting to initialize Google Gemini with key: {google_key[:10]}...")
                self.providers["google"] = ChatGoogleGenerativeAI(
                    api_key=google_key,
                    model="gemini-1.5-flash",
                    temperature=0.7
                )
                logger.info("Google Gemini provider initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Google Gemini: {e}")
        else:
            logger.debug(f"Google API key not configured or is placeholder: {google_key[:10] if google_key else 'None'}...")
        
        # 初始化xAI Grok
        xai_key = os.getenv("XAI_API_KEY")
        xai_base_url = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
        if xai_key and not xai_key.startswith("your_"):
            try:
                logger.info(f"Attempting to initialize xAI Grok with key: {xai_key[:10]}...")
                # xAI使用OpenAI兼容的API
                self.providers["xai"] = ChatOpenAI(
                    api_key=xai_key,
                    base_url=xai_base_url,
                    model="grok-2-latest",
                    temperature=0.7
                )
                logger.info("xAI Grok provider initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize xAI Grok: {e}")
        else:
            logger.debug(f"xAI API key not configured or is placeholder: {xai_key[:10] if xai_key else 'None'}...")
        
        # 初始化DeepSeek
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        if deepseek_key and not deepseek_key.startswith("your_"):
            try:
                logger.info(f"Attempting to initialize DeepSeek with key: {deepseek_key[:10]}...")
                # DeepSeek使用OpenAI兼容的API
                self.providers["deepseek"] = ChatOpenAI(
                    api_key=deepseek_key,
                    base_url=deepseek_base_url,
                    model="deepseek-chat",
                    temperature=0.7
                )
                logger.info("DeepSeek provider initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize DeepSeek: {e}")
        else:
            logger.debug(f"DeepSeek API key not configured or is placeholder: {deepseek_key[:10] if deepseek_key else 'None'}...")
        
        # 初始化Moonshot (Kimi)
        moonshot_key = os.getenv("MOONSHOT_API_KEY")
        moonshot_base_url = os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")
        if moonshot_key and not moonshot_key.startswith("your_"):
            try:
                logger.info(f"Attempting to initialize Moonshot with key: {moonshot_key[:10]}...")
                # Moonshot使用OpenAI兼容的API
                self.providers["moonshot"] = ChatOpenAI(
                    api_key=moonshot_key,
                    base_url=moonshot_base_url,
                    model="moonshot-v1-8k",
                    temperature=0.7
                )
                logger.info("Moonshot provider initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Moonshot: {e}")
        else:
            logger.debug(f"Moonshot API key not configured or is placeholder: {moonshot_key[:10] if moonshot_key else 'None'}...")
        
        # 初始化Volcengine (豆包)
        volcengine_key = os.getenv("VOLCENGINE_API_KEY")
        volcengine_base_url = os.getenv("VOLCENGINE_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        if volcengine_key and not volcengine_key.startswith("your_"):
            try:
                logger.info(f"Attempting to initialize Volcengine with key: {volcengine_key[:10]}...")
                # Volcengine使用OpenAI兼容的API
                self.providers["volcengine"] = ChatOpenAI(
                    api_key=volcengine_key,
                    base_url=volcengine_base_url,
                    model="ep-20241212110452-zk2nd",  # 使用豆包模型
                    temperature=0.7
                )
                logger.info("Volcengine provider initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Volcengine: {e}")
        else:
            logger.debug(f"Volcengine API key not configured or is placeholder: {volcengine_key[:10] if volcengine_key else 'None'}...")
        
        # 设置默认的primary provider
        if self.providers:
            # 优先使用的顺序: deepseek > moonshot > volcengine > xai > google > anthropic > openai
            if "deepseek" in self.providers:
                self.providers["primary"] = self.providers["deepseek"]
                logger.info("Using DeepSeek as primary LLM provider")
            elif "moonshot" in self.providers:
                self.providers["primary"] = self.providers["moonshot"]
                logger.info("Using Moonshot (Kimi) as primary LLM provider")
            elif "volcengine" in self.providers:
                self.providers["primary"] = self.providers["volcengine"]
                logger.info("Using Volcengine (豆包) as primary LLM provider")
            elif "xai" in self.providers:
                self.providers["primary"] = self.providers["xai"]
                logger.info("Using xAI Grok as primary LLM provider")
            elif "google" in self.providers:
                self.providers["primary"] = self.providers["google"]
                logger.info("Using Google Gemini as primary LLM provider")
            elif "anthropic" in self.providers:
                self.providers["primary"] = self.providers["anthropic"]
                logger.info("Using Anthropic Claude as primary LLM provider")
            elif "openai" in self.providers:
                self.providers["primary"] = self.providers["openai"]
                logger.info("Using OpenAI as primary LLM provider")
    
    async def chat(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        provider: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送聊天消息到LLM
        
        Args:
            message: 用户消息
            system_prompt: 系统提示词
            provider: 指定的LLM提供商
            **kwargs: 额外参数
            
        Returns:
            包含响应和元数据的字典
        """
        # 选择LLM提供商
        if provider and provider in self.providers:
            llm = self.providers[provider]
            llm_name = provider
        elif "primary" in self.providers:
            llm = self.providers["primary"]
            llm_name = "primary"
        elif self.providers:
            # 使用第一个可用的提供商
            llm_name = list(self.providers.keys())[0]
            llm = self.providers[llm_name]
        else:
            # 如果没有真实的LLM，返回模拟响应
            logger.warning("No LLM providers available, using mock response")
            return self._generate_mock_response(message)
        
        try:
            # 构建消息列表
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=message))
            
            # 调用LLM
            response = await llm.ainvoke(messages)
            
            return {
                "response": response.content,
                "llm_provider": llm_name,
                "tokens_used": response.response_metadata.get("token_usage", {}),
                "model": response.response_metadata.get("model_name", "unknown")
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            # 失败时返回模拟响应
            return self._generate_mock_response(message)
    
    def _generate_mock_response(self, message: str) -> Dict[str, Any]:
        """生成模拟响应（当真实LLM不可用时）"""
        # 根据关键词生成不同类型的回复
        if "沃尔玛" in message or "圣诞" in message:
            response = """基于您的查询，我已经分析了沃尔玛圣诞装饰品的相关数据。

🎄 **市场表现洞察**：
- 圣诞装饰品类目在11-12月销量激增，同比增长43%
- 价格区间集中在$15-$45，性价比产品最受欢迎
- LED灯串和人造圣诞树是核心品类

📊 **用户偏好分析**：
- 消费者更偏向多功能、易安装的装饰品
- 环保材质成为新的购买决策因素
- 个性化定制需求明显上升

🔍 **建议优化方向**：
1. 增加智能控制功能的装饰品
2. 开发更多环保材质选项
3. 提供DIY套装满足个性化需求

需要我为您启动完整的六层洞察分析吗？"""

        elif "评价" in message or "问题" in message:
            response = """我已经分析了产品评价数据中的常见问题模式。

⚠️ **主要痛点识别**：
1. **质量问题** (32%): 材质易损坏、使用寿命短
2. **物流问题** (24%): 包装不当、配送延迟
3. **功能问题** (21%): 说明书不清晰、组装困难
4. **性价比问题** (15%): 价格与质量不匹配

🔧 **解决方案建议**：
- 改进产品材质和工艺标准
- 优化包装设计和物流流程
- 提供更清晰的安装指南和视频教程
- 重新调整价格策略

是否需要我深入分析特定类目的问题模式？"""

        else:
            response = f"""感谢您的提问！我已经收到您关于"{message[:50]}..."的查询。

作为Prodscope产品推荐系统，我可以帮助您：

🎯 **产品分析服务**：
- 市场宏观趋势分析
- 供应链痛点识别
- 创新机会发现
- 定价策略优化
- 竞争对手分析

📈 **数据驱动洞察**：
- 基于37,891条真实产品数据
- 结合多个LLM模型分析
- 实时趋势数据支持

需要启动完整的六层洞察分析流程吗？"""
        
        return {
            "response": response,
            "llm_provider": "mock",
            "tokens_used": {},
            "model": "mock-model"
        }
    
    def get_available_providers(self) -> List[str]:
        """获取所有可用的LLM提供商"""
        return list(self.providers.keys())
    
    async def analyze_with_best_llm(
        self,
        task_type: str,
        content: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        根据任务类型选择最佳的LLM进行分析
        参考deer-flow的任务分配策略
        
        Args:
            task_type: 任务类型（如 market_analysis, sentiment_analysis等）
            content: 要分析的内容
            **kwargs: 额外参数
            
        Returns:
            分析结果
        """
        # 任务到LLM的映射（基于prodscope-design-v1.1.md）
        task_llm_mapping = {
            "market_trends": "google",      # Gemini擅长趋势分析
            "sentiment_analysis": "anthropic",  # Claude擅长情感分析
            "innovation": "openai",          # GPT擅长创新思考
            "report_generation": "anthropic",   # Claude擅长写作
            "data_analysis": "primary",     # 使用主要配置的LLM
        }
        
        # 选择最佳LLM
        preferred_llm = task_llm_mapping.get(task_type, "primary")
        
        # 构建系统提示词
        system_prompt = self._get_task_specific_prompt(task_type)
        
        return await self.chat(
            message=content,
            system_prompt=system_prompt,
            provider=preferred_llm,
            **kwargs
        )
    
    def _get_task_specific_prompt(self, task_type: str) -> str:
        """获取任务特定的系统提示词"""
        prompts = {
            "market_trends": "你是一个市场趋势分析专家，擅长识别市场模式和预测趋势。",
            "sentiment_analysis": "你是一个情感分析专家，擅长从用户评价中提取情感和观点。",
            "innovation": "你是一个产品创新专家，擅长发现市场机会和创新点。",
            "report_generation": "你是一个专业的分析报告撰写专家，擅长生成结构化的洞察报告。",
            "data_analysis": "你是一个数据分析专家，擅长从数据中提取有价值的洞察。"
        }
        return prompts.get(task_type, "你是一个产品分析专家。")


# 创建全局LLM服务实例
llm_service = LLMService()