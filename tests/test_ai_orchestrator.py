"""
Unit tests for AI Orchestrator
Tests intelligent routing and fallback mechanisms
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.ai_orchestrator import AIOrchestrator, TaskType


class TestAIOrchestrator(unittest.TestCase):
    """Test cases for AIOrchestrator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_claude_service = Mock()
        self.mock_gemini_service = Mock()
    
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'GOOGLE_API_KEY': 'test-google-key'
    })
    @patch('services.ai_orchestrator.ClaudeService')
    @patch('services.ai_orchestrator.GeminiService')
    def test_initialization(self, mock_gemini_class, mock_claude_class):
        """Test orchestrator initialization"""
        mock_claude_class.return_value = self.mock_claude_service
        mock_gemini_class.return_value = self.mock_gemini_service
        
        orchestrator = AIOrchestrator()
        
        self.assertEqual(orchestrator.primary_provider, "claude")
        self.assertIn("claude", orchestrator.services)
        self.assertIn("gemini", orchestrator.services)
        self.assertIn("github", orchestrator.services)
    
    def test_detect_task_type_grammar(self):
        """Test detection of grammar correction tasks"""
        orchestrator = AIOrchestrator()
        
        message = "Please correct my grammar in this sentence"
        task_type = orchestrator.detect_task_type(message)
        
        self.assertEqual(task_type, TaskType.GRAMMAR_CORRECTION)
    
    def test_detect_task_type_reasoning(self):
        """Test detection of reasoning tasks"""
        orchestrator = AIOrchestrator()
        
        message = "Can you explain why the sky is blue?"
        task_type = orchestrator.detect_task_type(message)
        
        self.assertEqual(task_type, TaskType.REASONING)
    
    def test_detect_task_type_creative(self):
        """Test detection of creative writing tasks"""
        orchestrator = AIOrchestrator()
        
        message = "Write me a short story about a dragon"
        task_type = orchestrator.detect_task_type(message)
        
        self.assertEqual(task_type, TaskType.CREATIVE_WRITING)
    
    def test_detect_task_type_quick_response(self):
        """Test detection of quick response needs"""
        orchestrator = AIOrchestrator()
        
        message = "What time is it?"
        task_type = orchestrator.detect_task_type(message)
        
        self.assertEqual(task_type, TaskType.QUICK_RESPONSE)
    
    def test_detect_task_type_general(self):
        """Test detection of general tasks"""
        orchestrator = AIOrchestrator()
        
        message = "Tell me about Python programming"
        task_type = orchestrator.detect_task_type(message)
        
        self.assertEqual(task_type, TaskType.GENERAL)
    
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'GOOGLE_API_KEY': 'test-google-key'
    })
    @patch('services.ai_orchestrator.ClaudeService')
    @patch('services.ai_orchestrator.GeminiService')
    def test_get_preferred_provider_grammar(self, mock_gemini_class, mock_claude_class):
        """Test preferred provider for grammar tasks"""
        mock_claude_class.return_value = self.mock_claude_service
        mock_gemini_class.return_value = self.mock_gemini_service
        
        orchestrator = AIOrchestrator()
        
        provider = orchestrator.get_preferred_provider(TaskType.GRAMMAR_CORRECTION)
        
        self.assertEqual(provider, "claude")
    
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'GOOGLE_API_KEY': 'test-google-key'
    })
    @patch('services.ai_orchestrator.ClaudeService')
    @patch('services.ai_orchestrator.GeminiService')
    def test_get_preferred_provider_multimodal(self, mock_gemini_class, mock_claude_class):
        """Test preferred provider for multimodal tasks"""
        mock_claude_class.return_value = self.mock_claude_service
        mock_gemini_class.return_value = self.mock_gemini_service
        
        orchestrator = AIOrchestrator()
        
        provider = orchestrator.get_preferred_provider(TaskType.MULTIMODAL)
        
        self.assertEqual(provider, "gemini")
    
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'GOOGLE_API_KEY': 'test-google-key'
    })
    @patch('services.ai_orchestrator.ClaudeService')
    @patch('services.ai_orchestrator.GeminiService')
    def test_get_response_with_claude(self, mock_gemini_class, mock_claude_class):
        """Test getting response using Claude"""
        mock_claude = Mock()
        mock_claude.get_response.return_value = "Response from Claude"
        mock_claude_class.return_value = mock_claude
        mock_gemini_class.return_value = self.mock_gemini_service
        
        orchestrator = AIOrchestrator(primary_provider="claude")
        
        messages = [{"role": "user", "content": "Hello"}]
        result = orchestrator.get_response(messages)
        
        self.assertEqual(result['content'], "Response from Claude")
        self.assertEqual(result['provider'], "claude")
        mock_claude.get_response.assert_called_once()
    
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'GOOGLE_API_KEY': 'test-google-key'
    })
    @patch('services.ai_orchestrator.ClaudeService')
    @patch('services.ai_orchestrator.GeminiService')
    def test_fallback_mechanism(self, mock_gemini_class, mock_claude_class):
        """Test fallback to secondary provider when primary fails"""
        # Claude fails
        mock_claude = Mock()
        mock_claude.get_response.side_effect = Exception("Claude API error")
        mock_claude_class.return_value = mock_claude
        
        # Gemini succeeds
        mock_gemini = Mock()
        mock_gemini.get_response.return_value = "Response from Gemini"
        mock_gemini_class.return_value = mock_gemini
        
        orchestrator = AIOrchestrator(primary_provider="claude")
        
        messages = [{"role": "user", "content": "Hello"}]
        result = orchestrator.get_response(messages)
        
        self.assertEqual(result['content'], "Response from Gemini")
        self.assertEqual(result['provider'], "gemini")
        mock_claude.get_response.assert_called_once()
        mock_gemini.get_response.assert_called_once()
    
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'GOOGLE_API_KEY': 'test-google-key'
    })
    @patch('services.ai_orchestrator.ClaudeService')
    @patch('services.ai_orchestrator.GeminiService')
    def test_provider_override(self, mock_gemini_class, mock_claude_class):
        """Test forcing a specific provider"""
        mock_claude = Mock()
        mock_claude.get_response.return_value = "Response from Claude"
        mock_claude_class.return_value = mock_claude
        
        mock_gemini = Mock()
        mock_gemini.get_response.return_value = "Response from Gemini"
        mock_gemini_class.return_value = mock_gemini
        
        orchestrator = AIOrchestrator(primary_provider="gemini")
        
        messages = [{"role": "user", "content": "Hello"}]
        result = orchestrator.get_response(messages, provider_override="claude")
        
        self.assertEqual(result['content'], "Response from Claude")
        self.assertEqual(result['provider'], "claude")
        mock_claude.get_response.assert_called_once()
        # Gemini should not be called
        mock_gemini.get_response.assert_not_called()
    
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'GOOGLE_API_KEY': 'test-google-key'
    })
    @patch('services.ai_orchestrator.ClaudeService')
    @patch('services.ai_orchestrator.GeminiService')
    def test_get_available_providers(self, mock_gemini_class, mock_claude_class):
        """Test getting list of available providers"""
        mock_claude = Mock()
        mock_claude.get_model_info.return_value = {
            "provider": "Anthropic",
            "model": "claude-3-5-sonnet-20241022"
        }
        mock_claude.is_available.return_value = True
        mock_claude_class.return_value = mock_claude
        
        mock_gemini = Mock()
        mock_gemini.get_model_info.return_value = {
            "provider": "Google",
            "model": "gemini-1.5-flash"
        }
        mock_gemini.is_available.return_value = True
        mock_gemini_class.return_value = mock_gemini
        
        orchestrator = AIOrchestrator()
        
        providers = orchestrator.get_available_providers()
        
        self.assertGreaterEqual(len(providers), 2)
        provider_names = [p.get('name') or p.get('provider') for p in providers]
        self.assertIn("claude", [p.lower() for p in provider_names if p])


if __name__ == '__main__':
    unittest.main()
