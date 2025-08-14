#!/usr/bin/env python
"""
Test MindsDB connection and basic query capabilities
"""

import requests
import json
from typing import Dict, Any, List

class MindsDBClient:
    """Simple MindsDB HTTP API client for testing"""
    
    def __init__(self, host: str = "localhost", port: int = 47334):
        self.base_url = f"http://{host}:{port}"
        self.api_url = f"{self.base_url}/api/sql/query"
        
    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute SQL query via MindsDB HTTP API"""
        try:
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_connection(self) -> bool:
        """Test if MindsDB is accessible"""
        result = self.execute_query("SELECT 1")
        return result.get("success", False)
    
    def list_databases(self) -> List[str]:
        """List available databases"""
        result = self.execute_query("SHOW DATABASES")
        if result["success"]:
            data = result["data"].get("data", [])
            # Filter out system databases
            return [db[0] for db in data if db[0] not in ['information_schema', 'mindsdb', 'files', 'log']]
        return []
    
    def list_tables(self, database: str) -> List[str]:
        """List tables in a database"""
        result = self.execute_query(f"SHOW TABLES FROM {database}")
        if result["success"]:
            data = result["data"].get("data", [])
            return [table[0] for table in data]
        return []
    
    def get_table_schema(self, database: str, table: str) -> Dict:
        """Get table schema information"""
        result = self.execute_query(f"DESCRIBE {database}.{table}")
        if result["success"]:
            columns = result["data"].get("column_names", [])
            data = result["data"].get("data", [])
            return {
                "columns": columns,
                "schema": data
            }
        return {}

def test_mindsdb_connection():
    """Main test function"""
    print("=" * 60)
    print("MindsDB Connection Test")
    print("=" * 60)
    
    client = MindsDBClient()
    
    # Test 1: Basic connection
    print("\n1. Testing connection...")
    if client.test_connection():
        print("✅ Connection successful")
    else:
        print("❌ Connection failed")
        print("Make sure MindsDB is running on localhost:47334")
        return
    
    # Test 2: List databases
    print("\n2. Available databases:")
    databases = client.list_databases()
    for db in databases:
        print(f"   - {db}")
    
    # Test 3: Check for our target databases
    print("\n3. Checking for e-commerce databases:")
    target_dbs = ["htinfo_db", "ext_ref_db"]
    for db in target_dbs:
        if db in databases:
            print(f"   ✅ Found: {db}")
            
            # List tables in this database
            tables = client.list_tables(db)
            print(f"      Tables in {db}:")
            for table in tables:
                print(f"         - {table}")
        else:
            print(f"   ❌ Not found: {db}")
    
    # Test 4: Check for Walmart/Amazon tables
    print("\n4. Looking for product data tables:")
    if "htinfo_db" in databases:
        tables = client.list_tables("htinfo_db")
        
        walmart_tables = [t for t in tables if "walmart" in t.lower()]
        amazon_tables = [t for t in tables if "amazon" in t.lower()]
        
        if walmart_tables:
            print("   Walmart tables found:")
            for table in walmart_tables:
                print(f"      - {table}")
        
        if amazon_tables:
            print("   Amazon tables found:")
            for table in amazon_tables:
                print(f"      - {table}")
        
        # Test 5: Sample query
        if walmart_tables:
            print(f"\n5. Testing sample query on {walmart_tables[0]}:")
            sample_query = f"SELECT * FROM htinfo_db.{walmart_tables[0]} LIMIT 3"
            result = client.execute_query(sample_query)
            
            if result["success"]:
                data = result["data"]
                print(f"   ✅ Query successful")
                print(f"   Columns: {data.get('column_names', [])}")
                print(f"   Rows returned: {len(data.get('data', []))}")
                
                # Display sample data
                if data.get('data'):
                    print("\n   Sample data:")
                    for row in data['data'][:3]:
                        print(f"      {row}")
            else:
                print(f"   ❌ Query failed: {result['error']}")

if __name__ == "__main__":
    test_mindsdb_connection()