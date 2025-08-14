#!/usr/bin/env python
"""
Fixed version of Google Trends test with better error handling
and compatibility fixes for latest PyTrends/urllib3
"""

import pandas as pd
from datetime import datetime, timedelta
import time
import random
import warnings

# Suppress SSL warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def test_pytrends_simple():
    """Test simplified PyTrends usage"""
    print("="*60)
    print("Testing PyTrends (Simplified Version)")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        print("✅ pytrends imported successfully")
        
        # Simple initialization without problematic parameters
        pytrends = TrendReq(hl='en-US', tz=360)
        print("✅ TrendReq initialized (basic mode)")
        
        # Test with a single, simple keyword
        keyword = "iPhone"
        print(f"\n📊 Testing single keyword: '{keyword}'")
        
        # Shorter timeframe to reduce load
        pytrends.build_payload(
            kw_list=[keyword],
            timeframe='today 1-m',  # Just last month
            geo='US'
        )
        
        # Get interest over time
        try:
            data = pytrends.interest_over_time()
            if not data.empty:
                print(f"✅ Data retrieved: {data.shape[0]} data points")
                print(f"   Latest value: {data[keyword].iloc[-1]}")
                print(f"   Average: {data[keyword].mean():.1f}")
                return True
        except Exception as e:
            print(f"⚠️ Interest over time failed: {str(e)[:100]}")
            
        return False
        
    except ImportError:
        print("❌ PyTrends not installed")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_product_comparison():
    """Test comparing multiple products with better error handling"""
    print("\n" + "="*60)
    print("Testing Product Comparison")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        
        # Initialize with minimal params
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Compare popular products
        products = ["AirPods", "Galaxy Buds", "Pixel Buds"]
        print(f"📊 Comparing: {', '.join(products)}")
        
        # Add delay
        time.sleep(2)
        
        try:
            pytrends.build_payload(
                kw_list=products[:2],  # Limit to 2 for better success rate
                timeframe='today 3-m',
                geo='US'
            )
            
            data = pytrends.interest_over_time()
            
            if not data.empty:
                print("✅ Comparison data retrieved")
                
                # Calculate average interest
                for product in products[:2]:
                    if product in data.columns:
                        avg = data[product].mean()
                        latest = data[product].iloc[-1]
                        print(f"   {product}: Avg={avg:.1f}, Latest={latest}")
                
                # Determine winner
                if len(data.columns) >= 2:
                    winner = data[products[:2]].mean().idxmax()
                    print(f"🏆 Most popular: {winner}")
                
                return True
            else:
                print("⚠️ No comparison data returned")
                return False
                
        except Exception as e:
            print(f"⚠️ Comparison failed: {str(e)[:100]}")
            return False
            
    except Exception as e:
        print(f"❌ Product comparison failed: {e}")
        return False

def test_search_volume_index():
    """Test getting search volume index for market analysis"""
    print("\n" + "="*60)
    print("Testing Search Volume Index")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Market analysis keywords
        categories = {
            "Smart Home": ["smart home", "alexa", "google home"],
            "Fitness": ["fitness tracker", "smartwatch", "apple watch"],
            "Gaming": ["ps5", "xbox", "nintendo switch"]
        }
        
        results = {}
        
        for category, keywords in categories.items():
            print(f"\n📈 Analyzing {category}...")
            
            # Use just the first keyword to avoid rate limits
            keyword = keywords[0]
            
            try:
                # Add delay
                time.sleep(random.uniform(3, 5))
                
                pytrends.build_payload(
                    kw_list=[keyword],
                    timeframe='today 3-m',
                    geo='US'
                )
                
                data = pytrends.interest_over_time()
                
                if not data.empty and keyword in data.columns:
                    # Calculate metrics
                    avg_interest = data[keyword].mean()
                    max_interest = data[keyword].max()
                    current = data[keyword].iloc[-1]
                    
                    # Calculate trend
                    first_half = data[keyword][:len(data)//2].mean()
                    second_half = data[keyword][len(data)//2:].mean()
                    trend = "📈 Growing" if second_half > first_half else "📉 Declining"
                    
                    results[category] = {
                        'avg': avg_interest,
                        'max': max_interest,
                        'current': current,
                        'trend': trend
                    }
                    
                    print(f"   Current Index: {current}")
                    print(f"   Trend: {trend}")
                else:
                    print(f"   ⚠️ No data for {keyword}")
                    
            except Exception as e:
                print(f"   ⚠️ Failed: {str(e)[:50]}")
        
        if results:
            print("\n📊 Market Summary:")
            hottest = max(results.keys(), key=lambda k: results[k]['avg'])
            print(f"🔥 Hottest category: {hottest}")
            
            for cat, metrics in results.items():
                print(f"   {cat}: {metrics['trend']} (Index: {metrics['current']})")
            
            return True
        else:
            print("❌ No market data collected")
            return False
            
    except Exception as e:
        print(f"❌ Search volume test failed: {e}")
        return False

def test_seasonal_trends():
    """Test seasonal trend detection"""
    print("\n" + "="*60)
    print("Testing Seasonal Trends")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Seasonal products
        seasonal_items = {
            "Christmas decorations": "Winter/Holiday",
            "swimwear": "Summer",
            "tax software": "Spring",
            "halloween costume": "Fall"
        }
        
        print("📅 Analyzing seasonal patterns...")
        
        current_month = datetime.now().month
        season_data = {}
        
        for item, season in list(seasonal_items.items())[:2]:  # Limit to 2
            try:
                time.sleep(random.uniform(3, 5))
                
                print(f"\n🔍 {item} ({season}):")
                
                pytrends.build_payload(
                    kw_list=[item],
                    timeframe='today 12-m',
                    geo='US'
                )
                
                data = pytrends.interest_over_time()
                
                if not data.empty and item in data.columns:
                    # Find peak month
                    peak_value = data[item].max()
                    peak_date = data[item].idxmax()
                    peak_month = peak_date.month if hasattr(peak_date, 'month') else 0
                    
                    current_value = data[item].iloc[-1]
                    avg_value = data[item].mean()
                    
                    season_data[item] = {
                        'peak_month': peak_month,
                        'peak_value': peak_value,
                        'current': current_value,
                        'average': avg_value,
                        'season': season
                    }
                    
                    print(f"   Peak month: {peak_month}")
                    print(f"   Current vs Peak: {current_value} / {peak_value}")
                    
                    # Seasonal relevance
                    if current_value > avg_value * 1.2:
                        print(f"   🔥 Currently trending!")
                    elif current_value < avg_value * 0.8:
                        print(f"   ❄️ Off-season")
                    else:
                        print(f"   ➡️ Normal levels")
                        
            except Exception as e:
                print(f"   ⚠️ Analysis failed: {str(e)[:50]}")
        
        if season_data:
            print("\n📊 Seasonal Summary:")
            for item, data in season_data.items():
                status = "In Season" if data['current'] > data['average'] else "Off Season"
                print(f"   {item}: {status}")
            return True
        else:
            print("❌ No seasonal data collected")
            return False
            
    except Exception as e:
        print(f"❌ Seasonal trends test failed: {e}")
        return False

def main():
    """Run simplified Google Trends tests"""
    print("Google Trends Integration Test (Fixed Version)")
    print("="*60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    print("\n⚠️ Note: Google Trends API has rate limits and may block requests.")
    print("This test uses delays and simplified queries to improve success rate.\n")
    
    results = []
    
    # Run tests with delays
    tests = [
        ("Simple Query", test_pytrends_simple),
        ("Product Comparison", test_product_comparison),
        ("Search Volume", test_search_volume_index),
        ("Seasonal Trends", test_seasonal_trends)
    ]
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        result = test_func()
        results.append((test_name, result))
        
        # Delay between tests
        if test_func != tests[-1][1]:
            print("\n⏳ Waiting before next test...")
            time.sleep(5)
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} : {status}")
    
    print(f"\nTotal: {sum(r[1] for r in results)}/{len(results)} tests passed")
    
    if sum(r[1] for r in results) == 0:
        print("\n⚠️ All tests failed. Common issues:")
        print("   - Rate limiting by Google")
        print("   - Network/proxy issues")
        print("   - PyTrends compatibility issues")
        print("\n💡 Alternatives to consider:")
        print("   - Use Google Trends website directly")
        print("   - Try SerpAPI's Google Trends API")
        print("   - Use cached/historical trend data")
        print("   - Implement exponential backoff and retry")
    elif sum(r[1] for r in results) < len(results):
        print("\n⚠️ Some tests failed due to API limitations")
        print("💡 Consider using alternative data sources or caching")

if __name__ == "__main__":
    main()