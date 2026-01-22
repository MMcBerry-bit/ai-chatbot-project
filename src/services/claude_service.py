"""
Claude Service - Anthropic API Integration
Handles all interactions with Anthropic's Claude AI models
"""

import os
from typing import List, Dict, Optional
from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError


class ClaudeService:
    """Service class for interacting with Anthropic's Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Claude service
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Latest Claude model
        self.max_tokens = 1024
        
    def get_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Get a response from Claude
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt to guide behavior
            max_tokens: Maximum tokens in response
            temperature: Response creativity (0.0-1.0)
            
        Returns:
            str: Claude's response text
            
        Raises:
            APIError: If API request fails
        """
        try:
            # Filter out system messages from conversation history
            conversation = [msg for msg in messages if msg.get("role") != "system"]
            
            # Build request parameters
            request_params = {
                "model": self.model,
                "max_tokens": max_tokens or self.max_tokens,
                "temperature": temperature,
                "messages": conversation
            }
            
            # Add system prompt if provided
            if system_prompt:
                request_params["system"] = system_prompt
            
            # Make API call
            response = self.client.messages.create(**request_params)
            
            # Extract text from response
            return response.content[0].text
            
        except RateLimitError as e:
            raise APIError(f"Rate limit exceeded: {str(e)}")
        except APIConnectionError as e:
            raise APIError(f"Connection error: {str(e)}")
        except Exception as e:
            raise APIError(f"Claude API error: {str(e)}")
    
    def is_available(self) -> bool:
        """
        Check if Claude API is available
        
        Returns:
            bool: True if API is accessible
        """
        try:
            # Simple test request
            test_messages = [{"role": "user", "content": "Hi"}]
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=test_messages
            )
            return True
        except:
            return False
    
    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the current model
        
        Returns:
            dict: Model information
        """
        return {
            "provider": "Anthropic",
            "model": self.model,
            "description": "Claude 3.5 Sonnet - Advanced reasoning and conversation",
            "best_for": ["reasoning", "grammar_correction", "conversation", "analysis"]
        }
