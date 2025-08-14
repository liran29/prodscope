#!/usr/bin/env python
"""
Test the multi-LLM configuration system
"""

import os
import sys
import yaml
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

def test_config_files():
    """Test if configuration files are properly structured"""
    print("="*60)
    print("Testing Configuration Files")
    print("="*60)
    
    # Test LLM config file
    llm_config_path = Path("config/llm_config.yaml")
    if llm_config_path.exists():
        try:
            with open(llm_config_path, 'r') as f:
                llm_config = yaml.safe_load(f)
            print("✅ LLM config file loaded successfully")
            
            # Validate structure
            if "providers" in llm_config:
                providers = llm_config["providers"]
                print(f"   Found {len(providers)} providers: {list(providers.keys())}")
                
                for provider, config in providers.items():
                    models = config.get("models", {})
                    print(f"   {provider}: {len(models)} models")
            else:
                print("❌ No 'providers' section in LLM config")
                
        except Exception as e:
            print(f"❌ Error loading LLM config: {e}")
    else:
        print("❌ LLM config file not found")
    
    # Test task assignments file
    task_config_path = Path("config/task_assignments.yaml")
    if task_config_path.exists():
        try:
            with open(task_config_path, 'r') as f:
                task_config = yaml.safe_load(f)
            print("✅ Task assignments file loaded successfully")
            
            # Check environments
            environments = list(task_config.keys())
            print(f"   Found environments: {environments}")
            
            # Check production tasks
            if "production" in task_config:
                prod_tasks = list(task_config["production"].keys())
                print(f"   Production tasks: {len(prod_tasks)}")
            
        except Exception as e:
            print(f"❌ Error loading task assignments: {e}")
    else:
        print("❌ Task assignments file not found")

def test_llm_manager_import():
    """Test if LLM manager can be imported"""
    print("\n" + "="*60)
    print("Testing LLM Manager Import")
    print("="*60)
    
    try:
        from llm.llm_manager import LLMManager, TaskType, get_llm_manager
        print("✅ LLM manager imports successful")
        
        # Test enum
        tasks = list(TaskType)
        print(f"✅ Found {len(tasks)} task types")
        
        return True
    except ImportError as e:
        print(f"❌ LLM manager import failed: {e}")
        return False

def test_environment_detection():
    """Test environment detection from .env"""
    print("\n" + "="*60)
    print("Testing Environment Detection")
    print("="*60)
    
    # Check if .env exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Try to load with dotenv
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            env = os.getenv("ENV", "development")
            debug = os.getenv("DEBUG", "false").lower() == "true"
            
            print(f"✅ Environment: {env}")
            print(f"✅ Debug mode: {debug}")
            
            # Check for API keys (without showing values)
            api_keys = [
                "GOOGLE_API_KEY",
                "OPENAI_API_KEY", 
                "XAI_API_KEY",
                "ANTHROPIC_API_KEY"
            ]
            
            available_keys = []
            for key in api_keys:
                if os.getenv(key):
                    available_keys.append(key)
            
            print(f"✅ Available API keys: {len(available_keys)}/{len(api_keys)}")
            if available_keys:
                print(f"   Keys found: {available_keys}")
            
        except Exception as e:
            print(f"❌ Error loading .env: {e}")
    else:
        print("⚠️ .env file not found (using .env.example as reference)")

def test_llm_manager_functionality():
    """Test LLM manager core functionality"""
    print("\n" + "="*60)
    print("Testing LLM Manager Functionality")
    print("="*60)
    
    try:
        from llm.llm_manager import LLMManager, TaskType
        
        # Initialize manager
        manager = LLMManager()
        print("✅ LLM manager initialized")
        
        # Test provider listing
        providers = manager.list_available_providers()
        print(f"✅ Available providers: {list(providers.keys())}")
        
        for provider, info in providers.items():
            status = info["status"]
            models = len(info["models"])
            print(f"   {provider}: {models} models, {status}")
        
        # Test task assignment (without actual LLM calls)
        test_task = TaskType.TREND_ANALYSIS
        print(f"\n✅ Testing task assignment for: {test_task.value}")
        
        # This will try to get LLM but won't fail if API keys missing
        llm = manager.get_llm_for_task(test_task)
        if llm:
            print(f"✅ LLM assigned for {test_task.value}")
        else:
            print(f"⚠️ No LLM available for {test_task.value} (likely missing API keys)")
        
        # Test cost estimation
        cost = manager.estimate_cost(test_task, 1000, 500)
        print(f"✅ Cost estimation: ${cost:.4f} for 1500 tokens")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM manager test failed: {e}")
        return False

def main():
    """Run all configuration tests"""
    print("Multi-LLM Configuration System Test")
    print("="*60)
    
    # Change to backend directory (where config files are located)
    backend_dir = Path(__file__).parent.parent.parent
    os.chdir(backend_dir)
    
    # Run tests
    test_config_files()
    
    manager_available = test_llm_manager_import()
    
    test_environment_detection()
    
    if manager_available:
        test_llm_manager_functionality()
    
    print("\n" + "="*60)
    print("Configuration System Summary")
    print("="*60)
    print("\n✅ Configuration Design:")
    print("   - API keys in .env (not committed)")
    print("   - Model capabilities in config/llm_config.yaml (committed)")
    print("   - Task assignments in config/task_assignments.yaml (committed)")
    print("   - Environment-specific settings supported")
    print("\n✅ Benefits:")
    print("   - Security: API keys separate from code")
    print("   - Flexibility: Easy to switch models per task")
    print("   - Scalability: Support for multiple providers")
    print("   - Cost control: Different configs for dev/prod")

if __name__ == "__main__":
    main()