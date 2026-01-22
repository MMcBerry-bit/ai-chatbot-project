"""
AI Orchestrator - Intelligent Model Selection and Fallback
Manages multiple AI providers and switches between them based on task type
"""

import os
import re
from typing import List, Dict, Optional, Literal
from enum import Enum

# Import services with error handling
try:
    from .claude_service import ClaudeService
except ImportError:
    ClaudeService = None

try:
    from .gemini_service import GeminiService
except ImportError:
    GeminiService = None


class TaskType(Enum):
    """Enum for different task types that influence model selection"""
    GENERAL = "general"
    GRAMMAR_CORRECTION = "grammar_correction"
    REASONING = "reasoning"
    CREATIVE_WRITING = "creative_writing"
    OBJECT_RECOGNITION = "object_recognition"
    MULTIMODAL = "multimodal"
    QUICK_RESPONSE = "quick_response"


class AIOrchestrator:
    """
    Orchestrates between multiple AI providers with intelligent routing and fallback
    """
    
    def __init__(self, primary_provider: str = "claude", fallback_chain: Optional[List[str]] = None):
        """
        Initialize the AI orchestrator
        
        Args:
            primary_provider: Primary AI provider to use ("claude", "gemini", or "github")
            fallback_chain: List of providers to fallback to in order
        """
        self.primary_provider = primary_provider
        self.fallback_chain = fallback_chain or ["claude", "gemini", "github"]
        
        # Initialize available services
        self.services = {}
        self._initialize_services()
        
        # Task routing preferences
        self.task_preferences = {
            TaskType.GRAMMAR_CORRECTION: ["claude", "gemini"],
            TaskType.REASONING: ["claude", "gemini"],
            TaskType.CREATIVE_WRITING: ["claude", "gemini"],
            TaskType.OBJECT_RECOGNITION: ["gemini", "claude"],
            TaskType.MULTIMODAL: ["gemini", "claude"],
            TaskType.QUICK_RESPONSE: ["gemini", "github"],
            TaskType.GENERAL: [primary_provider, "claude", "gemini", "github"]
        }
        
    def _initialize_services(self):
        """Initialize all available AI services"""
        # Try to initialize Claude
        if ClaudeService and os.environ.get("ANTHROPIC_API_KEY"):
            try:
                self.services["claude"] = ClaudeService()
            except Exception as e:
                print(f"Warning: Could not initialize Claude service: {e}")
        
        # Try to initialize Gemini
        if GeminiService and os.environ.get("GOOGLE_API_KEY"):
            try:
                self.services["gemini"] = GeminiService()
            except Exception as e:
                print(f"Warning: Could not initialize Gemini service: {e}")
        
        # GitHub is always available (assumed to be configured in main app)
        self.services["github"] = "available"
    
    def detect_task_type(self, message: str) -> TaskType:
        """
        Detect the task type from the user's message
        
        Args:
            message: User's input message
            
        Returns:
            TaskType: Detected task type
        """
        message_lower = message.lower()
        
        # Check for grammar/spelling correction requests
        grammar_keywords = ["correct", "grammar", "spelling", "fix", "proofread"]
        if any(keyword in message_lower for keyword in grammar_keywords):
            return TaskType.GRAMMAR_CORRECTION
        
        # Check for reasoning tasks
        reasoning_keywords = ["why", "explain", "analyze", "reason", "logic", "solve"]
        if any(keyword in message_lower for keyword in reasoning_keywords):
            return TaskType.REASONING
        
        # Check for creative writing
        creative_keywords = ["write", "story", "poem", "creative", "compose"]
        if any(keyword in message_lower for keyword in creative_keywords):
            return TaskType.CREATIVE_WRITING
        
        # Check for quick response needs
        if len(message) < 50 and "?" in message:
            return TaskType.QUICK_RESPONSE
        
        # Default to general
        return TaskType.GENERAL
    
    def get_preferred_provider(self, task_type: TaskType) -> str:
        """
        Get the preferred provider for a given task type
        
        Args:
            task_type: Type of task to perform
            
        Returns:
            str: Preferred provider name
        """
        preferences = self.task_preferences.get(task_type, [self.primary_provider])
        
        # Return first available provider from preferences
        for provider in preferences:
            if provider in self.services:
                return provider
        
        # Fallback to any available provider
        return next(iter(self.services.keys()))
    
    def get_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        task_type: Optional[TaskType] = None,
        temperature: float = 0.7,
        provider_override: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Get a response from the best available AI provider
        
        Args:
            messages: Conversation history
            system_prompt: System prompt to guide behavior
            task_type: Type of task (auto-detected if not provided)
            temperature: Response creativity
            provider_override: Force a specific provider
            
        Returns:
            dict: Response with 'content' and 'provider' keys
        """
        # Detect task type if not provided
        if task_type is None and messages:
            last_message = messages[-1].get("content", "")
            task_type = self.detect_task_type(last_message)
        
        # Determine provider to use
        if provider_override and provider_override in self.services:
            providers_to_try = [provider_override]
        else:
            preferred = self.get_preferred_provider(task_type or TaskType.GENERAL)
            providers_to_try = [preferred] + [p for p in self.fallback_chain if p != preferred]
        
        # Try each provider in order
        last_error = None
        for provider in providers_to_try:
            if provider not in self.services:
                continue
            
            try:
                # Skip GitHub provider in this implementation (handled by main app)
                if provider == "github":
                    continue
                
                service = self.services[provider]
                response = service.get_response(
                    messages=messages,
                    system_prompt=system_prompt,
                    temperature=temperature
                )
                
                return {
                    "content": response,
                    "provider": provider,
                    "task_type": task_type.value if task_type else "general"
                }
                
            except Exception as e:
                last_error = e
                print(f"Provider {provider} failed: {e}")
                continue
        
        # All providers failed
        raise Exception(f"All AI providers failed. Last error: {last_error}")
    
    def get_available_providers(self) -> List[Dict[str, any]]:
        """
        Get list of available providers and their info
        
        Returns:
            list: List of provider info dicts
        """
        providers = []
        
        for name, service in self.services.items():
            if name == "github":
                providers.append({
                    "name": "github",
                    "provider": "GitHub Models",
                    "status": "available"
                })
            elif hasattr(service, "get_model_info"):
                info = service.get_model_info()
                info["name"] = name
                info["status"] = "available" if service.is_available() else "unavailable"
                providers.append(info)
        
        return providers
    
    def health_check(self) -> Dict[str, bool]:
        """
        Check health status of all providers
        
        Returns:
            dict: Provider name to availability status
        """
        health = {}
        
        for name, service in self.services.items():
            if name == "github":
                health[name] = True
            elif hasattr(service, "is_available"):
                health[name] = service.is_available()
            else:
                health[name] = False
        
        return health
