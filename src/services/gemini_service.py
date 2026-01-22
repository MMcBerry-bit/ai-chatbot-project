"""
Gemini Service - Google AI Integration
Handles all interactions with Google's Gemini AI models
"""

import os
from typing import List, Dict, Optional
from google import genai
from google.genai import types


class GeminiService:
    """Service class for interacting with Google's Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini service
        
        Args:
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key not found. Set GOOGLE_API_KEY environment variable.")
        
        # Initialize client with API key
        self.client = genai.Client(api_key=self.api_key)
        
        # Model configuration
        self.model_name = "gemini-1.5-flash"  # Fast, efficient model
        
        # Generation config
        self.generation_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_output_tokens=1024,
        )
        
    def get_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Get a response from Gemini
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt to guide behavior
            temperature: Response creativity (0.0-1.0)
            
        Returns:
            str: Gemini's response text
            
        Raises:
            Exception: If API request fails
        """
        try:
            # Update generation config with temperature
            config = types.GenerateContentConfig(
                temperature=temperature,
                top_p=0.95,
                top_k=40,
                max_output_tokens=1024,
            )
            
            # Add system instruction if provided
            system_instruction = system_prompt if system_prompt else None
            
            # Convert messages to Gemini format
            chat_history = []
            for msg in messages[:-1]:  # Exclude last message
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                # Skip system messages in history
                if role == "system":
                    continue
                    
                # Map roles to Gemini format
                gemini_role = "model" if role == "assistant" else "user"
                chat_history.append(types.Content(
                    role=gemini_role,
                    parts=[types.Part(text=content)]
                ))
            
            # Get the last message (user's current message)
            last_message = messages[-1].get("content", "") if messages else ""
            
            # Generate response using chat
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[*chat_history, types.Content(
                    role="user",
                    parts=[types.Part(text=last_message)]
                )],
                config=config
            )
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def is_available(self) -> bool:
        """
        Check if Gemini API is available
        
        Returns:
            bool: True if API is accessible
        """
        try:
            # Simple test request
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Hi"
            )
            return bool(response.text)
        except:
            return False
    
    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the current model
        
        Returns:
            dict: Model information
        """
        return {
            "provider": "Google",
            "model": self.model_name,
            "description": "Gemini 1.5 Flash - Fast multimodal AI",
            "best_for": ["object_recognition", "multimodal", "quick_responses", "general_tasks"]
        }
