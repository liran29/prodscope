# Gemini API地域限制解决方案

## 问题说明
错误信息：`User location is not supported for the API use`

这表示你所在的地区（可能是中国大陆）目前不支持直接使用Gemini API。

## 解决方案

### 方案1：使用其他LLM提供商（推荐）

已配置的可用替代方案：
- **OpenAI GPT-4** - 全球可用，功能强大
- **Anthropic Claude** - 优秀的分析能力
- **DeepSeek** - 国内可用，成本效益高
- **Moonshot (月之暗面)** - 国内服务商，稳定可靠
- **Volcengine (火山引擎)** - 字节跳动提供，国内可用

### 方案2：使用代理服务

#### 2.1 VPN方案
- 通过VPN连接到支持的地区（如美国、日本、新加坡）
- 优点：简单直接
- 缺点：可能违反服务条款，增加延迟

#### 2.2 API代理服务
```python
# 使用代理服务器转发请求
import os
os.environ['HTTPS_PROXY'] = 'your-proxy-server:port'
```

### 方案3：使用Google Cloud Vertex AI（企业方案）

```python
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel

# 初始化Vertex AI（可选择支持的区域）
aiplatform.init(
    project="your-project-id",
    location="asia-northeast1"  # 东京区域
)

model = GenerativeModel("gemini-pro")
response = model.generate_content("Your prompt here")
```

支持的亚洲区域：
- `asia-northeast1` (东京)
- `asia-southeast1` (新加坡)
- `asia-south1` (孟买)

### 方案4：使用兼容的国内服务

#### 4.1 通义千问（阿里云）
```python
from dashscope import Generation

response = Generation.call(
    model='qwen-max',
    prompt='分析产品市场趋势'
)
```

#### 4.2 文心一言（百度）
```python
import qianfan

chat_comp = qianfan.ChatCompletion()
resp = chat_comp.do(
    model="ERNIE-4.0-8K",
    messages=[{"role": "user", "content": "市场分析"}]
)
```

## ProdScope项目建议

### 短期方案（立即可用）
1. **主要使用DeepSeek或Moonshot**
   - 已在`llm_config.yaml`中配置
   - 国内可直接访问
   - 成本效益高

2. **使用PyTrends获取趋势数据**
   - 已测试可用
   - 提供Google Trends数据
   - 无需Gemini API

### 中期方案（1-2周）
1. **集成多个国内LLM服务**
   - 分散风险
   - 提高可用性
   - 优化成本

2. **实现智能路由**
   ```python
   class LLMRouter:
       def select_provider(self, task_type, region):
           if region == "CN":
               return self.chinese_providers
           else:
               return self.global_providers
   ```

### 长期方案（1个月+）
1. **部署私有代理服务**
   - 在支持地区部署转发服务
   - 统一API接口
   - 集中管理

2. **申请Vertex AI企业账号**
   - 更稳定的服务
   - 更好的SLA保证
   - 企业级支持

## 立即行动项

1. **测试DeepSeek API**
```bash
python backend/tests/trying/test_llm_providers.py
```

2. **更新任务分配**
编辑 `backend/config/llm_config.yaml`：
```yaml
task_assignments:
  trend_analysis:
    primary:
      provider: "deepseek"
      model: "deepseek-chat"
```

3. **使用PyTrends作为趋势数据源**
```bash
python backend/tests/trying/test_google_trends_fixed.py
```

## 总结

虽然Gemini API在某些地区不可用，但ProdScope项目有多个可行的替代方案：
- **短期**：使用已配置的国内LLM服务
- **数据源**：PyTrends + MindsDB数据
- **长期**：考虑Vertex AI或私有代理

项目可以继续推进，不受Gemini API限制影响。