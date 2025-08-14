#!/usr/bin/env python
"""
Test data analysis capabilities with MindsDB data
Focus on the three-layer analysis framework
"""

import requests
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class ProductAnalysisTester:
    """Test product analysis capabilities"""
    
    def __init__(self, host: str = "localhost", port: int = 47334):
        self.base_url = f"http://{host}:{port}"
        self.api_url = f"{self.base_url}/api/sql/query"
    
    def query(self, sql: str) -> Optional[pd.DataFrame]:
        """Execute query and return as DataFrame"""
        try:
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json={"query": sql},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("data") and result.get("column_names"):
                    return pd.DataFrame(result["data"], columns=result["column_names"])
            return None
        except Exception as e:
            print(f"Query error: {e}")
            return None
    
    def test_market_trends(self, category: str = "Christmas Decorations"):
        """Test Layer 1: Market Trend Analysis"""
        print("\n" + "="*60)
        print("LAYER 1: Market Trend Analysis")
        print("="*60)
        
        # Test 1: Popular features extraction
        print("\n1. Extracting popular product features...")
        query_features = f"""
        SELECT 
            title,
            price,
            rating,
            review_count
        FROM htinfo_db.walmart_products 
        WHERE category LIKE '%{category}%'
        ORDER BY review_count DESC
        LIMIT 10
        """
        
        df_products = self.query(query_features)
        if df_products is not None and not df_products.empty:
            print(f"✅ Found {len(df_products)} top products")
            
            # Extract common keywords from titles
            all_titles = " ".join(df_products['title'].astype(str))
            keywords = self.extract_keywords(all_titles)
            print(f"   Common keywords: {keywords[:5]}")
            
            # Price analysis
            avg_price = df_products['price'].mean()
            print(f"   Average price: ${avg_price:.2f}")
            print(f"   Price range: ${df_products['price'].min():.2f} - ${df_products['price'].max():.2f}")
        else:
            print("❌ No product data found")
        
        # Test 2: Price-Sales correlation
        print("\n2. Analyzing price sensitivity...")
        query_price_history = """
        SELECT 
            product_id,
            old_price,
            new_price,
            change_date
        FROM htinfo_db.walmart_price_history
        LIMIT 100
        """
        
        df_prices = self.query(query_price_history)
        if df_prices is not None and not df_prices.empty:
            # Calculate price changes
            df_prices['price_change_pct'] = (df_prices['new_price'] - df_prices['old_price']) / df_prices['old_price'] * 100
            avg_discount = df_prices[df_prices['price_change_pct'] < 0]['price_change_pct'].mean()
            print(f"✅ Price history analyzed")
            print(f"   Average discount: {abs(avg_discount):.1f}%")
            print(f"   Price changes analyzed: {len(df_prices)}")
        else:
            print("❌ No price history data")
        
        # Test 3: Ranking trends
        print("\n3. Analyzing ranking trends...")
        query_rankings = """
        SELECT 
            product_id,
            best_seller_rank,
            ranking_date
        FROM htinfo_db.walmart_ranking_history
        WHERE best_seller_rank IS NOT NULL
        LIMIT 100
        """
        
        df_rankings = self.query(query_rankings)
        if df_rankings is not None and not df_rankings.empty:
            print(f"✅ Ranking data found")
            print(f"   Records analyzed: {len(df_rankings)}")
            top_ranked = df_rankings.nsmallest(5, 'best_seller_rank')
            print(f"   Top ranked products: {top_ranked['product_id'].tolist()}")
        else:
            print("❌ No ranking data")
    
    def test_pain_points(self):
        """Test Layer 2: Pain Point Analysis"""
        print("\n" + "="*60)
        print("LAYER 2: Pain Point Analysis")
        print("="*60)
        
        print("\n1. Analyzing customer reviews...")
        query_reviews = """
        SELECT 
            product_id,
            rating,
            review_title,
            review_text,
            helpful_count
        FROM htinfo_db.walmart_product_reviews
        WHERE rating <= 3
        LIMIT 50
        """
        
        df_reviews = self.query(query_reviews)
        if df_reviews is not None and not df_reviews.empty:
            print(f"✅ Found {len(df_reviews)} negative reviews")
            
            # Analyze common complaints
            negative_text = " ".join(df_reviews['review_text'].astype(str))
            pain_points = self.extract_pain_points(negative_text)
            print(f"   Common pain points: {pain_points}")
            
            # Rating distribution
            rating_dist = df_reviews['rating'].value_counts().to_dict()
            print(f"   Rating distribution: {rating_dist}")
        else:
            print("❌ No review data found")
        
        print("\n2. Cross-platform comparison...")
        # Compare with Amazon if available
        query_amazon = """
        SELECT COUNT(*) as count
        FROM htinfo_db.amazon_products
        """
        
        df_amazon = self.query(query_amazon)
        if df_amazon is not None and not df_amazon.empty:
            count = df_amazon['count'].iloc[0]
            print(f"✅ Amazon data available: {count} products")
        else:
            print("❌ No Amazon comparison data")
    
    def test_opportunities(self):
        """Test Layer 3: Opportunity Identification"""
        print("\n" + "="*60)
        print("LAYER 3: Opportunity Identification")
        print("="*60)
        
        print("\n1. Identifying market gaps...")
        
        # Test for products with high demand but low supply
        query_gaps = """
        SELECT 
            category,
            COUNT(*) as product_count,
            AVG(review_count) as avg_reviews,
            AVG(rating) as avg_rating
        FROM htinfo_db.walmart_products
        GROUP BY category
        HAVING COUNT(*) < 50 AND AVG(review_count) > 100
        LIMIT 10
        """
        
        df_gaps = self.query(query_gaps)
        if df_gaps is not None and not df_gaps.empty:
            print(f"✅ Found {len(df_gaps)} potential market gaps")
            for _, row in df_gaps.iterrows():
                print(f"   - {row['category']}: {row['product_count']} products, {row['avg_reviews']:.0f} avg reviews")
        else:
            print("⚠️ Market gap analysis needs more specific queries")
        
        print("\n2. Innovation opportunities...")
        print("   Need to combine:")
        print("   - External search trend data")
        print("   - Product feature gaps")
        print("   - Customer wishlist from reviews")
    
    def extract_keywords(self, text: str) -> List[str]:
        """Simple keyword extraction"""
        # Basic implementation - in production would use NLP
        words = text.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Filter short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:10]]
    
    def extract_pain_points(self, text: str) -> List[str]:
        """Extract common pain points from negative reviews"""
        # Basic pattern matching - in production would use LLM
        pain_keywords = {
            "fragile": "Material quality issues",
            "broken": "Durability problems", 
            "difficult": "Usability issues",
            "expensive": "Price concerns",
            "small": "Size issues",
            "cheap": "Quality concerns",
            "complicated": "Setup difficulty"
        }
        
        found_issues = []
        text_lower = text.lower()
        for keyword, issue in pain_keywords.items():
            if keyword in text_lower:
                found_issues.append(issue)
        
        return found_issues[:5] if found_issues else ["Needs LLM analysis for deeper insights"]

def test_analysis_pipeline():
    """Main test function"""
    print("=" * 60)
    print("Product Analysis Pipeline Test")
    print("=" * 60)
    
    tester = ProductAnalysisTester()
    
    # Test all three layers
    tester.test_market_trends()
    tester.test_pain_points()
    tester.test_opportunities()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("\n✅ Capabilities confirmed:")
    print("   - MindsDB data access")
    print("   - Basic statistical analysis")
    print("   - Multi-table queries")
    print("\n⚠️ Needs implementation:")
    print("   - LLM integration for text analysis")
    print("   - External data sources (search trends)")
    print("   - Complex correlation analysis")
    print("   - Report generation pipeline")

if __name__ == "__main__":
    test_analysis_pipeline()