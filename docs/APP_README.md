# AI Chatbot Windows Apps

## 🚀 Three Ways to Run Your AI Chatbot as a Windows App

### 1. 🖼️ GUI Desktop App (Recommended)
**File:** `chatbot_gui.py`

A native Windows desktop application with a clean, user-friendly interface.

**Features:**
- ✅ Clean Windows-style GUI
- ✅ Real-time chat interface
- ✅ Message history
- ✅ Clear chat button
- ✅ Status indicators
- ✅ Keyboard shortcuts (Enter to send)

**To Run:**
```bash
pip install -r requirements_app.txt
python chatbot_gui.py
```

### 2. 🌐 Web App (Modern)
**File:** `chatbot_web.py`

A modern web interface that runs in your browser.

**Features:**
- ✅ Modern web interface
- ✅ Responsive design
- ✅ Real-time chat
- ✅ Sidebar controls
- ✅ Message statistics
- ✅ Mobile-friendly

**To Run:**
```bash
pip install streamlit
streamlit run chatbot_web.py
```

Opens at `http://localhost:8501`

### 3. 📦 Standalone EXE (Distribution)
**Files:** Build from any Python file

Create a standalone executable that doesn't require Python installation.

**To Build:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed chatbot_gui.py
```

**Result:** `dist/chatbot_gui.exe` (self-contained)

## 🛠️ Quick Setup

### Install Dependencies
```bash
pip install -r requirements_app.txt
```

### Set GitHub Token (Required for all versions)
```powershell
$env:GITHUB_TOKEN="your_github_token_here"
```

### Try the GUI App
```bash
python chatbot_gui.py
```

### Try the Web App
```bash
streamlit run chatbot_web.py
```

## 📊 Comparison

| Feature | Console | GUI | Web | EXE |
|---------|---------|-----|-----|-----|
| Easy to Use | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Windows Native | ❌ | ✅ | ❌ | ✅ |
| No Python Required | ❌ | ❌ | ❌ | ✅ |
| Modern UI | ❌ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Easy Distribution | ❌ | ❌ | ❌ | ✅ |

## 🎯 Recommendations

- **For Personal Use**: GUI App (`chatbot_gui.py`)
- **For Modern UI**: Web App (`chatbot_web.py`)  
- **For Distribution**: Build EXE from GUI App
- **For Sharing**: Web App (easy to share URL)

## 🔧 Customization

All versions use the same backend, so you can:
- Change AI models
- Modify personality
- Add new features
- Customize appearance

## 🚨 Prerequisites

1. **GitHub Token**: Required for all versions
2. **Python 3.8+**: For running Python versions
3. **Internet Connection**: To access GitHub Models

Happy chatting! 🤖✨

---
**Developed by Dorcas Innovations LLC**  
© 2025 Dorcas Innovations LLC. All rights reserved.