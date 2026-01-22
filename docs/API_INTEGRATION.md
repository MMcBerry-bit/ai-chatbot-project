# API Integration Guide

## Overview

This AI Chatbot project now supports multiple AI providers with intelligent routing and fallback mechanisms:

- **GitHub Models** (Primary/Fallback) - OpenAI GPT models via GitHub
- **Anthropic Claude** - Advanced reasoning and conversation
- **Google Gemini** - Fast multimodal AI

The system automatically selects the best provider for each task and falls back to alternatives if one becomes unavailable.

---

## Table of Contents

1. [Setup and Configuration](#setup-and-configuration)
2. [Service Architecture](#service-architecture)
3. [API Integration Details](#api-integration-details)
4. [Intelligent Routing](#intelligent-routing)
5. [Fallback Mechanisms](#fallback-mechanisms)
6. [Usage Examples](#usage-examples)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Setup and Configuration

### 1. Install Dependencies

```bash
pip install -r requirements_app.txt
```

This installs:
- `anthropic>=0.39.0` - Anthropic Claude API client
- `google-genai>=0.2.0` - Google Gemini API client
- Other required packages

### 2. Obtain API Keys

#### GitHub Token (Required)
1. Go to https://github.com/settings/tokens
2. Generate a new token
3. No special scopes needed for GitHub Models

#### Anthropic API Key (Optional)
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

#### Google API Key (Optional)
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key

### 3. Configure Environment Variables

Copy the example file and add your keys:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```bash
# Required for basic functionality
GITHUB_TOKEN=your_github_token_here

# Optional - enables Claude integration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional - enables Gemini integration
GOOGLE_API_KEY=your_google_api_key_here
```

**Note:** The chatbot will work with just the GitHub token, but having all three providers enables intelligent routing and better fallback options.

---

## Service Architecture

### Directory Structure

```
src/
├── services/
│   ├── __init__.py              # Service exports
│   ├── claude_service.py        # Anthropic Claude integration
│   ├── gemini_service.py        # Google Gemini integration
│   └── ai_orchestrator.py       # Intelligent routing & fallback
└── ai_chatbot.py                # Main chatbot with multi-provider support
```

### Component Responsibilities

#### ClaudeService (`claude_service.py`)
- Handles all interactions with Anthropic's Claude API
- Manages authentication and request formatting
- Best for: reasoning, grammar correction, analysis, conversation

#### GeminiService (`gemini_service.py`)
- Handles all interactions with Google's Gemini API
- Manages authentication and request formatting
- Best for: multimodal tasks, object recognition, quick responses

#### AIOrchestrator (`ai_orchestrator.py`)
- Routes requests to the optimal provider
- Implements fallback chain when providers fail
- Detects task types for intelligent routing
- Manages provider health checks

---

## API Integration Details

### Claude Service

**Model:** `claude-3-5-sonnet-20241022`

**Features:**
- Advanced reasoning capabilities
- Excellent for grammar and language tasks
- Long context window
- Structured system prompts

**Example Usage:**
```python
from services.claude_service import ClaudeService

service = ClaudeService()
messages = [
    {"role": "user", "content": "Explain quantum computing"}
]
response = service.get_response(
    messages=messages,
    system_prompt="You are a helpful science teacher",
    temperature=0.7
)
print(response)
```

### Gemini Service

**Model:** `gemini-1.5-flash`

**Features:**
- Fast response times
- Multimodal capabilities (text, future: images)
- Cost-effective for high-volume requests
- Good general-purpose AI

**Example Usage:**
```python
from services.gemini_service import GeminiService

service = GeminiService()
messages = [
    {"role": "user", "content": "What's the weather like?"}
]
response = service.get_response(
    messages=messages,
    temperature=0.7
)
print(response)
```

### AI Orchestrator

**Example Usage:**
```python
from services.ai_orchestrator import AIOrchestrator, TaskType

orchestrator = AIOrchestrator(primary_provider="claude")

# Automatic task detection
messages = [{"role": "user", "content": "Fix my grammar"}]
result = orchestrator.get_response(messages)
print(f"Response from {result['provider']}: {result['content']}")

# Manual provider selection
result = orchestrator.get_response(
    messages=messages,
    provider_override="gemini"
)

# Check provider health
health = orchestrator.health_check()
print(health)  # {'claude': True, 'gemini': True, 'github': True}
```

---

## Intelligent Routing

The orchestrator automatically detects task types and routes to the best provider:

### Task Type Detection

| Task Type | Keywords | Preferred Provider |
|-----------|----------|-------------------|
| **Grammar Correction** | correct, grammar, spelling, fix, proofread | Claude → Gemini |
| **Reasoning** | why, explain, analyze, reason, logic, solve | Claude → Gemini |
| **Creative Writing** | write, story, poem, creative, compose | Claude → Gemini |
| **Object Recognition** | (future feature) | Gemini → Claude |
| **Quick Response** | Short questions with "?" | Gemini → GitHub |
| **General** | Everything else | Primary → Fallback chain |

### Provider Preferences by Task

```python
# In ai_orchestrator.py
self.task_preferences = {
    TaskType.GRAMMAR_CORRECTION: ["claude", "gemini"],
    TaskType.REASONING: ["claude", "gemini"],
    TaskType.CREATIVE_WRITING: ["claude", "gemini"],
    TaskType.OBJECT_RECOGNITION: ["gemini", "claude"],
    TaskType.MULTIMODAL: ["gemini", "claude"],
    TaskType.QUICK_RESPONSE: ["gemini", "github"],
    TaskType.GENERAL: [primary_provider, "claude", "gemini", "github"]
}
```

---

## Fallback Mechanisms

### How Fallback Works

1. **Primary Provider Attempt**: The orchestrator tries the preferred provider first
2. **Error Detection**: If the request fails (timeout, rate limit, API error)
3. **Fallback Chain**: Automatically tries the next provider in the chain
4. **Success or Failure**: Returns response or raises exception if all fail

### Default Fallback Chain

```
claude → gemini → github
```

### Custom Fallback Chain

```python
orchestrator = AIOrchestrator(
    primary_provider="gemini",
    fallback_chain=["gemini", "claude", "github"]
)
```

### Error Handling

```python
try:
    result = orchestrator.get_response(messages)
    print(f"✓ Success with {result['provider']}")
except Exception as e:
    print(f"✗ All providers failed: {e}")
```

---

## Usage Examples

### Basic Chatbot

```python
from src.ai_chatbot import AIChatbot

# Start with orchestrator enabled
chatbot = AIChatbot(use_orchestrator=True)
chatbot.run()
```

### Commands

```
/help       - Show help message
/clear      - Clear conversation history
/providers  - Show available AI providers
/quit       - Exit chatbot
```

### Programmatic Usage

```python
from services.ai_orchestrator import AIOrchestrator

orchestrator = AIOrchestrator()

# Check which providers are available
providers = orchestrator.get_available_providers()
for p in providers:
    print(f"{p['name']}: {p['status']}")

# Have a conversation
messages = []
while True:
    user_input = input("You: ")
    if user_input == "/quit":
        break
    
    messages.append({"role": "user", "content": user_input})
    
    result = orchestrator.get_response(messages)
    print(f"Assistant ({result['provider']}): {result['content']}")
    
    messages.append({"role": "assistant", "content": result['content']})
```

---

## Testing

### Running Unit Tests

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test file
python -m unittest tests.test_claude_service -v
python -m unittest tests.test_gemini_service -v
python -m unittest tests.test_ai_orchestrator -v
```

### Test Coverage

- **Claude Service Tests**: 8 tests
  - Initialization with/without API keys
  - Response generation
  - System prompt handling
  - Message filtering

- **Gemini Service Tests**: 7 tests
  - Initialization with/without API keys
  - Response generation
  - Conversation history
  - Message filtering

- **Orchestrator Tests**: 12 tests
  - Task type detection
  - Provider selection
  - Fallback mechanism
  - Provider override

### Manual Testing

Test the chatbot with different types of queries:

```bash
# Test grammar correction (should use Claude)
You: Please fix my grammer in this sentance

# Test quick question (should use Gemini)
You: What's 2+2?

# Test reasoning (should use Claude)
You: Explain why the sky is blue

# Check providers
You: /providers
```

---

## Troubleshooting

### Common Issues

#### 1. "API key not found" Error

**Problem:** Service can't find API key
**Solution:** 
```bash
# Check .env file exists and has correct keys
cat .env

# Make sure to load environment variables
export ANTHROPIC_API_KEY=your_key_here
export GOOGLE_API_KEY=your_key_here
```

#### 2. Import Errors

**Problem:** `ModuleNotFoundError: No module named 'anthropic'`
**Solution:**
```bash
pip install -r requirements_app.txt
```

#### 3. All Providers Failing

**Problem:** "All AI providers failed"
**Solution:**
- Check your internet connection
- Verify API keys are valid and not expired
- Check if you've exceeded rate limits
- Ensure at least GitHub token is configured

#### 4. Tests Failing

**Problem:** Tests fail with import errors
**Solution:**
```bash
# Install test dependencies
pip install anthropic google-genai

# Run from project root
cd /path/to/ai-chatbot-project
python -m unittest discover -s tests
```

### Debugging Tips

1. **Enable Verbose Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check Provider Health**
   ```python
   orchestrator = AIOrchestrator()
   health = orchestrator.health_check()
   print(health)
   ```

3. **Test Individual Services**
   ```python
   # Test Claude
   from services.claude_service import ClaudeService
   service = ClaudeService()
   print(service.is_available())
   
   # Test Gemini
   from services.gemini_service import GeminiService
   service = GeminiService()
   print(service.is_available())
   ```

### Getting Help

- **GitHub Issues**: [Create an issue](https://github.com/MMcBerry-bit/ai-chatbot-project/issues)
- **Documentation**: Check other docs in the `docs/` folder
- **API Documentation**:
  - [Anthropic Claude API](https://docs.anthropic.com/)
  - [Google Gemini API](https://ai.google.dev/docs)
  - [GitHub Models](https://github.com/marketplace/models)

---

## Best Practices

### 1. API Key Security

- ✅ Store keys in `.env` file
- ✅ Add `.env` to `.gitignore`
- ✅ Use environment variables in production
- ❌ Never commit API keys to version control
- ❌ Never hardcode keys in source files

### 2. Error Handling

```python
# Good: Handle provider failures gracefully
try:
    result = orchestrator.get_response(messages)
except Exception as e:
    print(f"Error: {e}")
    # Fallback to local processing or user notification
```

### 3. Rate Limiting

- Monitor your API usage
- Implement caching for repeated queries
- Use GitHub Models for high-volume requests
- Consider implementing request queuing

### 4. Cost Optimization

- Use Gemini for quick, simple queries (most cost-effective)
- Use Claude for complex reasoning tasks
- Use GitHub Models as free fallback
- Cache responses when appropriate

---

## Version History

### v1.2.0 - Current
- ✅ Multi-provider support (GitHub, Claude, Gemini)
- ✅ Intelligent task routing
- ✅ Automatic fallback mechanism
- ✅ Comprehensive unit tests
- ✅ Full documentation

### Future Enhancements
- [ ] Multimodal support (images, audio)
- [ ] Streaming responses
- [ ] Custom provider plugins
- [ ] Advanced caching layer
- [ ] Request rate limiting
- [ ] Provider cost tracking

---

## License

MIT License - See LICENSE file for details

---

## Contact

- **Developer**: Dorcas Innovations LLC
- **GitHub**: https://github.com/MMcBerry-bit/ai-chatbot-project
- **Support**: Open an issue on GitHub

---

*Last Updated: January 2025*
