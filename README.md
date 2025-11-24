# AI Chatbot - Dorcas Innovations LLC

A professional AI chatbot application powered by GitHub Models API, available in multiple formats: console, GUI, and web applications.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## 🌟 Features

- **Multiple Interfaces**: Console, Desktop GUI (tkinter), and Web (Streamlit)
- **AI-Powered**: Uses OpenAI GPT-4.1-mini via GitHub Models
- **Microsoft Store Ready**: Professional version prepared for commercial distribution
- **Conversation History**: Maintains context across chat sessions
- **Customizable Settings**: Adjustable temperature and token limits
- **Persistent Storage**: Saves conversations and preferences locally

## 📦 Available Versions

### 1. Console Version (`src/ai_chatbot.py`)
Simple command-line interface for quick AI interactions.

```bash
python src/ai_chatbot.py
```

### 2. Desktop GUI (`src/chatbot_gui.py`)
Native Windows application with tkinter interface.

```bash
python src/chatbot_gui.py
```

### 3. Web Application (`src/chatbot_web.py`)
Modern web interface using Streamlit.

```bash
streamlit run src/chatbot_web.py
```

### 4. Store-Ready Version (`src/chatbot_store_ready.py`)
Enhanced version with professional features for Microsoft Store.

```bash
python src/chatbot_store_ready.py
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- GitHub Personal Access Token (for API access)
- Windows OS (for GUI versions)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-chatbot-project.git
   cd ai-chatbot-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements_app.txt
   ```

3. **Set up GitHub Token**
   ```bash
   # Windows PowerShell
   $env:GITHUB_TOKEN="your_github_token_here"
   
   # Or add to your environment variables permanently
   ```

4. **Run the application**
   ```bash
   # Console version
   python src/ai_chatbot.py
   
   # GUI version
   python src/chatbot_store_ready.py
   
   # Web version
   streamlit run src/chatbot_web.py
   ```

## 📋 Requirements

All dependencies are listed in `requirements_app.txt`:
- `openai>=1.0.0` - OpenAI SDK for API access
- `streamlit>=1.0.0` - Web application framework
- `pyinstaller>=6.0.0` - Executable builder

## 🏗️ Project Structure

```
ai-chatbot-project/
├── src/
│   ├── ai_chatbot.py              # Console version
│   ├── chatbot_gui.py             # Basic GUI version
│   ├── chatbot_web.py             # Streamlit web version
│   └── chatbot_store_ready.py     # Microsoft Store version
├── docs/
│   ├── APP_README.md              # Detailed app documentation
│   ├── STORE_PUBLISHING_GUIDE.md  # Microsoft Store guide
│   ├── STORE_SUBMISSION_CHECKLIST.md
│   └── PRIVACY_POLICY.md          # Privacy policy template
├── dist/                          # Built executables (gitignored)
├── build_for_store.py             # Build automation script
├── requirements_app.txt           # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🎨 Usage Examples

### Basic Chat
```
You: Hello, how are you?
AI: I'm doing well! How can I assist you today?
```

### Commands (Console Version)
- `exit` or `quit` - Exit the application
- `clear` - Clear conversation history
- `help` - Show available commands

## 🛠️ Building Standalone Executable

To create a standalone Windows executable:

```bash
python build_for_store.py
```

The executable will be created in the `dist/` folder.

## 📱 Microsoft Store Deployment

See `docs/STORE_PUBLISHING_GUIDE.md` for complete instructions on:
- Preparing MSIX package
- Creating app icons
- Submitting to Microsoft Store
- Pricing and monetization

## 🔐 Privacy & Security

- **No Data Collection**: All data stays on your local machine
- **API Security**: GitHub token stored locally in environment variables
- **Conversation Privacy**: Chats are processed via GitHub Models API
- See `docs/PRIVACY_POLICY.md` for full privacy policy

## 📄 License

Copyright © 2025 Dorcas Innovations LLC

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Bug Reports

Found a bug? Please open an issue on GitHub with:
- Detailed description
- Steps to reproduce
- Expected vs actual behavior
- System information

## 📞 Support

- **Email**: support@dorcasinnovations.com
- **GitHub Issues**: [Create an issue](https://github.com/YOUR_USERNAME/ai-chatbot-project/issues)
- **Documentation**: See `docs/` folder

## 🙏 Acknowledgments

- Powered by [GitHub Models](https://github.com/marketplace/models)
- Built with [OpenAI SDK](https://github.com/openai/openai-python)
- UI frameworks: tkinter, Streamlit

## 🗺️ Roadmap

- [ ] Add more AI model options
- [ ] Implement conversation export
- [ ] Add custom themes
- [ ] Cloud sync for conversations
- [ ] Mobile app versions
- [ ] Plugin system for extensions

---

**Made with ❤️ by Dorcas Innovations LLC**
