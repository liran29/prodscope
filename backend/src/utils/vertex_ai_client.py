#!/usr/bin/env python
"""
Vertex AI Gemini客户端 - 支持全球访问的解决方案
"""

import os
import json
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VertexAIGeminiClient:
    """Vertex AI Gemini客户端，支持全球访问"""
    
    def __init__(self):
        self.project_id = None
        self.location = None
        self.model = None
        self._initialize()
    
    def _initialize(self):
        """初始化Vertex AI客户端"""
        try:
            import vertexai
            from vertexai.generative_models import GenerativeModel, Tool
            
            # 获取配置
            self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            self.location = os.getenv('GOOGLE_CLOUD_LOCATION', 'global')
            
            if not self.project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
            
            # 设置认证
            self._setup_auth()
            
            # 初始化Vertex AI
            vertexai.init(
                project=self.project_id,
                location=self.location
            )
            
            # 初始化模型
            self.model = GenerativeModel("gemini-2.0-flash")
            self.Tool = Tool
            
            print(f"✅ Vertex AI initialized: project={self.project_id}, location={self.location}")
            
        except ImportError as e:
            raise ImportError(
                "Vertex AI dependencies not installed. "
                "Run: pip install google-cloud-aiplatform"
            ) from e
        except Exception as e:
            raise Exception(f"Failed to initialize Vertex AI: {e}") from e
    
    def _setup_auth(self):
        """设置认证"""
        # 方法1: 使用服务账户密钥文件
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            print(f"✅ Using service account key file: {credentials_path}")
            return
        
        # 方法2: 使用JSON字符串
        credentials_json = os.getenv('GOOGLE_CLOUD_CREDENTIALS')
        if credentials_json:
            try:
                # 验证JSON格式
                json.loads(credentials_json)
                # 写入临时文件
                temp_path = '/tmp/gcp_credentials.json'
                with open(temp_path, 'w') as f:
                    f.write(credentials_json)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_path
                print("✅ Using service account JSON from environment")
                return
            except json.JSONDecodeError:
                pass
        
        # 方法3: 使用默认认证（本地开发）
        print("⚠️ Using default application credentials")
        print("   Run 'gcloud auth application-default login' if needed")
    
    def search(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """使用Google Search执行搜索"""
        try:
            # 使用正确的Vertex AI Tool格式
            search_tool = self.Tool.from_dict({
                "google_search": {}
            })
            
            # 生成内容
            response = self.model.generate_content(
                prompt,
                tools=[search_tool],
                generation_config={
                    "temperature": kwargs.get('temperature', 0.3),
                    "top_p": kwargs.get('top_p', 0.8),
                    "top_k": kwargs.get('top_k', 40),
                    "max_output_tokens": kwargs.get('max_tokens', 2048),
                }
            )
            
            # 解析响应
            result = {
                'text': response.text,
                'usage': getattr(response, 'usage_metadata', None),
                'citations': [],
                'grounding_metadata': None
            }
            
            # 提取引用信息
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                
                # 获取grounding metadata
                if hasattr(candidate, 'grounding_metadata'):
                    result['grounding_metadata'] = candidate.grounding_metadata
                    
                    # 提取引用
                    if candidate.grounding_metadata and hasattr(candidate.grounding_metadata, 'grounding_chunks'):
                        for chunk in candidate.grounding_metadata.grounding_chunks:
                            if hasattr(chunk, 'web') and chunk.web:
                                result['citations'].append({
                                    'title': chunk.web.title,
                                    'uri': chunk.web.uri
                                })
            
            return result
            
        except Exception as e:
            raise Exception(f"Search failed: {e}") from e
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """生成内容（无搜索）"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": kwargs.get('temperature', 0.7),
                    "top_p": kwargs.get('top_p', 0.8),
                    "top_k": kwargs.get('top_k', 40),
                    "max_output_tokens": kwargs.get('max_tokens', 2048),
                }
            )
            
            return {
                'text': response.text,
                'usage': getattr(response, 'usage_metadata', None)
            }
            
        except Exception as e:
            raise Exception(f"Generation failed: {e}") from e
    
    def analyze_product_trends(self, product: str) -> Dict[str, Any]:
        """分析产品趋势"""
        prompt = f"""
        Search for current market trends and consumer preferences for {product} in 2024-2025.
        
        Focus on:
        1. Market size and growth trends
        2. Popular brands and models
        3. Price trends and segments
        4. Key features consumers are looking for
        5. Competitive landscape
        6. Emerging opportunities
        
        Provide a comprehensive analysis with specific data points and sources.
        """
        
        return self.search(prompt, temperature=0.2)
    
    def compare_products(self, product_a: str, product_b: str) -> Dict[str, Any]:
        """对比两个产品"""
        prompt = f"""
        Search for and compare {product_a} vs {product_b} in the current market.
        
        Compare:
        1. Market share and popularity
        2. Pricing strategies
        3. Target demographics
        4. Feature differences
        5. Consumer reviews and satisfaction
        6. Sales performance
        
        Provide a detailed comparison with supporting data from reliable sources.
        """
        
        return self.search(prompt, temperature=0.1)
    
    def identify_market_opportunities(self, category: str) -> Dict[str, Any]:
        """识别市场机会"""
        prompt = f"""
        Search for market opportunities and gaps in the {category} industry for 2024-2025.
        
        Identify:
        1. Underserved market segments
        2. Emerging technologies with commercial potential
        3. Consumer pain points not adequately addressed
        4. Trending product categories with growth potential
        5. Regional market opportunities
        6. Investment and funding trends
        
        Provide specific opportunities with supporting market data and trends.
        """
        
        return self.search(prompt, temperature=0.4)

# 便捷函数
def create_vertex_client() -> VertexAIGeminiClient:
    """创建Vertex AI客户端实例"""
    return VertexAIGeminiClient()

def test_vertex_connection() -> bool:
    """测试Vertex AI连接"""
    try:
        client = create_vertex_client()
        
        # 简单测试
        result = client.generate("Hello, this is a test.")
        
        if result and result.get('text'):
            print("✅ Vertex AI connection test successful")
            return True
        else:
            print("❌ Vertex AI connection test failed - no response")
            return False
            
    except Exception as e:
        print(f"❌ Vertex AI connection test failed: {e}")
        return False

if __name__ == "__main__":
    # 测试连接
    test_vertex_connection()