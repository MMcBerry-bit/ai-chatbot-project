"""
Unit tests for Gemini Service
Tests Google Gemini API integration
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.gemini_service import GeminiService


class TestGeminiService(unittest.TestCase):
    """Test cases for GeminiService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_api_key = "test-google-key-123"
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai.Client')
    def test_initialization_with_env_var(self, mock_client_class):
        """Test service initialization with environment variable"""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        service = GeminiService()
        
        self.assertIsNotNone(service.client)
        self.assertEqual(service.model_name, "gemini-1.5-flash")
        mock_client_class.assert_called_once_with(api_key='test-key-123')
    
    @patch('services.gemini_service.genai.Client')
    def test_initialization_with_api_key(self, mock_client_class):
        """Test service initialization with explicit API key"""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        service = GeminiService(api_key=self.mock_api_key)
        
        self.assertIsNotNone(service.client)
        mock_client_class.assert_called_once_with(api_key=self.mock_api_key)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_api_key(self):
        """Test that initialization fails without API key"""
        with self.assertRaises(ValueError) as context:
            GeminiService()
        self.assertIn("API key not found", str(context.exception))
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai.Client')
    def test_get_response_success(self, mock_client_class):
        """Test successful response from Gemini API"""
        # Mock the response
        mock_response = Mock()
        mock_response.text = "This is a test response from Gemini"
        
        mock_models = Mock()
        mock_models.generate_content.return_value = mock_response
        
        mock_client = Mock()
        mock_client.models = mock_models
        mock_client_class.return_value = mock_client
        
        service = GeminiService()
        
        messages = [
            {"role": "user", "content": "Hello"}
        ]
        
        response = service.get_response(messages)
        
        self.assertEqual(response, "This is a test response from Gemini")
        mock_models.generate_content.assert_called_once()
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai.Client')
    def test_get_response_with_conversation_history(self, mock_client_class):
        """Test response with conversation history"""
        mock_response = Mock()
        mock_response.text = "Response with history"
        
        mock_models = Mock()
        mock_models.generate_content.return_value = mock_response
        
        mock_client = Mock()
        mock_client.models = mock_models
        mock_client_class.return_value = mock_client
        
        service = GeminiService()
        
        messages = [
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "First response"},
            {"role": "user", "content": "Second message"}
        ]
        
        response = service.get_response(messages)
        
        self.assertEqual(response, "Response with history")
        mock_models.generate_content.assert_called_once()
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai.Client')
    def test_get_response_skips_system_messages(self, mock_client_class):
        """Test that system messages are skipped"""
        mock_response = Mock()
        mock_response.text = "Response without system"
        
        mock_models = Mock()
        mock_models.generate_content.return_value = mock_response
        
        mock_client = Mock()
        mock_client.models = mock_models
        mock_client_class.return_value = mock_client
        
        service = GeminiService()
        
        messages = [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": "User message"}
        ]
        
        response = service.get_response(messages)
        
        # Should succeed and skip system messages
        self.assertEqual(response, "Response without system")
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai.Client')
    def test_get_model_info(self, mock_client_class):
        """Test getting model information"""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        service = GeminiService()
        
        info = service.get_model_info()
        
        self.assertEqual(info['provider'], 'Google')
        self.assertEqual(info['model'], 'gemini-1.5-flash')
        self.assertIn('multimodal', info['best_for'])
        self.assertIn('object_recognition', info['best_for'])


if __name__ == '__main__':
    unittest.main()
