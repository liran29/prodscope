#!/usr/bin/env python
"""
测试Vertex AI Gemini搜索功能
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 确保加载正确的.env文件
current_dir = os.path.dirname(__file__)  # tests/trying/
backend_dir = os.path.dirname(os.path.dirname(current_dir))  # backend/
env_path = os.path.join(backend_dir, '.env')
print(f"Loading .env from: {env_path}")
print(f".env exists: {os.path.exists(env_path)}")
load_dotenv(env_path)

# 添加src路径
sys.path.append(os.path.join(backend_dir, 'src'))

def test_vertex_ai_setup():
    """测试Vertex AI设置"""
    print("="*60)
    print("Testing Vertex AI Setup")
    print("="*60)
    
    # 检查环境变量
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    if not project_id:
        print("❌ GOOGLE_CLOUD_PROJECT not set in .env")
        print("   Please update backend/.env with your GCP project ID")
        return False
    
    print(f"✅ Project ID: {project_id}")
    
    if credentials_path and os.path.exists(credentials_path):
        print(f"✅ Credentials file: {credentials_path}")
    else:
        print(f"⚠️ Credentials file not found: {credentials_path}")
        print("   Will try default application credentials")
    
    return True

def test_vertex_ai_import():
    """测试Vertex AI依赖"""
    print("\n" + "="*60)
    print("Testing Vertex AI Dependencies")
    print("="*60)
    
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        print("✅ Vertex AI dependencies imported")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("Install with: pip install google-cloud-aiplatform")
        return False

def test_vertex_ai_client():
    """测试Vertex AI客户端"""
    print("\n" + "="*60)
    print("Testing Vertex AI Client")
    print("="*60)
    
    try:
        from utils.vertex_ai_client import VertexAIGeminiClient
        
        print("🔄 Initializing Vertex AI client...")
        client = VertexAIGeminiClient()
        
        print(f"✅ Client initialized successfully")
        print(f"   Project: {client.project_id}")
        print(f"   Location: {client.location}")
        
        return True, client
        
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if Google Cloud project exists")
        print("2. Verify API is enabled: gcloud services list --enabled")
        print("3. Check authentication: gcloud auth list")
        return False, None

def test_basic_generation():
    """测试基础生成功能"""
    print("\n" + "="*60)
    print("Testing Basic Generation")
    print("="*60)
    
    setup_result = test_vertex_ai_client()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        print("🔄 Testing basic text generation...")
        
        result = client.generate(
            "List 3 current trends in smart home technology. Be concise.",
            temperature=0.3
        )
        
        if result and result.get('text'):
            print("✅ Basic generation successful")
            print(f"📄 Response length: {len(result['text'])} characters")
            print(f"\n📝 Response preview:")
            print(result['text'][:300] + "...")
            
            # 显示使用统计
            if result.get('usage'):
                usage = result['usage']
                print(f"\n📊 Token usage:")
                print(f"   Input tokens: {getattr(usage, 'prompt_token_count', 'N/A')}")
                print(f"   Output tokens: {getattr(usage, 'candidates_token_count', 'N/A')}")
            
            return True
        else:
            print("❌ No response generated")
            return False
            
    except Exception as e:
        print(f"❌ Basic generation failed: {e}")
        return False

def test_search_functionality():
    """测试搜索功能"""
    print("\n" + "="*60)
    print("Testing Search Functionality")
    print("="*60)
    
    setup_result = test_vertex_ai_client()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        print("🔍 Testing Google Search integration...")
        
        result = client.search(
            "Search for current market trends in wireless earbuds for 2024",
            temperature=0.2
        )
        
        if result and result.get('text'):
            print("✅ Search functionality working")
            print(f"📄 Response length: {len(result['text'])} characters")
            print(f"🔗 Citations found: {len(result.get('citations', []))}")
            
            # 显示引用
            citations = result.get('citations', [])
            if citations:
                print("\n📚 Sources:")
                for i, citation in enumerate(citations[:3], 1):
                    title = citation.get('title', 'No title')[:50]
                    uri = citation.get('uri', 'No URI')
                    print(f"   {i}. {title}... - {uri}")
                if len(citations) > 3:
                    print(f"   ... and {len(citations) - 3} more sources")
            
            print(f"\n📝 Search results preview:")
            print(result['text'][:400] + "...")
            
            return True
        else:
            print("❌ No search results")
            return False
            
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        print("\nPossible issues:")
        print("1. Search API not enabled in GCP project")
        print("2. Insufficient permissions")
        print("3. API quota exceeded")
        return False

def test_product_analysis():
    """测试产品分析功能"""
    print("\n" + "="*60)
    print("Testing Product Analysis")
    print("="*60)
    
    setup_result = test_vertex_ai_client()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        print("📊 Analyzing product trends...")
        
        result = client.analyze_product_trends("smart watches")
        
        if result and result.get('text'):
            print("✅ Product analysis completed")
            
            analysis = result['text'].lower()
            
            # 检查分析要素
            components = [
                ("Market data", "market" in analysis or "size" in analysis),
                ("Brand mentions", "apple" in analysis or "samsung" in analysis or "brand" in analysis),
                ("Price analysis", "price" in analysis or "cost" in analysis),
                ("Features discussed", "feature" in analysis or "battery" in analysis),
                ("Competition", "competitor" in analysis or "competitive" in analysis)
            ]
            
            print("\n📊 Analysis components:")
            for name, present in components:
                status = "✅" if present else "❌"
                print(f"   {status} {name}")
            
            coverage = sum(1 for _, present in components if present)
            print(f"\nCoverage: {coverage}/5 components")
            
            print(f"\n📝 Analysis preview:")
            print(result['text'][:500] + "...")
            
            return coverage >= 3  # Success if 3+ components covered
        else:
            print("❌ No analysis generated")
            return False
            
    except Exception as e:
        print(f"❌ Product analysis failed: {e}")
        return False

def test_competitive_analysis():
    """测试竞争分析"""
    print("\n" + "="*60)
    print("Testing Competitive Analysis")
    print("="*60)
    
    setup_result = test_vertex_ai_client()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        print("🏪 Comparing products...")
        
        result = client.compare_products("AirPods", "Galaxy Buds")
        
        if result and result.get('text'):
            print("✅ Competitive analysis completed")
            
            analysis = result['text'].lower()
            
            # 检查对比要素
            elements = [
                ("Both products mentioned", "airpods" in analysis and ("galaxy" in analysis or "samsung" in analysis)),
                ("Market share discussed", "market share" in analysis or "popularity" in analysis),
                ("Pricing comparison", "price" in analysis and ("cheaper" in analysis or "expensive" in analysis or "cost" in analysis)),
                ("Features compared", "feature" in analysis and ("battery" in analysis or "sound" in analysis or "noise" in analysis)),
                ("Consumer preference", "prefer" in analysis or "review" in analysis or "rating" in analysis)
            ]
            
            print("\n⚖️ Comparison elements:")
            for name, present in elements:
                status = "✅" if present else "❌"
                print(f"   {status} {name}")
            
            coverage = sum(1 for _, present in elements if present)
            
            print(f"\n📈 Comparison quality: {coverage}/5 elements")
            print(f"\n📝 Comparison preview:")
            print(result['text'][:500] + "...")
            
            return coverage >= 3
        else:
            print("❌ No comparison generated")
            return False
            
    except Exception as e:
        print(f"❌ Competitive analysis failed: {e}")
        return False

def main():
    """运行所有Vertex AI测试"""
    print("Vertex AI Gemini Search Test Suite")
    print("="*60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = []
    
    # 运行测试
    results.append(("Environment Setup", test_vertex_ai_setup()))
    results.append(("Dependencies", test_vertex_ai_import()))
    
    # 只有前面的测试通过才继续
    if all(r[1] for r in results):
        results.append(("Client Initialization", test_vertex_ai_client()[0]))
        results.append(("Basic Generation", test_basic_generation()))
        results.append(("Search Functionality", test_search_functionality()))
        results.append(("Product Analysis", test_product_analysis()))
        results.append(("Competitive Analysis", test_competitive_analysis()))
    
    # 总结
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:25} : {status}")
    
    print(f"\nTotal: {sum(r[1] for r in results)}/{len(results)} tests passed")
    
    if not results[0][1]:
        print("\n💡 Setup Requirements:")
        print("1. Create Google Cloud project")
        print("2. Enable Vertex AI API")
        print("3. Create service account and download key")
        print("4. Update GOOGLE_CLOUD_PROJECT in .env")
        print("5. Set GOOGLE_APPLICATION_CREDENTIALS path")
        print("\n📖 See: backend/docs/vertex-ai-setup-guide.md")
    elif sum(r[1] for r in results) == len(results):
        print("\n🎉 All Vertex AI tests passed!")
        print("✅ Gemini搜索功能已就绪")
        print("✅ 可以开始使用Vertex AI进行产品分析")
        print("✅ 地域限制问题已解决")
    else:
        failed_count = len(results) - sum(r[1] for r in results)
        print(f"\n⚠️ {failed_count} tests failed")
        print("Check individual test outputs for troubleshooting steps")

if __name__ == "__main__":
    main()