// AI Chatbot - JavaScript Application
// Client-side implementation for GitHub Pages

// Configuration
const CONFIG = {
    endpoint: 'https://models.inference.ai.azure.com',
    defaultModel: 'openai/gpt-4.1-mini',
    defaultTemperature: 0.7,
    defaultMaxTokens: 500
};

// Application State
let conversationHistory = [];
let settings = {
    token: '',
    model: CONFIG.defaultModel,
    temperature: CONFIG.defaultTemperature,
    maxTokens: CONFIG.defaultMaxTokens
};

// Initialize app on load
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    setupEventListeners();
    updateUI();
});

// Load settings from localStorage
function loadSettings() {
    const saved = localStorage.getItem('chatbotSettings');
    if (saved) {
        settings = JSON.parse(saved);
        document.getElementById('githubToken').value = settings.token || '';
        document.getElementById('modelSelect').value = settings.model || CONFIG.defaultModel;
        document.getElementById('temperature').value = settings.temperature || CONFIG.defaultTemperature;
        document.getElementById('maxTokens').value = settings.maxTokens || CONFIG.defaultMaxTokens;
        updateTempDisplay();
    }
    
    // Load conversation history
    const savedHistory = localStorage.getItem('conversationHistory');
    if (savedHistory) {
        conversationHistory = JSON.parse(savedHistory);
        displayConversationHistory();
    }
}

// Save settings to localStorage
function saveSettings() {
    settings.token = document.getElementById('githubToken').value.trim();
    settings.model = document.getElementById('modelSelect').value;
    settings.temperature = parseFloat(document.getElementById('temperature').value);
    settings.maxTokens = parseInt(document.getElementById('maxTokens').value);
    
    localStorage.setItem('chatbotSettings', JSON.stringify(settings));
    
    updateUI();
    toggleSettings();
    showStatus('Settings saved successfully!', 'ready');
}

// Setup event listeners
function setupEventListeners() {
    // Temperature slider
    document.getElementById('temperature').addEventListener('input', updateTempDisplay);
    
    // Enter key to send message
    document.getElementById('messageInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    document.getElementById('messageInput').addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 150) + 'px';
    });
}

// Update temperature display
function updateTempDisplay() {
    const temp = document.getElementById('temperature').value;
    document.getElementById('tempValue').textContent = temp;
}

// Toggle settings panel
function toggleSettings() {
    const panel = document.getElementById('settingsPanel');
    panel.classList.toggle('active');
}

// Update UI based on settings
function updateUI() {
    const hasToken = settings.token && settings.token.length > 0;
    const statusBar = document.getElementById('statusBar');
    const statusText = document.getElementById('statusText');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    
    if (hasToken) {
        statusText.textContent = `Ready! Using ${settings.model}`;
        statusBar.className = 'status-bar ready';
        messageInput.disabled = false;
        sendBtn.disabled = false;
    } else {
        statusText.textContent = 'Please configure your GitHub Token in Settings';
        statusBar.className = 'status-bar';
        messageInput.disabled = true;
        sendBtn.disabled = true;
    }
}

// Show status message
function showStatus(message, type = 'info') {
    const statusBar = document.getElementById('statusBar');
    const statusText = document.getElementById('statusText');
    
    statusText.textContent = message;
    statusBar.className = `status-bar ${type}`;
}

// Clear chat
function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        conversationHistory = [];
        localStorage.removeItem('conversationHistory');
        const chatContainer = document.getElementById('chatContainer');
        chatContainer.innerHTML = `
            <div class="welcome-message">
                <h2>👋 Chat Cleared!</h2>
                <p>Start a new conversation by typing a message below.</p>
            </div>
        `;
        showStatus('Chat history cleared', 'ready');
    }
}

// Export chat
function exportChat() {
    if (conversationHistory.length === 0) {
        alert('No conversation to export!');
        return;
    }
    
    const text = conversationHistory.map(msg => {
        const role = msg.role === 'user' ? 'You' : 'Assistant';
        const time = new Date(msg.timestamp).toLocaleString();
        return `[${time}] ${role}:\n${msg.content}\n`;
    }).join('\n');
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-export-${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showStatus('Chat exported successfully!', 'ready');
}

// Display conversation history
function displayConversationHistory() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.innerHTML = '';
    
    conversationHistory.forEach(msg => {
        if (msg.role !== 'system') {
            addMessageToUI(msg.role, msg.content, msg.timestamp);
        }
    });
    
    scrollToBottom();
}

// Add message to UI
function addMessageToUI(role, content, timestamp) {
    const chatContainer = document.getElementById('chatContainer');
    
    // Remove welcome message if it exists
    const welcome = chatContainer.querySelector('.welcome-message');
    if (welcome) {
        welcome.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    
    const avatar = role === 'user' ? '👤' : '🤖';
    const label = role === 'user' ? 'You' : 'Assistant';
    const time = timestamp ? new Date(timestamp).toLocaleTimeString() : new Date().toLocaleTimeString();
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <strong>${label}:</strong>
            <div class="message-text">${escapeHtml(content)}</div>
            <div class="message-timestamp">${time}</div>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Scroll to bottom of chat
function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Send message
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    if (!settings.token) {
        alert('Please configure your GitHub Token in Settings first!');
        toggleSettings();
        return;
    }
    
    // Disable input while processing
    messageInput.disabled = true;
    document.getElementById('sendBtn').disabled = true;
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Add user message to UI and history
    const userMessage = {
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
    };
    
    conversationHistory.push(userMessage);
    addMessageToUI('user', message);
    
    // Show loading state
    showStatus('AI is thinking...', 'info');
    
    try {
        // Get AI response
        const response = await getAIResponse(message);
        
        // Add assistant message
        const assistantMessage = {
            role: 'assistant',
            content: response,
            timestamp: new Date().toISOString()
        };
        
        conversationHistory.push(assistantMessage);
        addMessageToUI('assistant', response);
        
        // Save to localStorage
        localStorage.setItem('conversationHistory', JSON.stringify(conversationHistory));
        
        showStatus(`Ready! Using ${settings.model}`, 'ready');
        
    } catch (error) {
        console.error('Error:', error);
        showStatus(`Error: ${error.message}`, 'error');
        
        // Remove the user message if request failed
        conversationHistory.pop();
    } finally {
        // Re-enable input
        messageInput.disabled = false;
        document.getElementById('sendBtn').disabled = false;
        messageInput.focus();
    }
}

// Get AI response from GitHub Models
async function getAIResponse(userMessage) {
    // Build messages array for API
    const messages = [
        {
            role: 'system',
            content: 'You are a helpful, friendly AI assistant. You provide clear, concise, and accurate responses. Keep responses conversational and helpful.'
        }
    ];
    
    // Add recent conversation history (last 10 messages to avoid token limits)
    const recentHistory = conversationHistory.slice(-10);
    recentHistory.forEach(msg => {
        if (msg.role !== 'system') {
            messages.push({
                role: msg.role,
                content: msg.content
            });
        }
    });
    
    const requestBody = {
        messages: messages,
        temperature: settings.temperature,
        top_p: 0.95,
        max_tokens: settings.maxTokens,
        model: settings.model
    };
    
    const response = await fetch(`${CONFIG.endpoint}/chat/completions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${settings.token}`
        },
        body: JSON.stringify(requestBody)
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error?.message || `API request failed: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    
    if (!data.choices || data.choices.length === 0) {
        throw new Error('No response from AI');
    }
    
    return data.choices[0].message.content;
}

// Make functions globally available
window.toggleSettings = toggleSettings;
window.saveSettings = saveSettings;
window.sendMessage = sendMessage;
window.clearChat = clearChat;
window.exportChat = exportChat;
