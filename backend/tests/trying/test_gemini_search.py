#!/usr/bin/env python
"""
Test Gemini native Google Search API capabilities for product analysis
Based on findings from gemini-fullstack-langgraph-quickstart project
"""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def test_genai_client_setup():
    """Test Google GenAI client setup"""
    print("="*60)
    print("Testing Google GenAI Client Setup")
    print("="*60)
    
    try:
        from google import genai
        print("✅ google.genai imported successfully")
    except ImportError as e:
        print(f"❌ google.genai import failed: {e}")
        print("Install with: pip install google-genai")
        return False
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ No Gemini API key found")
        print("Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Initialize client
        client = genai.Client(api_key=api_key)
        print("✅ GenAI client initialized successfully")
        return True, client
    except Exception as e:
        print(f"❌ GenAI client initialization failed: {e}")
        return False, None

def test_native_search_capability():
    """Test Gemini's native Google Search capability"""
    print("\n" + "="*60)
    print("Testing Gemini Native Search Capability")
    print("="*60)
    
    setup_result = test_genai_client_setup()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        # Test basic search functionality
        prompt = """Search for recent trends in smart home devices market 2024. 
        Provide a brief summary of the current market trends and key findings."""
        
        print(f"🔍 Testing search with prompt: {prompt[:50]}...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "tools": [{"google_search": {}}],  # Native search tool
                "temperature": 0.3,
            },
        )
        
        if response and response.text:
            print("✅ Native search successful")
            print(f"📄 Response length: {len(response.text)} characters")
            print(f"📝 Response preview: {response.text[:200]}...")
            
            # Check for grounding metadata (sources)
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                    chunks = candidate.grounding_metadata.grounding_chunks
                    print(f"🔗 Found {len(chunks)} source citations")
                    
                    # Show first 3 sources
                    for i, chunk in enumerate(chunks[:3]):
                        if hasattr(chunk, 'web') and chunk.web:
                            print(f"   Source {i+1}: {chunk.web.title[:50]}... - {chunk.web.uri}")
                else:
                    print("⚠️ No grounding metadata found")
            
            return True
        else:
            print("❌ No response text received")
            return False
            
    except Exception as e:
        print(f"❌ Native search test failed: {e}")
        return False

def test_product_trend_analysis():
    """Test product-specific trend analysis using Gemini search"""
    print("\n" + "="*60)
    print("Testing Product Trend Analysis")
    print("="*60)
    
    setup_result = test_genai_client_setup()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        # Analyze specific product categories
        product_categories = [
            "wireless earbuds",
            "smart watches", 
            "air fryers"
        ]
        
        results = {}
        
        for category in product_categories:
            print(f"\n📊 Analyzing trends for: {category}")
            
            prompt = f"""Search for current market trends and consumer preferences for {category} in 2024. 
            Focus on:
            1. Popular brands and models
            2. Price trends
            3. Key features consumers are looking for
            4. Market growth or decline
            
            Provide a concise analysis with specific data points when available."""
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                    config={
                        "tools": [{"google_search": {}}],
                        "temperature": 0.2,
                    },
                )
                
                if response and response.text:
                    results[category] = {
                        'analysis': response.text[:500] + "..." if len(response.text) > 500 else response.text,
                        'sources_count': 0
                    }
                    
                    # Count sources
                    if (hasattr(response, 'candidates') and response.candidates and 
                        hasattr(response.candidates[0], 'grounding_metadata') and 
                        response.candidates[0].grounding_metadata):
                        sources_count = len(response.candidates[0].grounding_metadata.grounding_chunks)
                        results[category]['sources_count'] = sources_count
                    
                    print(f"✅ Analysis completed ({results[category]['sources_count']} sources)")
                    print(f"📝 Preview: {results[category]['analysis'][:100]}...")
                else:
                    print(f"❌ No response for {category}")
                    
            except Exception as e:
                print(f"❌ Analysis failed for {category}: {e}")
        
        # Summary
        if results:
            print(f"\n📈 Product Trend Analysis Summary:")
            print(f"   Categories analyzed: {len(results)}")
            total_sources = sum(r['sources_count'] for r in results.values())
            print(f"   Total sources referenced: {total_sources}")
            
            # Find category with most sources
            if total_sources > 0:
                top_category = max(results.keys(), key=lambda k: results[k]['sources_count'])
                print(f"   Most researched category: {top_category} ({results[top_category]['sources_count']} sources)")
            
            return True
        else:
            print("❌ No successful product analyses")
            return False
            
    except Exception as e:
        print(f"❌ Product trend analysis failed: {e}")
        return False

def test_competitive_analysis():
    """Test competitive analysis using Gemini search"""
    print("\n" + "="*60)
    print("Testing Competitive Analysis")
    print("="*60)
    
    setup_result = test_genai_client_setup()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        prompt = """Compare Walmart vs Amazon product offerings and pricing strategies for holiday decorations in 2024.
        
        Search for information about:
        1. Product variety and availability
        2. Pricing comparison
        3. Customer satisfaction and reviews
        4. Delivery and service differences
        5. Market positioning
        
        Provide a balanced comparative analysis with specific examples."""
        
        print("🏪 Analyzing Walmart vs Amazon competitive landscape...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "tools": [{"google_search": {}}],
                "temperature": 0.1,  # Lower temperature for factual analysis
            },
        )
        
        if response and response.text:
            print("✅ Competitive analysis completed")
            print(f"📄 Analysis length: {len(response.text)} characters")
            
            # Extract key insights
            analysis = response.text
            insights = []
            
            # Simple keyword detection for insights
            if "walmart" in analysis.lower() and "amazon" in analysis.lower():
                insights.append("✓ Covers both Walmart and Amazon")
            if "price" in analysis.lower() or "pricing" in analysis.lower():
                insights.append("✓ Includes pricing analysis")
            if "customer" in analysis.lower() or "review" in analysis.lower():
                insights.append("✓ Mentions customer satisfaction")
            if "delivery" in analysis.lower() or "shipping" in analysis.lower():
                insights.append("✓ Covers delivery/shipping")
            
            print("🔍 Analysis coverage:")
            for insight in insights:
                print(f"   {insight}")
            
            # Show sources
            if (hasattr(response, 'candidates') and response.candidates and 
                hasattr(response.candidates[0], 'grounding_metadata') and 
                response.candidates[0].grounding_metadata):
                sources = response.candidates[0].grounding_metadata.grounding_chunks
                print(f"🔗 Sources used: {len(sources)}")
                
                # Show sample sources
                for i, chunk in enumerate(sources[:3]):
                    if hasattr(chunk, 'web') and chunk.web:
                        print(f"   {i+1}. {chunk.web.title[:60]}...")
            
            print(f"\n📝 Analysis preview:")
            print(f"{analysis[:300]}...")
            
            return True
        else:
            print("❌ No competitive analysis response")
            return False
            
    except Exception as e:
        print(f"❌ Competitive analysis failed: {e}")
        return False

def test_market_opportunity_identification():
    """Test market opportunity identification using search"""
    print("\n" + "="*60)
    print("Testing Market Opportunity Identification")
    print("="*60)
    
    setup_result = test_genai_client_setup()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        prompt = """Search for emerging market opportunities in consumer electronics for 2025.
        
        Focus on:
        1. Underserved market segments
        2. Emerging technologies with commercial potential
        3. Gap analysis between consumer needs and current offerings
        4. Trending product categories with growth potential
        5. Regional market opportunities
        
        Identify specific opportunities with supporting market data."""
        
        print("🚀 Identifying market opportunities...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "tools": [{"google_search": {}}],
                "temperature": 0.4,  # Slightly higher for creative insights
            },
        )
        
        if response and response.text:
            print("✅ Market opportunity analysis completed")
            
            analysis = response.text
            
            # Extract opportunities mentioned
            opportunities = []
            keywords = ["opportunity", "gap", "underserved", "emerging", "growth", "potential"]
            
            sentences = analysis.split('.')
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in keywords):
                    opportunities.append(sentence.strip())
            
            print(f"🎯 Identified {len(opportunities)} potential opportunities")
            
            # Show top opportunities
            for i, opp in enumerate(opportunities[:3], 1):
                if len(opp) > 20:  # Filter out very short sentences
                    print(f"   {i}. {opp[:100]}...")
            
            # Check for data-driven insights
            data_indicators = ["$", "%", "billion", "million", "growth", "increase", "market size"]
            has_data = any(indicator in analysis.lower() for indicator in data_indicators)
            
            if has_data:
                print("✅ Analysis includes quantitative data")
            else:
                print("⚠️ Analysis is primarily qualitative")
            
            return True
        else:
            print("❌ No opportunity analysis response")
            return False
            
    except Exception as e:
        print(f"❌ Market opportunity analysis failed: {e}")
        return False

def main():
    """Run all Gemini search tests"""
    print("Gemini Native Search API Test Suite")
    print("="*60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = []
    
    # Test basic setup
    setup_result = test_genai_client_setup()
    results.append(("Client Setup", setup_result[0] if isinstance(setup_result, tuple) else setup_result))
    
    # Only run other tests if setup succeeded
    if results[0][1]:
        results.append(("Native Search", test_native_search_capability()))
        results.append(("Product Trends", test_product_trend_analysis()))
        results.append(("Competitive Analysis", test_competitive_analysis()))
        results.append(("Market Opportunities", test_market_opportunity_identification()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:25} : {status}")
    
    print(f"\nTotal: {sum(r[1] for r in results)}/{len(results)} tests passed")
    
    if not results[0][1]:
        print("\n💡 Setup Requirements:")
        print("   - pip install google-genai")
        print("   - Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
    elif len(results) > 1 and not any(r[1] for r in results[1:]):
        print("\n⚠️ Search tests failed. Common issues:")
        print("   - API quota exceeded")
        print("   - Network connectivity issues")
        print("   - Invalid API key permissions")
        print("   - Model availability (ensure gemini-2.0-flash is accessible)")
    else:
        print(f"\n🎉 Gemini native search is functional!")
        print("   ✓ Can perform real-time web searches")
        print("   ✓ Provides source citations and grounding metadata")
        print("   ✓ Suitable for product trend analysis")
        print("   ✓ Enables competitive and market research")

if __name__ == "__main__":
    main()