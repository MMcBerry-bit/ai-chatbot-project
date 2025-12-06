# AI Chatbot - Version 1.2.0
### By Dorcas Innovations LLC

A professional AI chatbot application with premium features, powered by GitHub Models API and available on the Microsoft Store.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.2.0-brightgreen.svg)

## 🌟 Features

### Free Tier
- 15 AI-powered chats per day
- Access to GPT-4o-mini model
- Conversation history
- Clean, modern interface

### Unlimited Unlock ($0.99)
- Unlimited daily chats
- Access to GPT-4o-mini model
- No subscription required
- One-time purchase

### Premium Subscription ($9.99/month)
- Everything in Unlimited
- Access to advanced AI models:
  - GPT-4o
  - o1-preview
  - o1-mini
- AI Image Generation (powered by Pollinations.ai)
- Priority support

## 📦 Project Structure

### Core Application
- **`src/chatbot_store_ready.py`** - Main Microsoft Store application
- **`src/usage_tracker.py`** - Daily usage tracking and tier management
- **`src/store_iap.py`** - Microsoft Store in-app purchase handler
- **`src/premium_window.py`** - Premium features UI
- **`src/image_generator.py`** - AI image generation using Pollinations.ai

### Development Versions
- **`src/chatbot_gui.py`** - Basic desktop GUI version
- **`src/chatbot_web.py`** - Web interface using Streamlit

### Build Tools
- **`build_store_version.py`** - Build script for Microsoft Store
- **`create_msix.ps1`** - MSIX package creator

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- GitHub Personal Access Token (for API access)
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
   
   # Edit .env and add your GitHub token
   ```

4. **Run the application**
   ```bash
   python src/chatbot_store_ready.py
   ```

## 📋 Requirements

All dependencies are listed in `requirements_app.txt`:
- `openai>=1.0.0` - OpenAI SDK for API access
- `azure-ai-inference>=1.0.0` - Azure AI inference SDK
- `requests>=2.31.0` - HTTP library for image generation
- `python-dotenv>=1.0.0` - Environment variable management

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
