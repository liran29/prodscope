# Vertex AI 设置指南

## 第1步：创建Google Cloud项目

### 1.1 在线创建项目
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 点击"Create Project"或"新建项目"
3. 项目名称：`prodscope-analysis`
4. 项目ID：`prodscope-analysis-2025`（会自动生成唯一ID）

### 1.2 使用gcloud CLI创建（可选）
```bash
# 安装gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# 创建项目
gcloud projects create prodscope-analysis-2025
gcloud config set project prodscope-analysis-2025
```

## 第2步：启用必要的API

### 2.1 在Console中启用
1. 进入项目后，到"API & Services" > "Library"
2. 搜索并启用以下API：
   - **Vertex AI API**
   - **Generative AI API**
   - **Cloud Resource Manager API**

### 2.2 使用gcloud启用
```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

## 第3步：创建服务账户

### 3.1 创建服务账户
```bash
# 创建服务账户
gcloud iam service-accounts create prodscope-gemini \
    --description="Service account for ProdScope Gemini access" \
    --display-name="ProdScope Gemini Client"
```

### 3.2 分配权限
```bash
# 获取项目ID
PROJECT_ID=$(gcloud config get-value project)

# 分配Vertex AI用户权限
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:prodscope-gemini@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# 分配Generative AI权限
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:prodscope-gemini@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/ml.developer"
```

### 3.3 创建并下载密钥文件
```bash
# 创建密钥文件
gcloud iam service-accounts keys create credentials.json \
    --iam-account=prodscope-gemini@$PROJECT_ID.iam.gserviceaccount.com

# 移动到项目目录
mv credentials.json /mnt/d/HT/market-assistant/prodscope/backend/config/
```

## 第4步：配置环境变量

### 4.1 更新.env文件
```bash
# 编辑 backend/.env
GOOGLE_CLOUD_PROJECT=prodscope-analysis-2025
GOOGLE_CLOUD_LOCATION=global
GOOGLE_APPLICATION_CREDENTIALS=/mnt/d/HT/market-assistant/prodscope/backend/config/credentials.json
```

### 4.2 验证配置
```python
# 运行测试
cd /mnt/d/HT/market-assistant/prodscope/backend
python src/utils/vertex_ai_client.py
```

## 第5步：安装依赖

```bash
# 激活虚拟环境
cd /mnt/d/HT/market-assistant/prodscope
source .venv/bin/activate

# 安装Vertex AI依赖
pip install google-cloud-aiplatform google-auth google-auth-oauthlib
```

## 第6步：测试搜索功能

```python
# 创建测试文件
cat > test_vertex_search.py << 'EOF'
from src.utils.vertex_ai_client import create_vertex_client

# 创建客户端
client = create_vertex_client()

# 测试搜索
result = client.search("Search for current trends in wireless earbuds market 2024")
print("搜索结果:", result['text'][:200])
print("引用数量:", len(result['citations']))
EOF

python test_vertex_search.py
```

## 故障排除

### 问题1：认证失败
```bash
# 检查服务账户
gcloud auth list

# 激活服务账户
gcloud auth activate-service-account --key-file=config/credentials.json

# 设置默认认证
gcloud auth application-default login
```

### 问题2：API未启用
```bash
# 检查已启用的API
gcloud services list --enabled

# 启用缺失的API
gcloud services enable aiplatform.googleapis.com
```

### 问题3：权限不足
```bash
# 检查当前权限
gcloud projects get-iam-policy $PROJECT_ID

# 添加缺失权限
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:prodscope-gemini@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.admin"
```

### 问题4：配额限制
1. 到Console > IAM & Admin > Quotas
2. 搜索"Vertex AI API"
3. 申请增加配额

## 成本控制

### 预算警报
```bash
# 创建预算警报
gcloud billing budgets create \
    --billing-account=BILLING_ACCOUNT_ID \
    --display-name="ProdScope Monthly Budget" \
    --budget-amount=50USD \
    --threshold-rules-percent=0.5,0.9,1.0
```

### 估算成本
- **Gemini 2.0 Flash**: $0.075/1K tokens (input), $0.3/1K tokens (output)
- **搜索功能**: 按使用计费
- **每月预算建议**: $50-100 USD

## 快速设置脚本

```bash
#!/bin/bash
# setup_vertex_ai.sh

set -e

echo "Setting up Vertex AI for ProdScope..."

# 设置变量
PROJECT_ID="prodscope-analysis-$(date +%Y%m%d)"
SERVICE_ACCOUNT_NAME="prodscope-gemini"
CREDENTIALS_PATH="backend/config/credentials.json"

echo "Creating project: $PROJECT_ID"
gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID

echo "Enabling APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com

echo "Creating service account..."
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME

echo "Assigning roles..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

echo "Creating credentials..."
gcloud iam service-accounts keys create $CREDENTIALS_PATH \
    --iam-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com

echo "Updating .env file..."
echo "GOOGLE_CLOUD_PROJECT=$PROJECT_ID" >> backend/.env
echo "GOOGLE_APPLICATION_CREDENTIALS=$CREDENTIALS_PATH" >> backend/.env

echo "✅ Vertex AI setup complete!"
echo "Project ID: $PROJECT_ID"
echo "Next: Run 'python backend/src/utils/vertex_ai_client.py' to test"
```

运行脚本：
```bash
chmod +x setup_vertex_ai.sh
./setup_vertex_ai.sh
```