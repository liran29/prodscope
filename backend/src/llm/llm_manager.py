#!/usr/bin/env python
"""
LLM Manager for ProdScope
Handles multiple LLM providers and task-specific model selection
"""

import os
import yaml
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import logging

from langchain_core.language_models import BaseLLM
from langchain_core.messages import BaseMessage

logger = logging.getLogger(__name__)

class TaskType(Enum):
    """Supported analysis task types"""
    TREND_ANALYSIS = "trend_analysis"
    PAIN_POINT_ANALYSIS = "pain_point_analysis"
    OPPORTUNITY_IDENTIFICATION = "opportunity_identification"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    KEYWORD_EXTRACTION = "keyword_extraction"
    TEXT_CLASSIFICATION = "text_classification"
    EXECUTIVE_SUMMARY = "executive_summary"
    DETAILED_REPORT = "detailed_report"
    PRODUCT_RECOMMENDATIONS = "product_recommendations"

@dataclass
class LLMConfig:
    """Configuration for a specific LLM"""
    provider: str
    model: str
    description: str
    max_tokens: int
    temperature: float
    cost_per_1k_tokens: float
    use_cases: list

@dataclass
class TaskAssignment:
    """LLM assignment for a specific task"""
    primary_provider: str
    primary_model: str
    fallback_provider: Optional[str] = None
    fallback_model: Optional[str] = None

class LLMManager:
    """Manages multiple LLM providers and task assignments"""
    
    def __init__(self, config_path: str = "config/llm_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.llm_cache: Dict[str, BaseLLM] = {}
        self.development_mode = os.getenv("DEBUG", "false").lower() == "true"
        
    def _load_config(self) -> Dict[str, Any]:
        """Load LLM configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            return self._get_default_config()
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Fallback configuration if config file is not available"""
        return {
            "providers": {
                "google": {
                    "api_key_env": "GOOGLE_API_KEY",
                    "models": {
                        "gemini-1.5-flash": {
                            "description": "Default model",
                            "max_tokens": 8192,
                            "temperature": 0.7,
                            "cost_per_1k_tokens": 0.0005,
                            "use_cases": ["all"]
                        }
                    }
                }
            },
            "task_assignments": {},
            "settings": {
                "retry_attempts": 3,
                "timeout_seconds": 60,
                "fallback_enabled": True
            }
        }
    
    def _create_llm(self, provider: str, model: str) -> Optional[BaseLLM]:
        """Create LLM instance for given provider and model"""
        try:
            if provider == "google":
                from langchain_google_genai import ChatGoogleGenerativeAI
                api_key = os.getenv("GOOGLE_API_KEY")
                if not api_key:
                    logger.warning("Google API key not found")
                    return None
                
                return ChatGoogleGenerativeAI(
                    model=model,
                    google_api_key=api_key,
                    temperature=self._get_model_temperature(provider, model)
                )
            
            elif provider == "openai":
                from langchain_openai import ChatOpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    logger.warning("OpenAI API key not found")
                    return None
                
                return ChatOpenAI(
                    model=model,
                    api_key=api_key,
                    temperature=self._get_model_temperature(provider, model)
                )
            
            elif provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    logger.warning("Anthropic API key not found")
                    return None
                
                return ChatAnthropic(
                    model=model,
                    anthropic_api_key=api_key,
                    temperature=self._get_model_temperature(provider, model)
                )
            
            elif provider == "xai":
                from langchain_openai import ChatOpenAI
                api_key = os.getenv("XAI_API_KEY")
                base_url = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
                if not api_key:
                    logger.warning("xAI API key not found")
                    return None
                
                return ChatOpenAI(
                    model=model,
                    api_key=api_key,
                    base_url=base_url,
                    temperature=self._get_model_temperature(provider, model)
                )
            
            else:
                logger.error(f"Unsupported provider: {provider}")
                return None
                
        except ImportError as e:
            logger.error(f"Required package not installed for {provider}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error creating LLM for {provider}/{model}: {e}")
            return None
    
    def _get_model_temperature(self, provider: str, model: str) -> float:
        """Get temperature setting for a specific model"""
        try:
            return self.config["providers"][provider]["models"][model]["temperature"]
        except KeyError:
            return 0.7  # Default temperature
    
    def get_llm_for_task(self, task: Union[TaskType, str]) -> Optional[BaseLLM]:
        """Get the appropriate LLM for a specific task"""
        if isinstance(task, TaskType):
            task = task.value
        
        # Development mode override
        if self.development_mode:
            dev_config = self.config.get("development", {})
            override = dev_config.get("override_all_to")
            if override:
                return self.get_llm(override["provider"], override["model"])
        
        # Get task assignment
        assignment = self.config.get("task_assignments", {}).get(task, {})
        if not assignment:
            logger.warning(f"No assignment found for task: {task}")
            return self._get_default_llm()
        
        # Try primary LLM
        primary = assignment.get("primary", {})
        if primary:
            llm = self.get_llm(primary["provider"], primary["model"])
            if llm:
                return llm
        
        # Try fallback LLM if enabled
        if self.config.get("settings", {}).get("fallback_enabled", True):
            fallback = assignment.get("fallback", {})
            if fallback:
                llm = self.get_llm(fallback["provider"], fallback["model"])
                if llm:
                    logger.info(f"Using fallback LLM for task: {task}")
                    return llm
        
        # Last resort: default LLM
        logger.warning(f"No suitable LLM found for task: {task}, using default")
        return self._get_default_llm()
    
    def get_llm(self, provider: str, model: str) -> Optional[BaseLLM]:
        """Get LLM instance for specific provider and model"""
        cache_key = f"{provider}:{model}"
        
        if cache_key not in self.llm_cache:
            llm = self._create_llm(provider, model)
            if llm:
                self.llm_cache[cache_key] = llm
            else:
                return None
        
        return self.llm_cache[cache_key]
    
    def _get_default_llm(self) -> Optional[BaseLLM]:
        """Get default LLM (usually the cheapest/most reliable)"""
        # Try to get Google Gemini Flash as default
        return self.get_llm("google", "gemini-1.5-flash")
    
    def list_available_providers(self) -> Dict[str, list]:
        """List all configured providers and their models"""
        result = {}
        for provider, config in self.config.get("providers", {}).items():
            api_key_env = config.get("api_key_env")
            has_key = bool(os.getenv(api_key_env)) if api_key_env else False
            
            models = list(config.get("models", {}).keys())
            result[provider] = {
                "models": models,
                "has_api_key": has_key,
                "status": "available" if has_key else "missing_api_key"
            }
        
        return result
    
    def estimate_cost(self, task: Union[TaskType, str], input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a specific task"""
        if isinstance(task, TaskType):
            task = task.value
        
        assignment = self.config.get("task_assignments", {}).get(task, {})
        primary = assignment.get("primary", {})
        
        if not primary:
            return 0.0
        
        provider = primary["provider"]
        model = primary["model"]
        
        try:
            cost_per_1k = self.config["providers"][provider]["models"][model]["cost_per_1k_tokens"]
            total_tokens = input_tokens + output_tokens
            return (total_tokens / 1000) * cost_per_1k
        except KeyError:
            return 0.0

# Global LLM manager instance
llm_manager = None

def get_llm_manager() -> LLMManager:
    """Get global LLM manager instance"""
    global llm_manager
    if llm_manager is None:
        llm_manager = LLMManager()
    return llm_manager