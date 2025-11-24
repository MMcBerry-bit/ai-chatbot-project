# Contributing to AI Chatbot

Thank you for your interest in contributing to AI Chatbot by Dorcas Innovations LLC!

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/YOUR_USERNAME/ai-chatbot-project/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Screenshots if applicable

### Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe the feature and its use case
3. Explain why it would be valuable

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add some AmazingFeature'`)
6. Push to your fork (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and small

### Testing

- Test all changes on Windows
- Verify all three versions work (console, GUI, web)
- Check that the executable builds correctly
- Test with different Python versions (3.13+)

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ai-chatbot-project.git
cd ai-chatbot-project

# Install dependencies
pip install -r requirements_app.txt

# Set up environment
set GITHUB_TOKEN=your_token_here

# Run tests
python src/ai_chatbot.py
python src/chatbot_store_ready.py
streamlit run src/chatbot_web.py
```

## Questions?

Feel free to ask questions in [Discussions](https://github.com/YOUR_USERNAME/ai-chatbot-project/discussions)

Thank you for contributing! 🎉
