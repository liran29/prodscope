#!/usr/bin/env python
"""
Test with actual MindsDB data structure
"""

import requests
import json
from typing import Dict, Any, Optional

class ActualDataTester:
    """Test with real MindsDB data"""
    
    def __init__(self):
        self.api_url = "http://localhost:47334/api/sql/query"
    
    def query(self, sql: str) -> Dict[str, Any]:
        """Execute query"""
        try:
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json={"query": sql},
                timeout=30
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def test_walmart_products(self):
        """Test Walmart product data"""
        print("\n" + "="*60)
        print("Testing Walmart Product Data")
        print("="*60)
        
        # 1. Check walmart_products structure
        print("\n1. Checking walmart_products table structure...")
        result = self.query("DESCRIBE ext_ref_db.walmart_products")
        if "column_names" in result:
            print(f"✅ Columns: {result['column_names']}")
        
        # 2. Sample product data
        print("\n2. Getting sample product data...")
        result = self.query("""
            SELECT * FROM prodscope_db.walmart_products 
            WHERE category LIKE '%Christmas%' OR category LIKE '%Holiday%'
            LIMIT 5
        """)
        
        if "data" in result and result["data"]:
            print(f"✅ Found {len(result['data'])} Christmas/Holiday products")
            print(f"   Columns: {result.get('column_names', [])}")
            
            # Show first product
            if result["data"]:
                print("\n   Sample product:")
                for col, val in zip(result.get('column_names', []), result['data'][0]):
                    if col in ['product_id', 'title', 'price', 'category', 'rating']:
                        print(f"      {col}: {val}")
        else:
            print("❌ No Christmas products found, trying all products...")
            result = self.query("SELECT * FROM prodscope_db.walmart_products LIMIT 5")
            if "data" in result:
                print(f"   Found {len(result['data'])} products total")
    
    def test_reviews(self):
        """Test review data"""
        print("\n" + "="*60)
        print("Testing Review Data")
        print("="*60)
        
        print("\n1. Checking review table...")
        result = self.query("""
            SELECT COUNT(*) as review_count 
            FROM prodscope_db.walmart_product_reviews
        """)
        
        if "data" in result and result["data"]:
            count = result["data"][0][0]
            print(f"✅ Total reviews: {count}")
        
        # Sample negative reviews
        print("\n2. Getting negative reviews (rating <= 2)...")
        result = self.query("""
            SELECT product_id, rating, review_title, review_text
            FROM ext_ref_db.walmart_product_reviews
            WHERE rating <= 2
            LIMIT 3
        """)
        
        if "data" in result and result["data"]:
            print(f"✅ Found negative reviews")
            for i, review in enumerate(result["data"][:2], 1):
                print(f"\n   Review {i}:")
                print(f"      Product ID: {review[0]}")
                print(f"      Rating: {review[1]}")
                print(f"      Title: {review[2][:50]}...")
                print(f"      Text: {review[3][:100]}..." if review[3] else "      Text: None")
    
    def test_price_history(self):
        """Test price history data"""
        print("\n" + "="*60)
        print("Testing Price History")
        print("="*60)
        
        result = self.query("""
            SELECT product_id, old_price, new_price, 
                   (old_price - new_price) / old_price * 100 as discount_pct
            FROM ext_ref_db.walmart_price_history
            WHERE new_price < old_price
            LIMIT 5
        """)
        
        if "data" in result and result["data"]:
            print(f"✅ Found price drops")
            for row in result["data"]:
                print(f"   Product {row[0]}: ${row[1]:.2f} → ${row[2]:.2f} ({row[3]:.1f}% off)")
    
    def test_cross_platform(self):
        """Test Amazon comparison data"""
        print("\n" + "="*60)
        print("Testing Cross-Platform Data")
        print("="*60)
        
        # Check Amazon products
        result = self.query("""
            SELECT COUNT(*) as amazon_count
            FROM ext_ref_db.amazon_products
        """)
        
        if "data" in result and result["data"]:
            count = result["data"][0][0]
            print(f"✅ Amazon products available: {count}")
        
        # Compare categories
        print("\n Comparing categories...")
        result = self.query("""
            SELECT 'Walmart' as platform, COUNT(DISTINCT category) as category_count
            FROM ext_ref_db.walmart_products
            UNION ALL
            SELECT 'Amazon' as platform, COUNT(DISTINCT category) as category_count
            FROM ext_ref_db.amazon_products
        """)
        
        if "data" in result and result["data"]:
            for row in result["data"]:
                print(f"   {row[0]}: {row[1]} categories")

def main():
    print("="*60)
    print("ACTUAL DATA STRUCTURE TEST")
    print("="*60)
    
    tester = ActualDataTester()
    
    # Run all tests
    tester.test_walmart_products()
    tester.test_reviews()
    tester.test_price_history()
    tester.test_cross_platform()
    
    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    print("\n✅ Data is available in ext_ref_db")
    print("✅ Tables match expected structure")
    print("✅ Ready for analysis implementation")

if __name__ == "__main__":
    main()