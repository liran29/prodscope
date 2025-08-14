#!/usr/bin/env python
"""
Robust Google Trends test with enhanced timeout handling and retry logic
"""

import pandas as pd
from datetime import datetime, timedelta
import time
import random
import warnings
from functools import wraps

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
warnings.filterwarnings("ignore", category=FutureWarning, module='pytrends')
pd.set_option('future.no_silent_downcasting', True)

def retry_on_failure(max_retries=3, delay_range=(5, 10)):
    """装饰器：失败时重试"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        delay = random.uniform(*delay_range)
                        print(f"   ⚠️ Attempt {attempt + 1} failed: {str(e)[:50]}...")
                        print(f"   ⏳ Retrying in {delay:.1f} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"   ❌ All {max_retries} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator

class RobustPyTrends:
    """增强版PyTrends客户端，具有更好的错误处理和重试机制"""
    
    def __init__(self):
        self.pytrends = None
        self._initialize_client()
    
    @retry_on_failure(max_retries=3, delay_range=(2, 5))
    def _initialize_client(self):
        """初始化PyTrends客户端"""
        from pytrends.request import TrendReq
        
        # 使用更长的超时和重试
        self.pytrends = TrendReq(
            hl='en-US', 
            tz=360,
            timeout=(15, 45),  # 连接超时15s，读取超时45s
            retries=5,         # 增加重试次数
            backoff_factor=2.0 # 重试间隔倍数
        )
        print("✅ Enhanced TrendReq initialized")
    
    @retry_on_failure(max_retries=2, delay_range=(3, 6))
    def get_interest_over_time(self, keywords, timeframe='today 1-m', geo='US'):
        """获取兴趣趋势数据"""
        print(f"🔍 Fetching trends for: {keywords}")
        
        # 添加随机延迟避免限制
        time.sleep(random.uniform(2, 4))
        
        self.pytrends.build_payload(
            kw_list=keywords[:2],  # 限制关键词数量
            timeframe=timeframe,
            geo=geo
        )
        
        return self.pytrends.interest_over_time()
    
    @retry_on_failure(max_retries=2, delay_range=(4, 8))
    def get_interest_by_region(self, keyword, timeframe='today 1-m'):
        """获取地区兴趣数据"""
        print(f"🌍 Fetching regional data for: {keyword}")
        
        time.sleep(random.uniform(3, 5))
        
        self.pytrends.build_payload(
            kw_list=[keyword],
            timeframe=timeframe,
            geo='US'
        )
        
        return self.pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)
    
    @retry_on_failure(max_retries=2, delay_range=(5, 10))
    def compare_keywords(self, keywords, timeframe='today 3-m'):
        """对比关键词趋势"""
        print(f"⚖️ Comparing: {' vs '.join(keywords[:2])}")
        
        time.sleep(random.uniform(4, 7))
        
        self.pytrends.build_payload(
            kw_list=keywords[:2],  # 限制为2个关键词
            timeframe=timeframe,
            geo='US'
        )
        
        data = self.pytrends.interest_over_time()
        
        if not data.empty:
            return {
                'data': data,
                'winner': data[keywords[:2]].mean().idxmax() if len(keywords) >= 2 else keywords[0],
                'summary': {kw: {'avg': data[kw].mean(), 'latest': data[kw].iloc[-1]} 
                           for kw in keywords[:2] if kw in data.columns}
            }
        return None

def test_robust_initialization():
    """测试增强版PyTrends初始化"""
    print("="*60)
    print("Testing Robust PyTrends Initialization")
    print("="*60)
    
    try:
        client = RobustPyTrends()
        return True, client
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False, None

def test_single_keyword_robust():
    """测试单个关键词（增强版）"""
    print("\n" + "="*60)
    print("Testing Single Keyword (Robust)")
    print("="*60)
    
    setup_result = test_robust_initialization()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        # 测试简单关键词
        keyword = "smartphone"
        data = client.get_interest_over_time([keyword], timeframe='today 1-m')
        
        if not data.empty and keyword in data.columns:
            avg_interest = data[keyword].mean()
            latest = data[keyword].iloc[-1]
            
            print(f"✅ Single keyword test successful")
            print(f"   Data points: {len(data)}")
            print(f"   Average interest: {avg_interest:.1f}")
            print(f"   Latest value: {latest}")
            
            return True
        else:
            print("❌ No data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ Single keyword test failed: {e}")
        return False

def test_product_comparison_robust():
    """测试产品对比（增强版）"""
    print("\n" + "="*60)
    print("Testing Product Comparison (Robust)")
    print("="*60)
    
    setup_result = test_robust_initialization()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        # 测试流行产品对比
        products = ["iPhone", "Samsung Galaxy"]
        result = client.compare_keywords(products, timeframe='today 2-m')
        
        if result and result['data'] is not None and not result['data'].empty:
            print(f"✅ Product comparison successful")
            print(f"🏆 Winner: {result['winner']}")
            
            for product, stats in result['summary'].items():
                print(f"   {product}: Avg={stats['avg']:.1f}, Latest={stats['latest']}")
            
            return True
        else:
            print("❌ No comparison data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ Product comparison failed: {e}")
        return False

def test_regional_analysis_robust():
    """测试地区分析（增强版）"""
    print("\n" + "="*60)
    print("Testing Regional Analysis (Robust)")
    print("="*60)
    
    setup_result = test_robust_initialization()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        # 测试地区数据
        keyword = "Black Friday"
        data = client.get_interest_by_region(keyword, timeframe='today 2-m')
        
        if not data.empty:
            # 获取前5个州
            top_states = data.sort_values(keyword, ascending=False).head(5)
            
            print(f"✅ Regional analysis successful")
            print(f"   Data for {len(data)} states/regions")
            print(f"🗺️ Top 5 states for '{keyword}':")
            
            for state, row in top_states.iterrows():
                print(f"   {state}: {row[keyword]}")
            
            return True
        else:
            print("❌ No regional data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ Regional analysis failed: {e}")
        return False

def test_market_trends_robust():
    """测试市场趋势分析（增强版）"""
    print("\n" + "="*60)
    print("Testing Market Trends Analysis (Robust)")
    print("="*60)
    
    setup_result = test_robust_initialization()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        # 分析不同市场类别
        categories = {
            "Smart Home": ["smart home", "alexa"],
            "Wearables": ["smartwatch", "fitness tracker"],
            "Gaming": ["gaming laptop", "ps5"]
        }
        
        results = {}
        
        for category, keywords in list(categories.items())[:2]:  # 限制测试2个类别
            try:
                print(f"\n📈 Analyzing {category}...")
                data = client.get_interest_over_time(keywords, timeframe='today 2-m')
                
                if not data.empty:
                    # 计算主要关键词的趋势
                    main_keyword = keywords[0]
                    if main_keyword in data.columns:
                        avg_interest = data[main_keyword].mean()
                        trend_direction = "📈" if data[main_keyword].iloc[-5:].mean() > data[main_keyword].iloc[:5].mean() else "📉"
                        
                        results[category] = {
                            'avg_interest': avg_interest,
                            'trend': trend_direction,
                            'keyword': main_keyword
                        }
                        
                        print(f"   {main_keyword}: {avg_interest:.1f} avg, {trend_direction}")
                
            except Exception as e:
                print(f"   ⚠️ {category} analysis failed: {str(e)[:50]}...")
        
        if results:
            print(f"\n📊 Market Trends Summary:")
            hottest = max(results.keys(), key=lambda k: results[k]['avg_interest'])
            print(f"🔥 Hottest category: {hottest}")
            
            for cat, data in results.items():
                print(f"   {cat}: {data['trend']} ({data['avg_interest']:.1f})")
            
            return True
        else:
            print("❌ No market trend data collected")
            return False
            
    except Exception as e:
        print(f"❌ Market trends analysis failed: {e}")
        return False

def main():
    """运行增强版Google Trends测试"""
    print("Google Trends Integration Test (Robust Version)")
    print("="*60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    print("\n🛡️ Enhanced features:")
    print("   - Longer timeouts (15s connect, 45s read)")
    print("   - Automatic retry with backoff")
    print("   - Random delays to avoid rate limiting")
    print("   - Simplified queries for better success rate")
    print()
    
    results = []
    
    # 运行测试
    tests = [
        ("Initialization", test_robust_initialization),
        ("Single Keyword", test_single_keyword_robust),
        ("Product Comparison", test_product_comparison_robust),
        ("Regional Analysis", test_regional_analysis_robust),
        ("Market Trends", test_market_trends_robust)
    ]
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        
        try:
            if test_name == "Initialization":
                result = test_func()[0]  # 只取成功标志
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
        
        # 测试间延迟
        if test_func != tests[-1][1]:  # 不是最后一个测试
            delay = random.uniform(8, 12)
            print(f"\n⏳ Waiting {delay:.1f}s before next test...")
            time.sleep(delay)
    
    # 总结
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} : {status}")
    
    passed = sum(r[1] for r in results)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == 0:
        print("\n❌ All tests failed. Possible issues:")
        print("   - Network connectivity problems")
        print("   - Google Trends service unavailable")
        print("   - IP blocked due to excessive requests")
        print("   - PyTrends compatibility issues")
        print("\n💡 Recommendations:")
        print("   - Check internet connection")
        print("   - Try again later")
        print("   - Use VPN if persistent issues")
        print("   - Consider alternative trend data sources")
    elif passed < total:
        print(f"\n⚠️ {total - passed} tests failed but {passed} succeeded")
        print("💡 PyTrends partially working - can proceed with caution")
    else:
        print("\n🎉 All tests passed!")
        print("✅ Robust PyTrends client is ready for production use")

if __name__ == "__main__":
    main()