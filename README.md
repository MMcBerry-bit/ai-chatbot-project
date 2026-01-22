# AI Chatbot - Version 1.2.0
### By Dorcas Innovations LLC

A professional AI chatbot application with **multi-provider AI support**, featuring intelligent routing between GitHub Models, Anthropic Claude, and Google Gemini. Available on the Microsoft Store with premium features.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.2.0-brightgreen.svg)

## 🌟 Features

### 🤖 Multi-Provider AI Support (NEW!)
- **GitHub Models** - Free OpenAI GPT models via GitHub
- **Anthropic Claude** - Advanced reasoning and conversation
- **Google Gemini** - Fast multimodal AI
- **Intelligent Routing** - Automatically selects the best AI for each task
- **Automatic Fallback** - Seamlessly switches providers if one is unavailable

### Free Tier
- 15 AI-powered chats per day
- Access to GPT-4o-mini model
- Multi-provider support with intelligent routing
- Conversation history
- Clean, modern interface

### Unlimited Unlock ($0.99)
- Unlimited daily chats
- Access to GPT-4o-mini model
- Full multi-provider support
- No subscription required
- One-time purchase

### Premium Subscription ($9.99/month)
- Everything in Unlimited
- Access to advanced AI models:
  - GPT-4o
  - o1-preview
  - o1-mini
  - Claude 3.5 Sonnet
  - Gemini 1.5 Flash
- AI Image Generation (powered by Pollinations.ai)
- Priority support

## 📦 Project Structure

### Core Application
- **`src/chatbot_store_ready.py`** - Main Microsoft Store application
- **`src/ai_chatbot.py`** - Console chatbot with multi-provider support
- **`src/usage_tracker.py`** - Daily usage tracking and tier management
- **`src/store_iap.py`** - Microsoft Store in-app purchase handler
- **`src/premium_window.py`** - Premium features UI
- **`src/image_generator.py`** - AI image generation using Pollinations.ai

### AI Services (NEW!)
- **`src/services/claude_service.py`** - Anthropic Claude API integration
- **`src/services/gemini_service.py`** - Google Gemini API integration
- **`src/services/ai_orchestrator.py`** - Intelligent routing and fallback

### Development Versions
- **`src/chatbot_gui.py`** - Basic desktop GUI version
- **`src/chatbot_web.py`** - Web interface using Streamlit

### Testing
- **`tests/test_claude_service.py`** - Claude service unit tests
- **`tests/test_gemini_service.py`** - Gemini service unit tests
- **`tests/test_ai_orchestrator.py`** - Orchestrator unit tests

### Build Tools
- **`build_store_version.py`** - Build script for Microsoft Store
- **`create_msix.ps1`** - MSIX package creator

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- GitHub Personal Access Token (required for basic functionality)
- Anthropic API Key (optional - for Claude integration)
- Google API Key (optional - for Gemini integration)
- Windows 10/11

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MMcBerry-bit/ai-chatbot-project.git
   cd ai-chatbot-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements_app.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env and add your API keys
   # Required:
   GITHUB_TOKEN=your_github_token_here
   
   # Optional (for multi-provider support):
   ANTHROPIC_API_KEY=your_anthropic_key_here
   GOOGLE_API_KEY=your_google_key_here
   ```

4. **Run the application**
   ```bash
   # Console version with multi-provider support
   python src/ai_chatbot.py
   
   # GUI version (basic)
   python src/chatbot_gui.py
   
   # Store version (premium features)
   python src/chatbot_store_ready.py
   ```

## 🔑 Getting API Keys

### GitHub Token (Required)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. No special scopes needed for GitHub Models
4. Copy the token to your `.env` file

### Anthropic Claude (Optional)
1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Add to `.env` as `ANTHROPIC_API_KEY`

### Google Gemini (Optional)
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Create a new API key
4. Add to `.env` as `GOOGLE_API_KEY`
## 📋 Requirements

All dependencies are listed in `requirements_app.txt`:
- `openai>=1.0.0` - OpenAI SDK for API access
- `azure-ai-inference>=1.0.0` - Azure AI inference SDK
- `anthropic>=0.39.0` - Anthropic Claude API client
- `google-genai>=0.2.0` - Google Gemini API client
- `requests>=2.31.0` - HTTP library for image generation
- `python-dotenv>=1.0.0` - Environment variable management

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test modules
python -m unittest tests.test_claude_service -v
python -m unittest tests.test_gemini_service -v
python -m unittest tests.test_ai_orchestrator -v
```

Test coverage includes:
- ✅ 8 tests for Claude service
- ✅ 7 tests for Gemini service
- ✅ 12 tests for AI orchestrator
- ✅ Fallback mechanism verification
- ✅ Provider override testing

## 📚 Documentation

- **[API Integration Guide](docs/API_INTEGRATION.md)** - Complete guide to multi-provider setup
- **[Privacy Policy](docs/PRIVACY_POLICY.md)** - Privacy and data handling
- **[Store Publishing Guide](docs/STORE_PUBLISHING_GUIDE.md)** - Microsoft Store submission
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute

## 🔧 Building for Microsoft Store

```
ai-chatbot-project/
├── src/
│   ├── ai_chatbot.py              # Console version
│   ├── chatbot_gui.py             # Basic GUI version
### Building the Executable

```bash
python build_store_version.py
```

This will:
1. Load the embedded token from `.env`
2. Create a temporary build file with the token
3. Build a single-file EXE using PyInstaller
4. Clean up temporary files
5. Output: `dist/AI_Chatbot_Store.exe`

### Creating the MSIX Package

```bash
.\create_msix.ps1
```

The MSIX package will be created in the `msix/` folder, ready for Microsoft Store submission.

## 💰 Monetization

Version 1.2.0 includes Microsoft Store IAP integration:

- **Free Tier**: 15 chats/day, GPT-4o-mini model
- **Unlimited Unlock**: $0.99 one-time purchase
- **Premium Subscription**: $9.99/month with advanced models and image generation

Product IDs must match in Partner Center:
- `unlimited_unlock` - Durable purchase
- `premium_subscription` - Subscription

## 🔐 Privacy & Security

- **Local Storage**: All conversations stored locally in `%LOCALAPPDATA%/AI_Chatbot`
- **No Cloud Sync**: Your data never leaves your device
- **Secure Tokens**: API tokens embedded in build, not exposed in UI
- **Open Source**: Code is auditable on GitHub

See `docs/PRIVACY_POLICY.md` for full privacy policy.

## 📄 License

Copyright © 2025 Dorcas Innovations LLC

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for guidelines.

## 📞 Support

- **GitHub Issues**: [Create an issue](https://github.com/MMcBerry-bit/ai-chatbot-project/issues)
- **Documentation**: See `docs/` folder for detailed guides

## 🙏 Acknowledgments

- Powered by [GitHub Models](https://github.com/marketplace/models)
- Built with [OpenAI SDK](https://github.com/openai/openai-python)
- Image generation by [Pollinations.ai](https://pollinations.ai)
- Built with ❤️ using Python and Tkinter

---

**Version 1.2.0** | **Dorcas Innovations LLC** | **2025**
