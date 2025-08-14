#!/usr/bin/env python
"""
Test Google Trends integration using PyTrends
"""

import pandas as pd
from datetime import datetime, timedelta
import time
import random

def test_pytrends_installation():
    """Test if PyTrends is available"""
    print("="*60)
    print("Testing PyTrends Installation")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        print("✅ pytrends imported successfully")
        return True
    except ImportError as e:
        print(f"❌ pytrends import failed: {e}")
        print("Install with: pip install pytrends")
        return False

def test_basic_trends_query():
    """Test basic Google Trends query"""
    print("\n" + "="*60)
    print("Testing Basic Trends Query")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        
        # Initialize with compatible parameters
        pytrends = TrendReq(
            hl='en-US',  # language
            tz=360,      # timezone offset
            timeout=(10, 25),  # timeout settings
            # Remove incompatible retry parameters for newer urllib3
            requests_args={'verify': False}  # disable SSL verification if needed
        )
        
        print("✅ TrendReq initialized")
        
        # Test with product-related keywords
        keywords = ["Christmas ornaments", "holiday decorations"]
        print(f"📊 Testing keywords: {keywords}")
        
        # Add delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        # Build payload with timeframe
        pytrends.build_payload(
            kw_list=keywords,
            cat=0,  # all categories
            timeframe='today 12-m',  # last 12 months
            geo='US',  # United States
            gprop=''  # web search
        )
        
        print("✅ Payload built successfully")
        
        # Get interest over time
        interest_over_time = pytrends.interest_over_time()
        
        if not interest_over_time.empty:
            print(f"✅ Interest over time data retrieved: {interest_over_time.shape}")
            print(f"📈 Data period: {interest_over_time.index[0]} to {interest_over_time.index[-1]}")
            
            # Show sample data
            print("\n📊 Sample data (last 5 weeks):")
            print(interest_over_time.tail())
            
            return True
        else:
            print("❌ No data returned")
            return False
            
    except Exception as e:
        print(f"❌ Basic trends query failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

def test_regional_interest():
    """Test regional interest data"""
    print("\n" + "="*60)
    print("Testing Regional Interest")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        
        pytrends = TrendReq(hl='en-US', tz=360, requests_args={'verify': False})
        
        # Add delay
        time.sleep(random.uniform(2, 4))
        
        # Build payload for a single keyword
        keyword = "Christmas gifts"
        pytrends.build_payload(
            kw_list=[keyword],
            timeframe='today 3-m',
            geo='US'
        )
        
        print(f"📍 Testing regional interest for: {keyword}")
        
        # Get interest by region
        regional_interest = pytrends.interest_by_region(
            resolution='REGION',  # state level
            inc_low_vol=True,
            inc_geo_code=False
        )
        
        if not regional_interest.empty:
            print(f"✅ Regional interest data retrieved: {regional_interest.shape}")
            
            # Show top 10 states
            top_states = regional_interest.sort_values(keyword, ascending=False).head(10)
            print(f"\n🗺️ Top 10 states for '{keyword}':")
            for state, value in top_states.iterrows():
                print(f"   {state}: {value[keyword]}")
            
            return True
        else:
            print("❌ No regional data returned")
            return False
            
    except Exception as e:
        print(f"❌ Regional interest test failed: {e}")
        return False

def test_related_queries():
    """Test related queries and topics"""
    print("\n" + "="*60)
    print("Testing Related Queries")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        
        pytrends = TrendReq(hl='en-US', tz=360, requests_args={'verify': False})
        
        # Add delay
        time.sleep(random.uniform(2, 4))
        
        # Build payload
        keyword = "smart home devices"
        pytrends.build_payload(
            kw_list=[keyword],
            timeframe='today 6-m',
            geo='US'
        )
        
        print(f"🔍 Testing related queries for: {keyword}")
        
        # Get related queries
        related_queries = pytrends.related_queries()
        
        if keyword in related_queries and related_queries[keyword]:
            top_queries = related_queries[keyword].get('top')
            rising_queries = related_queries[keyword].get('rising')
            
            print("✅ Related queries data retrieved")
            
            if top_queries is not None and not top_queries.empty:
                print(f"\n🔝 Top related queries:")
                for idx, row in top_queries.head(10).iterrows():
                    print(f"   {row['query']} (value: {row['value']})")
            
            if rising_queries is not None and not rising_queries.empty:
                print(f"\n📈 Rising related queries:")
                for idx, row in rising_queries.head(5).iterrows():
                    print(f"   {row['query']} (value: {row['value']})")
            
            return True
        else:
            print("❌ No related queries data returned")
            return False
            
    except Exception as e:
        print(f"❌ Related queries test failed: {e}")
        return False

def test_trending_searches():
    """Test trending searches"""
    print("\n" + "="*60)
    print("Testing Trending Searches")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        
        pytrends = TrendReq(hl='en-US', tz=360, requests_args={'verify': False})
        
        # Add delay
        time.sleep(random.uniform(2, 4))
        
        print("🔥 Testing trending searches for US")
        
        # Get trending searches (daily)
        trending_searches = pytrends.trending_searches(pn='united_states')
        
        if not trending_searches.empty:
            print(f"✅ Trending searches retrieved: {trending_searches.shape[0]} trends")
            
            print("\n🔥 Current trending searches:")
            for idx, trend in enumerate(trending_searches[0].head(10), 1):
                print(f"   {idx}. {trend}")
            
            return True
        else:
            print("❌ No trending searches data returned")
            return False
            
    except Exception as e:
        print(f"❌ Trending searches test failed: {e}")
        return False

def test_product_analysis_use_case():
    """Test specific product analysis use case"""
    print("\n" + "="*60)
    print("Testing Product Analysis Use Case")
    print("="*60)
    
    try:
        from pytrends.request import TrendReq
        
        pytrends = TrendReq(hl='en-US', tz=360, requests_args={'verify': False})
        
        # Add delay
        time.sleep(random.uniform(2, 4))
        
        # Analyze Walmart vs Amazon product categories
        product_keywords = ["wireless earbuds", "smart watch", "air fryer"]
        
        print(f"🛍️ Analyzing product trends: {product_keywords}")
        
        results = {}
        
        for keyword in product_keywords:
            try:
                # Add small delay between requests
                time.sleep(random.uniform(1, 2))
                
                pytrends.build_payload(
                    kw_list=[keyword],
                    timeframe='today 12-m',
                    geo='US'
                )
                
                # Get interest over time
                interest_data = pytrends.interest_over_time()
                
                if not interest_data.empty:
                    # Calculate trend metrics
                    avg_interest = interest_data[keyword].mean()
                    max_interest = interest_data[keyword].max()
                    latest_interest = interest_data[keyword].iloc[-1]
                    
                    # Calculate trend direction (last 4 weeks vs previous 4 weeks)
                    recent_avg = interest_data[keyword].tail(4).mean()
                    previous_avg = interest_data[keyword].tail(8).head(4).mean()
                    trend_direction = "📈 Rising" if recent_avg > previous_avg else "📉 Declining"
                    
                    results[keyword] = {
                        'avg_interest': avg_interest,
                        'max_interest': max_interest,
                        'latest_interest': latest_interest,
                        'trend_direction': trend_direction
                    }
                    
                    print(f"\n📊 {keyword}:")
                    print(f"   Average interest: {avg_interest:.1f}")
                    print(f"   Peak interest: {max_interest}")
                    print(f"   Current interest: {latest_interest}")
                    print(f"   Trend: {trend_direction}")
                
            except Exception as e:
                print(f"   ❌ Failed to analyze {keyword}: {e}")
        
        if results:
            # Find top trending product
            top_product = max(results.keys(), key=lambda k: results[k]['avg_interest'])
            print(f"\n🏆 Top trending product: {top_product}")
            print(f"   Average interest score: {results[top_product]['avg_interest']:.1f}")
            
            return True
        else:
            print("❌ No product analysis results")
            return False
            
    except Exception as e:
        print(f"❌ Product analysis test failed: {e}")
        return False

def main():
    """Run all Google Trends tests"""
    print("Google Trends Integration Test")
    print("="*60)
    
    results = []
    
    # Test installation
    results.append(("Installation", test_pytrends_installation()))
    
    # Only run other tests if installation succeeded
    if results[0][1]:
        print("\n⚠️ Adding delays between requests to avoid rate limiting...")
        
        # Test basic functionality
        results.append(("Basic Query", test_basic_trends_query()))
        results.append(("Regional Interest", test_regional_interest()))
        results.append(("Related Queries", test_related_queries()))
        results.append(("Trending Searches", test_trending_searches()))
        results.append(("Product Analysis", test_product_analysis_use_case()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} : {status}")
    
    print(f"\nTotal: {sum(r[1] for r in results)}/{len(results)} tests passed")
    
    if not results[0][1]:
        print("\n💡 Install PyTrends with: pip install pytrends")
    elif len(results) > 1 and not any(r[1] for r in results[1:]):
        print("\n⚠️ PyTrends tests failed. Common issues:")
        print("   - Rate limiting (429 errors) - add delays between requests")
        print("   - Network connectivity issues")
        print("   - Google Trends service changes")
        print("   - Consider using proxies or VPN if persistent issues")

if __name__ == "__main__":
    main()