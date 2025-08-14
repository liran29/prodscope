# 必须使用Gemini Search的解决方案

## 方案对比

### 方案1：Vertex AI + 企业账户（推荐）

#### 优势
- **官方支持**：Google正式企业方案
- **全球访问**：使用Global Endpoint自动路由
- **功能完整**：支持所有Gemini功能包括搜索
- **稳定可靠**：企业级SLA保证

#### 实施步骤
```python
# 1. 安装Vertex AI SDK
pip install google-cloud-aiplatform

# 2. 设置项目
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

# 3. 初始化（支持全球访问）
vertexai.init(
    project="your-gcp-project-id",
    location="global"  # 关键：使用全球端点
)

# 4. 使用Gemini搜索
model = GenerativeModel("gemini-2.0-flash")
response = model.generate_content(
    "Search for latest smart home trends 2024",
    tools=[{"google_search": {}}],
    generation_config={"temperature": 0.3}
)
```

#### 成本估算
- **免费额度**：每月$300信用额度（新用户）
- **实际成本**：
  - Gemini Pro: $0.00025/1K tokens
  - Gemini Flash: $0.000075/1K tokens
  - 搜索工具：按使用计费

### 方案2：代理服务器（快速实现）

#### 架构设计
```
中国用户 → 海外代理服务器 → Gemini API → 返回结果
```

#### 实施方案

##### 2.1 使用云服务商
选择支持地区的云服务器：
- **AWS**: us-east-1, ap-northeast-1
- **Google Cloud**: us-central1, asia-northeast1  
- **Azure**: East US, Japan East
- **Vultr/DigitalOcean**: 美国、新加坡节点

##### 2.2 代理服务代码
```python
# proxy_server.py（部署在海外服务器）
from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

@app.route('/gemini-search', methods=['POST'])
def gemini_search_proxy():
    try:
        # 初始化Gemini客户端
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
        # 获取请求数据
        data = request.json
        prompt = data.get('prompt')
        
        # 调用Gemini搜索
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "tools": [{"google_search": {}}],
                "temperature": data.get('temperature', 0.3)
            }
        )
        
        return jsonify({
            'success': True,
            'text': response.text,
            'citations': getattr(response, 'grounding_metadata', None)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

##### 2.3 客户端调用
```python
# backend/src/utils/gemini_proxy_client.py
import requests
import json

class GeminiProxyClient:
    def __init__(self, proxy_url):
        self.proxy_url = proxy_url
    
    def search(self, prompt, **kwargs):
        """通过代理调用Gemini搜索"""
        payload = {
            'prompt': prompt,
            'temperature': kwargs.get('temperature', 0.3)
        }
        
        response = requests.post(
            f"{self.proxy_url}/gemini-search",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"代理请求失败: {response.text}")

# 使用示例
client = GeminiProxyClient("https://your-proxy-server.com")
result = client.search("分析2024年智能家居市场趋势")
```

### 方案3：第三方Gemini代理服务

#### 商用代理服务
```python
# 使用第三方代理（如OneAPI、ChatGPT-Next-Web等）
import openai

# 配置代理服务
openai.api_base = "https://your-proxy-service.com/v1"
openai.api_key = "your-proxy-key"

# 调用（通过OpenAI兼容接口）
response = openai.ChatCompletion.create(
    model="gemini-pro",  # 代理服务映射到Gemini
    messages=[
        {"role": "system", "content": "Use Google Search to find information"},
        {"role": "user", "content": "搜索2024年电商趋势"}
    ]
)
```

### 方案4：边缘函数部署

#### Vercel Edge Functions
```typescript
// api/gemini-proxy.ts
import { NextRequest, NextResponse } from 'next/server'

export const config = {
  runtime: 'edge',
}

export default async function handler(req: NextRequest) {
  const { prompt } = await req.json()
  
  const response = await fetch('https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.GEMINI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      tools: [{ googleSearch: {} }],
    }),
  })
  
  return NextResponse.json(await response.json())
}
```

#### Cloudflare Workers
```javascript
// gemini-proxy-worker.js
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 200, headers: corsHeaders })
  }
  
  const { prompt } = await request.json()
  
  const response = await fetch(GEMINI_API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GEMINI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      tools: [{ googleSearch: {} }]
    }),
  })
  
  return new Response(await response.text(), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  })
}
```

## Google Trends解决方案

### PyTrends优化（已验证可用）
```python
# backend/src/utils/trends_client.py
import warnings
import pandas as pd
from pytrends.request import TrendReq
from contextlib import contextmanager

# 抑制警告
pd.set_option('future.no_silent_downcasting', True)

@contextmanager
def suppress_warnings():
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=FutureWarning)
        yield

class OptimizedTrendsClient:
    def __init__(self):
        with suppress_warnings():
            self.pytrends = TrendReq(
                hl='en-US', 
                tz=360,
                requests_args={'verify': False}
            )
    
    def get_product_trends(self, keywords, timeframe='today 3-m'):
        """获取产品趋势数据"""
        with suppress_warnings():
            self.pytrends.build_payload(
                kw_list=keywords[:3],  # 限制关键词数量
                timeframe=timeframe,
                geo='US'
            )
            return self.pytrends.interest_over_time()
    
    def compare_products(self, product_a, product_b):
        """对比两个产品的趋势"""
        data = self.get_product_trends([product_a, product_b])
        if not data.empty:
            return {
                'winner': data.mean().idxmax(),
                'data': data.to_dict(),
                'summary': f"{product_a} vs {product_b} 趋势对比"
            }
        return None
```

## 推荐实施方案

### 阶段1：立即可用（1-2天）
1. **申请Google Cloud账户**
2. **启用Vertex AI API**
3. **配置Global Endpoint**
4. **测试Gemini搜索功能**

### 阶段2：稳定部署（1周内）
1. **部署代理服务**（作为备选方案）
2. **集成PyTrends客户端**
3. **实现故障切换机制**

### 阶段3：生产优化（2周内）
1. **监控和日志**
2. **成本控制**
3. **性能优化**

## 具体实施指南

### 立即行动步骤
```bash
# 1. 安装Vertex AI
pip install google-cloud-aiplatform

# 2. 创建GCP项目
gcloud projects create prodscope-analysis

# 3. 启用必要APIs
gcloud services enable aiplatform.googleapis.com

# 4. 创建服务账户
gcloud iam service-accounts create gemini-client

# 5. 下载密钥文件
gcloud iam service-accounts keys create key.json \
  --iam-account=gemini-client@prodscope-analysis.iam.gserviceaccount.com
```

### 测试代码
```python
# test_vertex_ai.py
import vertexai
from vertexai.generative_models import GenerativeModel
import os

# 设置认证
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

# 初始化
vertexai.init(project="prodscope-analysis", location="global")

# 测试搜索功能
model = GenerativeModel("gemini-2.0-flash")
response = model.generate_content(
    "Search for current trends in wireless earbuds market",
    tools=[{"google_search": {}}]
)

print("搜索结果:", response.text)
```

## 总结

由于项目必须使用Gemini搜索，建议优先选择 **Vertex AI + Global Endpoint** 方案，这是最官方、最稳定的解决方案。同时保持PyTrends作为Google Trends数据源，已验证可用。

如需帮助实施具体方案，请告知偏好的实施路径。