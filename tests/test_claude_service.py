"""
Unit tests for Claude Service
Tests Anthropic API integration
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.claude_service import ClaudeService


class TestClaudeService(unittest.TestCase):
    """Test cases for ClaudeService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_api_key = "test-anthropic-key-123"
        
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key-123'})
    @patch('services.claude_service.Anthropic')
    def test_initialization_with_env_var(self, mock_anthropic):
        """Test service initialization with environment variable"""
        service = ClaudeService()
        self.assertIsNotNone(service.client)
        self.assertEqual(service.model, "claude-3-5-sonnet-20241022")
        mock_anthropic.assert_called_once_with(api_key='test-key-123')
    
    @patch('services.claude_service.Anthropic')
    def test_initialization_with_api_key(self, mock_anthropic):
        """Test service initialization with explicit API key"""
        service = ClaudeService(api_key=self.mock_api_key)
        self.assertIsNotNone(service.client)
        mock_anthropic.assert_called_once_with(api_key=self.mock_api_key)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_api_key(self):
        """Test that initialization fails without API key"""
        with self.assertRaises(ValueError) as context:
            ClaudeService()
        self.assertIn("API key not found", str(context.exception))
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key-123'})
    @patch('services.claude_service.Anthropic')
    def test_get_response_success(self, mock_anthropic):
        """Test successful response from Claude API"""
        # Mock the API response
        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "This is a test response from Claude"
        mock_response.content = [mock_content]
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        service = ClaudeService()
        
        messages = [
            {"role": "user", "content": "Hello"}
        ]
        
        response = service.get_response(messages)
        
        self.assertEqual(response, "This is a test response from Claude")
        mock_client.messages.create.assert_called_once()
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key-123'})
    @patch('services.claude_service.Anthropic')
    def test_get_response_with_system_prompt(self, mock_anthropic):
        """Test response with system prompt"""
        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "Response with system prompt"
        mock_response.content = [mock_content]
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        service = ClaudeService()
        
        messages = [
            {"role": "user", "content": "Test message"}
        ]
        system_prompt = "You are a helpful assistant"
        
        response = service.get_response(messages, system_prompt=system_prompt)
        
        self.assertEqual(response, "Response with system prompt")
        call_args = mock_client.messages.create.call_args
        self.assertEqual(call_args[1]['system'], system_prompt)
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key-123'})
    @patch('services.claude_service.Anthropic')
    def test_get_response_filters_system_messages(self, mock_anthropic):
        """Test that system messages are filtered from conversation"""
        mock_response = Mock()
        mock_content = Mock()
        mock_content.text = "Filtered response"
        mock_response.content = [mock_content]
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        service = ClaudeService()
        
        messages = [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": "User message"}
        ]
        
        response = service.get_response(messages)
        
        call_args = mock_client.messages.create.call_args
        # Should only have user message, not system
        self.assertEqual(len(call_args[1]['messages']), 1)
        self.assertEqual(call_args[1]['messages'][0]['role'], 'user')
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key-123'})
    @patch('services.claude_service.Anthropic')
    def test_get_model_info(self, mock_anthropic):
        """Test getting model information"""
        mock_anthropic.return_value = Mock()
        service = ClaudeService()
        
        info = service.get_model_info()
        
        self.assertEqual(info['provider'], 'Anthropic')
        self.assertEqual(info['model'], 'claude-3-5-sonnet-20241022')
        self.assertIn('reasoning', info['best_for'])
        self.assertIn('grammar_correction', info['best_for'])


if __name__ == '__main__':
    unittest.main()
