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
    @patch('services.gemini_service.genai')
    def test_initialization_with_env_var(self, mock_genai):
        """Test service initialization with environment variable"""
        mock_genai.GenerativeModel.return_value = Mock()
        
        service = GeminiService()
        
        self.assertIsNotNone(service.model)
        self.assertEqual(service.model_name, "gemini-1.5-flash")
        mock_genai.configure.assert_called_once_with(api_key='test-key-123')
    
    @patch('services.gemini_service.genai')
    def test_initialization_with_api_key(self, mock_genai):
        """Test service initialization with explicit API key"""
        mock_genai.GenerativeModel.return_value = Mock()
        
        service = GeminiService(api_key=self.mock_api_key)
        
        self.assertIsNotNone(service.model)
        mock_genai.configure.assert_called_once_with(api_key=self.mock_api_key)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_api_key(self):
        """Test that initialization fails without API key"""
        with self.assertRaises(ValueError) as context:
            GeminiService()
        self.assertIn("API key not found", str(context.exception))
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai')
    def test_get_response_success(self, mock_genai):
        """Test successful response from Gemini API"""
        # Mock the chat and response
        mock_response = Mock()
        mock_response.text = "This is a test response from Gemini"
        
        mock_chat = Mock()
        mock_chat.send_message.return_value = mock_response
        
        mock_model = Mock()
        mock_model.start_chat.return_value = mock_chat
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService()
        
        messages = [
            {"role": "user", "content": "Hello"}
        ]
        
        response = service.get_response(messages)
        
        self.assertEqual(response, "This is a test response from Gemini")
        mock_chat.send_message.assert_called_once()
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai')
    def test_get_response_with_conversation_history(self, mock_genai):
        """Test response with conversation history"""
        mock_response = Mock()
        mock_response.text = "Response with history"
        
        mock_chat = Mock()
        mock_chat.send_message.return_value = mock_response
        
        mock_model = Mock()
        mock_model.start_chat.return_value = mock_chat
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService()
        
        messages = [
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "First response"},
            {"role": "user", "content": "Second message"}
        ]
        
        response = service.get_response(messages)
        
        self.assertEqual(response, "Response with history")
        # Check that start_chat was called with history
        mock_model.start_chat.assert_called_once()
        call_args = mock_model.start_chat.call_args
        # Should have 2 messages in history (excluding the last one)
        self.assertEqual(len(call_args[1]['history']), 2)
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai')
    def test_get_response_skips_system_messages(self, mock_genai):
        """Test that system messages are skipped"""
        mock_response = Mock()
        mock_response.text = "Response without system"
        
        mock_chat = Mock()
        mock_chat.send_message.return_value = mock_response
        
        mock_model = Mock()
        mock_model.start_chat.return_value = mock_chat
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService()
        
        messages = [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": "User message"}
        ]
        
        response = service.get_response(messages)
        
        # System messages should be filtered out
        call_args = mock_model.start_chat.call_args
        history = call_args[1]['history']
        # Should be empty since only system and last user message
        self.assertEqual(len(history), 0)
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai')
    def test_get_response_with_system_prompt(self, mock_genai):
        """Test response with system prompt prepended"""
        mock_response = Mock()
        mock_response.text = "Response with system prompt"
        
        mock_chat = Mock()
        mock_chat.send_message.return_value = mock_response
        
        mock_model = Mock()
        mock_model.start_chat.return_value = mock_chat
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService()
        
        messages = [
            {"role": "user", "content": "Test message"}
        ]
        system_prompt = "You are a helpful assistant"
        
        response = service.get_response(messages, system_prompt=system_prompt)
        
        # Check that system prompt was prepended to message
        call_args = mock_chat.send_message.call_args
        sent_message = call_args[0][0]
        self.assertIn("System:", sent_message)
        self.assertIn("Test message", sent_message)
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-key-123'})
    @patch('services.gemini_service.genai')
    def test_get_model_info(self, mock_genai):
        """Test getting model information"""
        mock_genai.GenerativeModel.return_value = Mock()
        
        service = GeminiService()
        
        info = service.get_model_info()
        
        self.assertEqual(info['provider'], 'Google')
        self.assertEqual(info['model'], 'gemini-1.5-flash')
        self.assertIn('multimodal', info['best_for'])
        self.assertIn('object_recognition', info['best_for'])


if __name__ == '__main__':
    unittest.main()
