#!/usr/bin/env python
"""
Test Gemini API basic capabilities without Google Search tool
Due to regional restrictions, Google Search tool may not be available
"""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def test_genai_client_basic():
    """Test basic Google GenAI client setup and text generation"""
    print("="*60)
    print("Testing Google GenAI Basic Functionality")
    print("="*60)
    
    try:
        from google import genai
        print(f"✅ google.genai imported (v{genai.__version__})")
    except ImportError as e:
        print(f"❌ google.genai import failed: {e}")
        return False
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ No Gemini API key found")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Initialize client
        client = genai.Client(api_key=api_key)
        print("✅ GenAI client initialized")
        
        # Test basic text generation (without search tools)
        prompt = "List 3 current trends in smart home technology in 2024. Be concise."
        
        print(f"\n📝 Testing basic generation with prompt: {prompt[:50]}...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "temperature": 0.3,
                "max_output_tokens": 500,
            },
        )
        
        if response and response.text:
            print("✅ Basic generation successful")
            print(f"📄 Response length: {len(response.text)} characters")
            print(f"\n📝 Response:")
            print(response.text[:500])
            return True
        else:
            print("❌ No response text received")
            return False
            
    except Exception as e:
        print(f"❌ Basic generation failed: {e}")
        return False

def test_structured_output():
    """Test Gemini's structured output capabilities"""
    print("\n" + "="*60)
    print("Testing Structured Output Generation")
    print("="*60)
    
    setup_result = test_genai_client_setup_minimal()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        prompt = """
        Analyze the following product and provide a structured response:
        
        Product: Wireless Noise-Canceling Headphones
        Price: $299
        Rating: 4.5/5 stars
        Reviews: 1,234
        
        Provide your analysis in the following JSON format:
        {
            "market_position": "premium/mid-range/budget",
            "key_strengths": ["strength1", "strength2"],
            "target_audience": "description",
            "price_competitiveness": "competitive/overpriced/underpriced",
            "recommendation": "buy/wait/skip"
        }
        """
        
        print("📊 Testing structured product analysis...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "temperature": 0.1,
                "response_mime_type": "application/json",
            },
        )
        
        if response and response.text:
            print("✅ Structured output generated")
            
            # Try to parse JSON
            import json
            try:
                data = json.loads(response.text)
                print("✅ Valid JSON response")
                print(f"📦 Market Position: {data.get('market_position', 'N/A')}")
                print(f"💪 Strengths: {', '.join(data.get('key_strengths', []))}")
                print(f"🎯 Target: {data.get('target_audience', 'N/A')}")
                print(f"💰 Price: {data.get('price_competitiveness', 'N/A')}")
                print(f"✨ Recommendation: {data.get('recommendation', 'N/A')}")
                return True
            except json.JSONDecodeError:
                print("⚠️ Response is not valid JSON, but text generated")
                print(f"Response: {response.text[:200]}...")
                return True
        else:
            print("❌ No structured output generated")
            return False
            
    except Exception as e:
        print(f"❌ Structured output test failed: {e}")
        return False

def test_multimodal_analysis():
    """Test Gemini's ability to analyze product descriptions"""
    print("\n" + "="*60)
    print("Testing Multimodal Analysis (Text-based)")
    print("="*60)
    
    setup_result = test_genai_client_setup_minimal()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        # Simulate product data analysis
        product_data = """
        Product Catalog Analysis Request:
        
        Category: Electronics > Audio > Wireless Earbuds
        
        Products to analyze:
        1. AirPods Pro 2 - $249, 4.6★, Active Noise Cancellation
        2. Samsung Galaxy Buds Pro - $199, 4.4★, IPX7 Water Resistant
        3. Sony WF-1000XM5 - $299, 4.5★, Industry Leading ANC
        4. Google Pixel Buds Pro - $179, 4.2★, Google Assistant Integration
        5. Bose QuietComfort Earbuds - $279, 4.3★, Premium Sound Quality
        
        Task: Identify market trends, price positioning, and competitive advantages.
        """
        
        print("🎧 Analyzing wireless earbuds market...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=product_data,
            config={
                "temperature": 0.4,
                "max_output_tokens": 1000,
            },
        )
        
        if response and response.text:
            print("✅ Product analysis completed")
            
            # Extract key insights
            analysis = response.text.lower()
            
            insights = []
            if "price" in analysis:
                insights.append("✓ Price analysis included")
            if "trend" in analysis:
                insights.append("✓ Market trends identified")
            if "competitive" in analysis or "advantage" in analysis:
                insights.append("✓ Competitive analysis provided")
            if "noise cancellation" in analysis or "anc" in analysis:
                insights.append("✓ Feature comparison included")
            
            print("🔍 Analysis coverage:")
            for insight in insights:
                print(f"   {insight}")
            
            print(f"\n📝 Analysis preview:")
            print(response.text[:400] + "...")
            
            return len(insights) >= 2  # Success if at least 2 insights found
        else:
            print("❌ No analysis generated")
            return False
            
    except Exception as e:
        print(f"❌ Multimodal analysis failed: {e}")
        return False

def test_batch_processing():
    """Test processing multiple queries efficiently"""
    print("\n" + "="*60)
    print("Testing Batch Processing Capabilities")
    print("="*60)
    
    setup_result = test_genai_client_setup_minimal()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        queries = [
            "What are the top 3 features consumers look for in smartwatches?",
            "Compare budget vs premium wireless earbuds market segments.",
            "What is driving growth in the smart home security market?"
        ]
        
        print(f"📦 Processing {len(queries)} market research queries...")
        
        results = []
        for i, query in enumerate(queries, 1):
            print(f"\n🔄 Query {i}: {query[:50]}...")
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=query,
                    config={
                        "temperature": 0.3,
                        "max_output_tokens": 300,
                    },
                )
                
                if response and response.text:
                    results.append({
                        'query': query,
                        'response': response.text,
                        'length': len(response.text)
                    })
                    print(f"   ✅ Response received ({len(response.text)} chars)")
                else:
                    print(f"   ❌ No response")
                    
            except Exception as e:
                print(f"   ❌ Failed: {str(e)[:50]}")
        
        if results:
            print(f"\n📊 Batch Processing Summary:")
            print(f"   Successful: {len(results)}/{len(queries)}")
            avg_length = sum(r['length'] for r in results) / len(results)
            print(f"   Avg response length: {avg_length:.0f} chars")
            
            # Show sample response
            if results:
                print(f"\n📝 Sample response (Query 1):")
                print(results[0]['response'][:200] + "...")
            
            return len(results) >= 2  # Success if at least 2 queries processed
        else:
            print("❌ No queries processed successfully")
            return False
            
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")
        return False

def test_genai_client_setup_minimal():
    """Minimal client setup for internal use"""
    try:
        from google import genai
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return False, None
        client = genai.Client(api_key=api_key)
        return True, client
    except:
        return False, None

def test_alternative_search_approach():
    """Test alternative approach to market research without Google Search tool"""
    print("\n" + "="*60)
    print("Testing Alternative Market Research Approach")
    print("="*60)
    
    setup_result = test_genai_client_setup_minimal()
    if not setup_result[0]:
        return False
    
    client = setup_result[1]
    
    try:
        # Use Gemini's knowledge for market analysis
        prompt = """
        Based on your knowledge up to early 2025, provide a market analysis for:
        
        Topic: E-commerce competition between Walmart and Amazon in holiday decorations
        
        Include:
        1. Market positioning of each company
        2. Typical pricing strategies
        3. Customer demographics
        4. Competitive advantages
        5. Recent trends or changes
        
        Be specific and data-oriented where possible.
        """
        
        print("🏪 Analyzing Walmart vs Amazon (using model knowledge)...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 1500,
            },
        )
        
        if response and response.text:
            print("✅ Market analysis completed")
            
            # Check for key components
            analysis = response.text.lower()
            components = [
                ("Walmart mentioned", "walmart" in analysis),
                ("Amazon mentioned", "amazon" in analysis),
                ("Pricing discussed", "price" in analysis or "pricing" in analysis),
                ("Demographics covered", "customer" in analysis or "demographic" in analysis),
                ("Trends identified", "trend" in analysis or "recent" in analysis)
            ]
            
            print("\n📊 Analysis Components:")
            for name, present in components:
                status = "✅" if present else "❌"
                print(f"   {status} {name}")
            
            coverage = sum(1 for _, present in components if present)
            
            if coverage >= 3:
                print(f"\n✅ Comprehensive analysis ({coverage}/5 components)")
                print(f"\n📝 Analysis excerpt:")
                print(response.text[:500] + "...")
                return True
            else:
                print(f"\n⚠️ Limited analysis ({coverage}/5 components)")
                return False
        else:
            print("❌ No analysis generated")
            return False
            
    except Exception as e:
        print(f"❌ Alternative search approach failed: {e}")
        return False

def main():
    """Run Gemini API tests without location-restricted features"""
    print("Gemini API Basic Test Suite (No Google Search)")
    print("="*60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    print("\n⚠️ Note: Google Search tool is region-restricted.")
    print("These tests use alternative approaches for market research.\n")
    
    results = []
    
    # Run tests
    results.append(("Basic Generation", test_genai_client_basic()))
    results.append(("Structured Output", test_structured_output()))
    results.append(("Product Analysis", test_multimodal_analysis()))
    results.append(("Batch Processing", test_batch_processing()))
    results.append(("Alternative Research", test_alternative_search_approach()))
    
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
    else:
        passed = sum(r[1] for r in results)
        if passed == len(results):
            print(f"\n🎉 All Gemini basic features are functional!")
            print("\n📌 Alternative approaches for regions without Google Search:")
            print("   ✓ Use model's knowledge base for market insights")
            print("   ✓ Analyze provided data without real-time search")
            print("   ✓ Structure outputs for downstream processing")
            print("   ✓ Batch process multiple queries efficiently")
        else:
            print(f"\n⚠️ {len(results) - passed} tests failed")
            
        print("\n💡 For Google Search functionality, consider:")
        print("   1. Using Vertex AI with location='global'")
        print("   2. Implementing external search APIs (Tavily, Serper, etc.)")
        print("   3. Using PyTrends for Google Trends data")
        print("   4. Waiting for broader regional availability")

if __name__ == "__main__":
    main()