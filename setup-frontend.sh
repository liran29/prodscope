#!/bin/bash

# ProdScope Frontend Setup Script
# Usage: From project root: ./setup-frontend.sh

set -e  # Exit on any error

echo "🚀 Starting ProdScope Frontend Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_status "Node.js version: $(node --version)"
print_status "npm version: $(npm --version)"

# Navigate to prodscope root directory (script is in root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_status "Working directory: $(pwd)"

# Step 1: Create Vite React TypeScript project
print_status "Step 1: Creating Vite React TypeScript project..."
if [ -d "frontend" ]; then
    print_warning "Frontend directory already exists. Removing it..."
    rm -rf frontend
fi

npm create vite@latest frontend -- --template react-ts
print_success "Vite project created"

# Step 2: Navigate to frontend directory
cd frontend

# Step 3: Install core dependencies
print_status "Step 2: Installing core dependencies..."

# UI Components
print_status "Installing UI components..."
npm install \
    @radix-ui/react-slot \
    @radix-ui/react-tabs \
    @radix-ui/react-scroll-area \
    @radix-ui/react-tooltip \
    @radix-ui/react-select \
    @radix-ui/react-collapsible \
    class-variance-authority \
    clsx \
    tailwind-merge \
    lucide-react

print_success "UI components installed"

# Charts and Visualization
print_status "Installing chart libraries..."
npm install recharts
print_success "Chart libraries installed"

# Markdown rendering
print_status "Installing markdown support..."
npm install react-markdown
print_success "Markdown support installed"

# LangGraph integration
print_status "Installing LangGraph SDK..."
npm install @langchain/langgraph-sdk @langchain/core
print_success "LangGraph SDK installed"

# Development dependencies
print_status "Installing development dependencies..."
npm install -D \
    @types/node \
    tailwindcss \
    @tailwindcss/vite \
    postcss \
    autoprefixer

print_success "Development dependencies installed"

# Step 4: Configure Tailwind CSS 4.x (New Architecture)
print_status "Step 3: Configuring Tailwind CSS 4.x..."

# Update vite.config.ts for Tailwind CSS 4.x
cat > vite.config.ts << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: {
    host: '0.0.0.0',
    port: 5173
  }
})
EOF

# Create tailwind.config.js for Tailwind CSS 4.x
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
}
EOF

print_success "Tailwind CSS configured"

# Step 5: Update CSS with design system (Tailwind CSS 4.x)
print_status "Step 4: Setting up design system..."
cat > src/index.css << 'EOF'
@import "tailwindcss";

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 84% 4.9%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 84% 4.9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 84% 4.9%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 94.1%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}

/* ProdScope specific styles */
.prodscope-container {
  @apply min-h-screen bg-background;
}

.three-column-layout {
  @apply grid grid-cols-1 lg:grid-cols-4 gap-6 p-6;
}

.workflow-panel {
  @apply lg:col-span-1;
}

.insights-panel {
  @apply lg:col-span-2;
}

.interaction-panel {
  @apply lg:col-span-1;
}

.insight-card {
  @apply mb-4 transition-all duration-200 hover:shadow-lg;
}

.chart-container {
  @apply w-full h-64 mt-4;
}
EOF

print_success "Design system configured"

# Step 6: Create basic project structure
print_status "Step 5: Creating project structure..."

# Create directories
mkdir -p src/components/{ui,agent-workflow,visualizations,insights,chat}
mkdir -p src/lib
mkdir -p src/types
mkdir -p src/data

print_success "Project structure created"

# Step 7: Create utility files
print_status "Step 6: Creating utility files..."

# Create utils
cat > src/lib/utils.ts << 'EOF'
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
EOF

# Create types
cat > src/types/index.ts << 'EOF'
export interface Insight {
  id: string
  title: string
  description: string
  llm: string
  status: 'pending' | 'processing' | 'completed' | 'error'
  dataSource: string
  dataCount: number
  chartData?: any[]
  type: 'trend' | 'comparison' | 'correlation' | 'heatmap'
}

export interface DataSource {
  name: string
  table: string
  count: number
  description: string
}

export interface LLMTask {
  llm: 'Gemini' | 'Claude' | 'Grok' | 'GPT-4o'
  task: string
  status: 'idle' | 'processing' | 'completed'
  progress: number
}

export interface ProductRecommendation {
  id: string
  title: string
  description: string
  rationale: string
  insights: string[]
  priority: 'high' | 'medium' | 'low'
}
EOF

print_success "Utility files created"

# Step 8: Update package.json scripts
print_status "Step 7: Updating package.json scripts..."
npm pkg set scripts.dev="vite --host 0.0.0.0 --port 5173"
npm pkg set scripts.build="tsc && vite build"
npm pkg set scripts.preview="vite preview --host 0.0.0.0 --port 4173"

# Step 9: Create basic App.tsx
print_status "Step 8: Creating basic App component..."
cat > src/App.tsx << 'EOF'
import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="prodscope-container">
      <header className="bg-primary text-primary-foreground p-4">
        <h1 className="text-2xl font-bold">ProdScope - 产品分析与推荐系统</h1>
        <p className="text-sm opacity-90">AI驱动的六层洞察分析演示</p>
      </header>
      
      <main className="three-column-layout">
        <aside className="workflow-panel">
          <div className="bg-card p-4 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">Agent工作流</h2>
            <p className="text-muted-foreground">六层洞察分析进度将在这里显示</p>
          </div>
        </aside>
        
        <section className="insights-panel">
          <div className="bg-card p-4 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">洞察结果</h2>
            <p className="text-muted-foreground">分析结果和可视化图表将在这里展示</p>
          </div>
        </section>
        
        <aside className="interaction-panel">
          <div className="bg-card p-4 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">数据源 & 交互</h2>
            <p className="text-muted-foreground">数据源信息和聊天界面将在这里展示</p>
          </div>
        </aside>
      </main>
      
      <footer className="bg-muted p-4 text-center">
        <p className="text-muted-foreground">ProdScope Frontend v1.0 - 基础架构已完成</p>
      </footer>
    </div>
  )
}

export default App
EOF

# Clean up default CSS
cat > src/App.css << 'EOF'
/* ProdScope specific component styles */
EOF

print_success "Basic App component created"

# Step 10: Create development environment file
print_status "Step 9: Creating environment configuration..."
cat > .env.example << 'EOF'
# ProdScope Frontend Environment Variables
VITE_API_URL=http://localhost:8000
VITE_LANGGRAPH_API_URL=http://localhost:2024
VITE_APP_TITLE=ProdScope
VITE_APP_VERSION=1.0.0
EOF

cp .env.example .env

print_success "Environment configuration created"

# Step 11: Create README
print_status "Step 10: Creating documentation..."
cat > README.md << 'EOF'
# ProdScope Frontend

AI驱动的产品分析与推荐系统前端应用

## 🚀 快速开始

### 开发环境启动
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

### 预览生产构建
```bash
npm run preview
```

## 📁 项目结构

```
src/
├── components/           # 组件目录
│   ├── ui/              # 基础UI组件
│   ├── agent-workflow/  # Agent工作流组件
│   ├── visualizations/  # 数据可视化组件
│   ├── insights/        # 洞察展示组件
│   └── chat/           # 聊天交互组件
├── lib/                # 工具函数
├── types/              # TypeScript类型定义
├── data/               # Mock数据
└── App.tsx             # 主应用组件
```

## 🎯 核心功能

- **六层洞察分析**: 市场趋势、痛点分析、机会识别等
- **Agent工作流可视化**: LLM任务分配和进度展示
- **数据可视化**: 图表展示分析结果
- **实时交互**: 轻量级聊天界面
- **数据溯源**: 清晰的数据来源展示

## 🛠️ 技术栈

- **React 18** + **TypeScript**
- **Vite** - 构建工具
- **Tailwind CSS** - 样式框架
- **Recharts** - 图表库
- **LangGraph SDK** - AI工作流集成
- **Radix UI** - 无障碍UI组件

## 📊 集成的分析框架

基于 `prodscope-design-v1.1.md` 的六层洞察系统:

1. 市场宏观趋势与视觉偏好分析
2. 产品优劣势与供应链痛点分析  
3. 潜在市场需求与产品创新机会
4. 季节性销售与价格策略精细化分析
5. 产品功能与用户痛点的精细化关联
6. 品牌市场表现与竞品对比分析

## 🔗 后端集成

- **MindsDB**: 电商数据分析
- **Vertex AI**: 搜索增强
- **PyTrends**: 趋势数据
- **Multi-LLM**: Gemini, Claude, Grok协同

---

Generated by ProdScope Setup Script
EOF

print_success "Documentation created"

# Final success message
echo ""
print_success "🎉 ProdScope Frontend setup completed successfully!"
echo ""
print_status "Next steps:"
echo "  1. cd frontend"
echo "  2. npm run dev"
echo "  3. Open http://localhost:5173 in your browser"
echo ""
print_status "Project structure ready for component development!"
echo ""
print_warning "Note: This is the basic setup. You can now start developing components."