#!/usr/bin/env python
"""
Test LangChain/LangGraph integration with Gemini and Grok
"""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_langchain_imports():
    """Test if LangChain packages are available"""
    print("="*60)
    print("Testing LangChain Package Imports")
    print("="*60)
    
    try:
        from langchain_core.messages import HumanMessage, AIMessage
        from langchain_core.prompts import PromptTemplate
        print("✅ langchain_core imports successful")
    except ImportError as e:
        print(f"❌ langchain_core import failed: {e}")
        return False
    
    try:
        from langgraph.graph import StateGraph, START, END
        from langgraph.graph.state import CompiledStateGraph
        print("✅ langgraph imports successful")
    except ImportError as e:
        print(f"❌ langgraph import failed: {e}")
        print("Install with: pip install langgraph")
        return False
    
    return True

def test_gemini_integration():
    """Test Gemini integration via LangChain"""
    print("\n" + "="*60)
    print("Testing Gemini Integration")
    print("="*60)
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ langchain_google_genai imported")
    except ImportError as e:
        print(f"❌ langchain_google_genai import failed: {e}")
        print("Install with: pip install langchain-google-genai")
        return False
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ No Gemini API key found")
        print("Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Initialize Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        # Test simple query
        response = llm.invoke("What is 2+2? Respond with just the number.")
        print(f"✅ Gemini test successful: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        return False

def test_grok_integration():
    """Test Grok integration via OpenAI-compatible API"""
    print("\n" + "="*60)
    print("Testing Grok Integration")
    print("="*60)
    
    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain_openai imported")
    except ImportError as e:
        print(f"❌ langchain_openai import failed: {e}")
        print("Install with: pip install langchain-openai")
        return False
    
    # Check API key and base URL
    api_key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
    base_url = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
    
    if not api_key:
        print("❌ No Grok API key found")
        print("Set XAI_API_KEY or GROK_API_KEY environment variable")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    print(f"✅ Base URL: {base_url}")
    
    try:
        # Initialize Grok model
        llm = ChatOpenAI(
            model="grok-4",
            api_key=api_key,
            base_url=base_url,
            temperature=0.7
        )
        
        # Test simple query
        response = llm.invoke("What is 3+3? Respond with just the number.")
        print(f"✅ Grok test successful: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Grok test failed: {e}")
        return False

def test_simple_langgraph():
    """Test simple LangGraph workflow"""
    print("\n" + "="*60)
    print("Testing Simple LangGraph Workflow")
    print("="*60)
    
    try:
        from langgraph.graph import StateGraph, START, END
        from typing_extensions import TypedDict
        from langchain_core.messages import HumanMessage
        
        # Define state
        class AnalysisState(TypedDict):
            messages: List[HumanMessage]
            result: str
        
        # Define nodes
        def analyze_node(state: AnalysisState) -> AnalysisState:
            """Simple analysis node"""
            message = state["messages"][-1].content
            result = f"Analyzed: {message}"
            return {"messages": state["messages"], "result": result}
        
        # Build graph
        graph = StateGraph(AnalysisState)
        graph.add_node("analyze", analyze_node)
        graph.add_edge(START, "analyze")
        graph.add_edge("analyze", END)
        
        # Compile and test
        app = graph.compile()
        
        test_input = {
            "messages": [HumanMessage(content="Test product analysis")],
            "result": ""
        }
        
        result = app.invoke(test_input)
        print(f"✅ LangGraph test successful: {result['result']}")
        return True
        
    except Exception as e:
        print(f"❌ LangGraph test failed: {e}")
        return False

def test_product_analysis_prompt():
    """Test product analysis specific prompts"""
    print("\n" + "="*60)
    print("Testing Product Analysis Prompts")
    print("="*60)
    
    # Test with available LLM
    llm = None
    
    # Try Gemini first
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if api_key:
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.7
            )
            print("✅ Using Gemini for prompt test")
    except:
        pass
    
    # Try Grok if Gemini failed
    if not llm:
        try:
            from langchain_openai import ChatOpenAI
            api_key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
            base_url = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
            if api_key:
                llm = ChatOpenAI(
                    model="grok-4",
                    api_key=api_key,
                    base_url=base_url,
                    temperature=0.7
                )
                print("✅ Using Grok for prompt test")
        except:
            pass
    
    if not llm:
        print("❌ No LLM available for prompt testing")
        return False
    
    # Test product analysis prompt
    prompt = """
    Based on the following product data, identify the top 3 market trends:
    
    Products:
    1. "Arizona Wildcats 3-Pack Ornament Set" - $15.99, 4.2 rating
    2. "Original Squishamllow Christmas Ornament 8PK" - $24.99, 4.5 rating  
    3. "Best Choice Products 2-Piece 58in Moose Family" - $89.99, 4.1 rating
    
    Respond with:
    1. Top trend
    2. Second trend  
    3. Third trend
    """
    
    try:
        response = llm.invoke(prompt)
        print("✅ Product analysis prompt successful:")
        print(f"Response: {response.content[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Product analysis prompt failed: {e}")
        return False

def main():
    """Run all LLM tests"""
    print("LangChain/LangGraph LLM Integration Test")
    print("="*60)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_langchain_imports()))
    
    # Test LLM integrations
    results.append(("Gemini", test_gemini_integration()))
    results.append(("Grok", test_grok_integration()))
    
    # Test LangGraph
    results.append(("LangGraph", test_simple_langgraph()))
    
    # Test product analysis
    results.append(("Product Analysis", test_product_analysis_prompt()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} : {status}")
    
    print(f"\nTotal: {sum(r[1] for r in results)}/{len(results)} tests passed")
    
    if not any(r[1] for r in results[1:3]):  # No LLM working
        print("\n⚠️ No LLM integration working. Check:")
        print("   - API keys are set correctly")
        print("   - Required packages are installed")
        print("   - Network connectivity")

if __name__ == "__main__":
    main()