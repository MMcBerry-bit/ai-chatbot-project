#!/usr/bin/env python3
"""
AI Chatbot Web App using Streamlit
Modern web interface for the AI chatbot
"""

import streamlit as st
import os
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="🤖 AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        max-width: 800px;
        margin: 0 auto;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
    }
    .message-content {
        flex-grow: 1;
    }
    .message-avatar {
        font-size: 1.2rem;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Initialize the chatbot configuration"""
    if 'initialized' not in st.session_state:
        # Configuration
        st.session_state.endpoint = "https://models.github.ai/inference"
        st.session_state.model = "openai/gpt-4.1-mini"
        
        # Check for GitHub token
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            st.error("""
            **GITHUB_TOKEN environment variable is required!**
            
            Please set your GitHub Personal Access Token:
            1. Go to https://github.com/settings/tokens
            2. Generate a new token with appropriate permissions
            3. Set environment variable: `GITHUB_TOKEN=your_token`
            4. Restart this application
            """)
            st.stop()
        
        # Initialize OpenAI client
        st.session_state.client = OpenAI(
            base_url=st.session_state.endpoint,
            api_key=token,
        )
        
        # System message
        system_message = {
            "role": "system",
            "content": """You are a helpful, friendly AI assistant. You provide clear, 
            concise, and accurate responses. Keep responses conversational and helpful."""
        }
        
        # Initialize conversation history
        if 'messages' not in st.session_state:
            st.session_state.messages = [system_message]
        
        st.session_state.initialized = True

def display_chat_message(role, content):
    """Display a chat message with proper styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-avatar">👤</div>
            <div class="message-content">
                <strong>You:</strong><br>
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <strong>Assistant:</strong><br>
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

def get_ai_response(user_message):
    """Get response from AI"""
    try:
        # Add user message to conversation
        user_msg = {"role": "user", "content": user_message}
        st.session_state.messages.append(user_msg)
        
        # Get AI response
        with st.spinner("Thinking..."):
            response = st.session_state.client.chat.completions.create(
                messages=st.session_state.messages,
                temperature=0.7,
                top_p=0.95,
                max_tokens=500,
                model=st.session_state.model
            )
        
        # Extract and add assistant response
        ai_response = response.choices[0].message.content
        assistant_msg = {"role": "assistant", "content": ai_response}
        st.session_state.messages.append(assistant_msg)
        
        return ai_response
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def main():
    """Main Streamlit app"""
    # Initialize
    initialize_chatbot()
    
    # Header
    st.title("🤖 AI Chatbot")
    st.markdown(f"*Connected to GitHub Models ({st.session_state.model})*")
    
    # Sidebar with controls
    with st.sidebar:
        st.header("Controls")
        
        if st.button("🧹 Clear Chat"):
            # Reset to just system message
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()
        
        st.divider()
        
        st.header("Model Info")
        st.write(f"**Model:** {st.session_state.model}")
        st.write(f"**Endpoint:** GitHub Models")
        st.write(f"**Messages:** {len(st.session_state.messages) - 1}")  # Exclude system message
        
        st.divider()
        
        st.header("About")
        st.write("This is an AI chatbot powered by GitHub Models. Ask me anything!")
    
    # Display chat history (skip system message)
    st.subheader("💬 Chat")
    
    # Create container for chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages[1:]:  # Skip system message
            display_chat_message(message["role"], message["content"])
    
    # Chat input
    st.divider()
    
    # Input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Type your message here...",
            placeholder="Ask me anything!",
            key="user_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            send_button = st.form_submit_button("Send 📤")
        
    # Handle message sending
    if send_button and user_input.strip():
        # Display user message immediately
        display_chat_message("user", user_input)
        
        # Get and display AI response
        ai_response = get_ai_response(user_input)
        if ai_response:
            display_chat_message("assistant", ai_response)
        
        # Rerun to update the chat
        st.rerun()
    
    # Welcome message if no conversation yet
    if len(st.session_state.messages) == 1:
        st.info("👋 Hello! I'm your AI assistant. Type a message below to start our conversation!")

if __name__ == "__main__":
    main()