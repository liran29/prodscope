# ProdScope - Product Analysis & Recommendation System

## Project Overview
ProdScope is a data-driven product analysis and recommendation system designed to analyze e-commerce data (primarily from Walmart and Amazon) stored in MindsDB, and generate actionable product development recommendations.

## Project Structure (Updated)
```
prodscope/
├── backend/                     # Backend application
│   ├── .env                    # API keys (not committed)
│   ├── .env.example           # API key template
│   ├── conf.yaml              # Main configuration file
│   ├── config/                # Configuration files
│   │   ├── llm_config.yaml    # LLM capabilities and models
│   │   └── task_assignments.yaml # Task-specific LLM assignments
│   ├── docs/                  # Backend documentation
│   ├── src/                   # Source code
│   │   └── llm/              # LLM management system
│   │       ├── __init__.py
│   │       └── llm_manager.py # Multi-LLM manager
│   └── tests/                 # Backend tests
│       └── trying/           # Experimental tests
├── frontend/                   # Frontend application (planned)
├── docs/                      # Project documentation
├── requirements.txt           # Python dependencies
└── .venv/                     # Python virtual environment
```

## Core Requirements

### Data Sources (in MindsDB `prodscope_db`)
- `walmart_products` (1,139 products) - Product catalog with specifications
- `walmart_product_reviews` (12,142 reviews) - Customer reviews with sentiment
- `walmart_categories` (209 categories) - Product categorization
- `amazon_products` (3,000 products) - Competitor product data
- `amazon_reviews` (21,311 reviews) - Competitor review data

### Analysis Framework (Six-Layer Insight System)
Based on `prodscope-design-v1.1.md`, our comprehensive analysis framework consists of:

1. **Market Macro Trends & Visual Preference Analysis** - Flow trends tracking, visual style analysis, trend prediction
2. **Product Weaknesses & Supply Chain Pain Points Analysis** - Negative review analysis, pain point categorization, quality issues identification
3. **Potential Market Demand & Product Innovation Opportunities** - Market gap identification, potential evaluation, underserved niche discovery
4. **Seasonal Sales & Pricing Strategy Analysis** - Price band segmentation, promotion pattern recognition, seasonal rhythm optimization
5. **Product Function & User Pain Point Correlation** - Feature keyword extraction, sentiment-function correlation, optimization recommendations
6. **Brand Performance & Competitive Analysis** - Brand performance aggregation, competitive brand analysis, user loyalty insights

**Dynamic Analysis Strategy:**
- **Phase 1**: Post-event Analysis (retrospective market performance evaluation)  
- **Phase 2**: Mid-term Prediction (cross-validation with external data and trends)
- **Phase 3**: Real-time Tracking (live performance monitoring and rapid response)

**Insight Combination Framework:**
- **High-Quality Mass Market Products** (Insights 1+2)
- **Innovative Niche Products** (Insights 3+6) 
- **Performance-Upgraded Premium Products** (Insights 5+4)
- **High-End Art Design Products** (Insights 1+6)

### Multi-LLM System
**Configured Providers:**
- **Google Gemini** - High-quality reasoning, multilingual support
- **xAI Grok** - Creative analysis, real-time insights (currently active)
- **OpenAI GPT** - Consistent performance, versatile tasks
- **Anthropic Claude** - Excellent writing, detailed analysis
- **DeepSeek, Moonshot, Volcengine** - Additional options

**Task-Specific Assignments (Aligned with Six-Layer Framework):**
- **Market Macro Trends & Visual Analysis** → Gemini Pro (complex reasoning, multimodal)
- **Supply Chain Pain Points Analysis** → Claude (nuanced analysis, detailed extraction)
- **Innovation Opportunities Identification** → Grok (creative insights, market gaps)
- **Seasonal Sales & Pricing Strategy** → GPT-4o (consistent performance, quantitative analysis)
- **Function-Pain Point Correlation** → Claude (sentiment analysis, feature correlation)
- **Brand & Competitive Analysis** → Gemini Pro (comprehensive reasoning, cross-platform comparison)
- **Dynamic Analysis Orchestration** → Grok (real-time insights, trend prediction)
- **Report Generation & Insight Combination** → Claude (superior writing, synthesis)

## Technology Stack Updates (2025-08-14)

### Google GenAI 1.30.0 New Capabilities
**Advanced Search & Retrieval:**
- `GoogleSearch`、`GoogleMaps` - Native Google search and maps integration
- `UrlContext` - URL context tool for enhanced search results
- `VertexAISearch`、`RagRetrieval` - Enterprise-grade search and RAG retrieval

**Real-time Multimedia:**
- `live` and `live_music` modules - Real-time audio conversations and music generation  
- 30+ new language audio output support
- Veo 3.0 video generation (with audio)

**Multi-tool Integration:**
- `ToolComputerUse` - Project Mariner browser control capabilities
- `ToolCodeExecution` - Code execution tools
- Multi-tool simultaneous use (search + code execution)

**Batch Processing & Caching:**
- `batches` - Async batch processing requests
- `caches` - Content caching management
- `operations` - Long-running operation management

**Model Fine-tuning:**
- `tunings` - Complete model fine-tuning framework
- Supervised learning and model distillation support

### LangGraph 0.6.5 & LangChain 0.3.27 New Features
**LangGraph 0.6+ Major Updates:**
- **Context API** - New pattern for passing run-scoped context with enhanced type safety
- **Durability Control** - Fine-grained persistence control with new `durability` argument
- **Node Caching** - Cache individual node results to skip redundant computation
- **Deferred Nodes** - Delay execution until all upstream paths complete
- **Pre/Post Model Hooks** - Custom logic before/after model calls for guardrails
- **Built-in Provider Tools** - Web search, RemoteMCP tools out of the box

**LangChain 0.3+ Updates:**
- **Pydantic v2 Migration** - Full internal upgrade from Pydantic 1 to 2
- **Enhanced Type Safety** - Improved type checking throughout the framework
- **LangSmith Integration** - Better observability with trace-to-log connections
- **Python 3.13 Support** - Full compatibility with latest Python version

## Development Status

### ✅ Completed (Phase 1)
- **Directory Structure**: Backend/frontend separation
- **MindsDB Integration**: Connection tested, data verified
- **Multi-LLM System**: 5 providers configured with task-specific assignments
- **Configuration Management**: Secure API key handling, environment-specific configs
- **Test Suite**: Connection, data analysis, LLM integration tests
- **Google GenAI Research**: Native search capabilities verified, 1.30.0 features documented

### 🔄 Current Phase (Phase 2)
- **Analysis Pipeline**: Implement six-layer insight system with dynamic analysis strategy
- **LangGraph Integration**: Workflow orchestration for complex multi-stage analysis
- **Insight Combination Engine**: Four-pattern product recommendation framework
- **Report Generation**: Structured output with quantified insights and actionable recommendations

### 📋 Next Steps (Phase 3)
- **Frontend Development**: React-based dashboard for report visualization
- **API Development**: FastAPI endpoints for analysis requests
- **Production Deployment**: Containerization and hosting setup

## Key Technical Decisions Made

### ✅ Decided
1. **Data Source**: MindsDB HTTP API (prodscope_db with real test data)
2. **LLM Strategy**: Multi-provider system with task-specific assignments
3. **Configuration**: YAML-based config (committed) + .env for secrets (not committed)
4. **Framework**: LangChain + LangGraph for AI workflows
5. **Architecture**: Modular backend with separate frontend

### ⏳ Pending
1. Frontend framework selection (React vs Next.js)
2. Deployment strategy (Docker, hosting platform)
3. Real-time vs batch processing approach

## Environment Setup

```bash
# Navigate to backend
cd /mnt/d/HT/market-assistant/prodscope/backend

# Activate virtual environment
source ../.venv/bin/activate  # Linux/Mac
# or
..\.venv\Scripts\activate  # Windows

# Run tests
python tests/trying/test_mindsdb_connection.py
python tests/trying/test_llm_config_system.py
python tests/trying/test_data_analysis.py
```

## Configuration Files

### Main Config (`backend/conf.yaml`)
- Primary LLM selection (currently: Grok)
- Search engine settings (Tavily)
- MindsDB connection parameters
- Feature toggles and domain filters

### LLM Management (`backend/config/`)
- `llm_config.yaml` - Model capabilities and characteristics
- `task_assignments.yaml` - Environment-specific task assignments (dev/prod/budget/premium)

### Environment Variables (`backend/.env`)
- API keys for all LLM providers
- MindsDB connection settings
- Debug and logging configuration

## Important Constraints
- **Security**: API keys separated from code
- **Scalability**: Support for multiple LLM providers and models
- **Flexibility**: Environment-specific configurations
- **Cost Control**: Budget-conscious model assignments available
- **Production-Ready**: 3-4 week development timeline

## References
- **Process Documentation**: `backend/docs/prodscope-design-v1.1.md` (detailed analysis framework and product recommendations)
- **Data Source**: MindsDB `prodscope_db` database
- **Configuration Examples**: See `backend/.env.example` and config files