#!/usr/bin/env python
"""
Test LLM integration for generating insights from data
"""

import os
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Test with different LLM providers
# Uncomment the one you want to test

# Option 1: OpenAI
# from openai import OpenAI

# Option 2: Anthropic Claude
# from anthropic import Anthropic

# Option 3: Local LLM via HTTP endpoint
import requests

@dataclass
class InsightGenerator:
    """Test LLM-based insight generation"""
    
    def __init__(self, provider: str = "http", api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        
        if provider == "openai":
            # self.client = OpenAI(api_key=self.api_key)
            pass
        elif provider == "anthropic":
            # self.client = Anthropic(api_key=self.api_key)
            pass
        elif provider == "http":
            self.base_url = os.getenv("LLM_BASE_URL", "http://localhost:8000")
    
    def generate_insight(self, data: Dict, analysis_type: str) -> str:
        """Generate insights from data using LLM"""
        
        prompts = {
            "trend_analysis": """
            Based on the following product data, identify key market trends:
            
            Data: {data}
            
            Please provide:
            1. Top 3 trending features
            2. Price sensitivity analysis
            3. Seasonal patterns if any
            
            Format your response as structured insights.
            """,
            
            "pain_point_analysis": """
            Analyze the following customer reviews to identify main pain points:
            
            Reviews: {data}
            
            Please identify:
            1. Top 5 customer complaints
            2. Root causes of dissatisfaction
            3. Product improvement opportunities
            
            Be specific and actionable.
            """,
            
            "opportunity_identification": """
            Based on market data and gaps analysis:
            
            Data: {data}
            
            Suggest:
            1. Underserved market segments
            2. Product innovation opportunities
            3. Competitive differentiation strategies
            
            Focus on actionable recommendations.
            """,
            
            "product_recommendation": """
            Based on all analysis data:
            
            Market Trends: {trends}
            Pain Points: {pain_points}
            Opportunities: {opportunities}
            
            Generate 3 specific product recommendations with:
            1. Product concept description
            2. Target market
            3. Key features
            4. Unique selling points
            5. Expected challenges
            
            Make recommendations specific and actionable.
            """
        }
        
        prompt = prompts.get(analysis_type, "").format(data=json.dumps(data, indent=2))
        
        if self.provider == "http":
            return self._call_http_llm(prompt)
        elif self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            return "LLM provider not configured"
    
    def _call_http_llm(self, prompt: str) -> str:
        """Call LLM via HTTP endpoint"""
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "messages": [
                        {"role": "system", "content": "You are a product analysis expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
            else:
                return f"HTTP Error: {response.status_code}"
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        # Implementation for OpenAI
        return "OpenAI integration not implemented in test"
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API"""
        # Implementation for Claude
        return "Anthropic integration not implemented in test"

def test_llm_insights():
    """Test LLM insight generation"""
    print("=" * 60)
    print("LLM Insight Generation Test")
    print("=" * 60)
    
    # Initialize generator
    generator = InsightGenerator(provider="http")
    
    # Test 1: Trend Analysis
    print("\n1. Testing Trend Analysis...")
    sample_trend_data = {
        "popular_features": ["LED lights", "foldable", "remote control"],
        "price_range": {"min": 15.99, "max": 199.99, "average": 45.50},
        "top_categories": ["Indoor decorations", "Outdoor lights", "Tree ornaments"]
    }
    
    trend_insight = generator.generate_insight(sample_trend_data, "trend_analysis")
    print(f"Generated insight:\n{trend_insight[:200]}...")
    
    # Test 2: Pain Point Analysis
    print("\n2. Testing Pain Point Analysis...")
    sample_reviews = {
        "negative_reviews": [
            "The glass ornaments broke during shipping",
            "Installation was too complicated",
            "Lights stopped working after 2 weeks",
            "Much smaller than expected"
        ],
        "common_complaints": ["fragile", "difficult setup", "poor quality"]
    }
    
    pain_insight = generator.generate_insight(sample_reviews, "pain_point_analysis")
    print(f"Generated insight:\n{pain_insight[:200]}...")
    
    # Test 3: Product Recommendation
    print("\n3. Testing Product Recommendation Generation...")
    combined_data = {
        "trends": sample_trend_data,
        "pain_points": sample_reviews,
        "opportunities": {
            "gaps": ["customizable ornaments", "smart home integration"],
            "emerging_needs": ["eco-friendly materials", "energy efficiency"]
        }
    }
    
    recommendation = generator.generate_insight(
        combined_data, 
        "product_recommendation"
    )
    print(f"Generated recommendation:\n{recommendation[:300]}...")
    
    print("\n" + "="*60)
    print("LLM Integration Summary")
    print("="*60)
    print("\n✅ Test completed")
    print("⚠️ Note: For production, you'll need:")
    print("   - Proper API keys configured")
    print("   - Error handling and retries")
    print("   - Response parsing and validation")
    print("   - Prompt optimization")
    print("   - Cost management (token limits)")

if __name__ == "__main__":
    test_llm_insights()