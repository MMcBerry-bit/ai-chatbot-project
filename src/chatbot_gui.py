#!/usr/bin/env python3
"""
AI Chatbot GUI Application for Windows
A desktop GUI version of the AI chatbot using tkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Chatbot")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize chatbot backend
        self.setup_chatbot()
        self.setup_gui()
        
    def setup_chatbot(self):
        """Initialize the chatbot backend"""
        self.endpoint = "https://models.inference.ai.azure.com"
        self.model = "gpt-4o-mini"
        
        # Get GitHub token from environment variable or use embedded token
        # For production builds, set EMBEDDED_TOKEN before building MSIX
        self.token = os.environ.get("GITHUB_TOKEN") or os.environ.get("EMBEDDED_TOKEN")
        
        if not self.token:
            messagebox.showerror(
                "Configuration Error", 
                "No API token found!\n\n"
                "This app requires configuration. Please contact support."
            )
            sys.exit(1)
        
        # Initialize OpenAI client
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )
        
        # System message
        self.system_message = {
            "role": "system",
            "content": """You are a helpful, friendly AI assistant. You provide clear, 
            concise, and accurate responses. Keep responses reasonably short for a chat interface."""
        }
        
        # Conversation history
        self.conversation_history = [self.system_message]
        
    def setup_gui(self):
        """Setup the GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🤖 AI Chatbot", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=70,
            height=25,
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#333333",
            state=tk.DISABLED
        )
        self.chat_display.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Input field
        self.input_field = ttk.Entry(
            input_frame,
            font=("Arial", 11),
            width=60
        )
        self.input_field.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.input_field.bind('<Return>', self.on_send_message)
        
        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.on_send_message
        )
        self.send_button.grid(row=0, column=1)
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        # Clear button
        clear_button = ttk.Button(
            control_frame,
            text="🧹 Clear Chat",
            command=self.clear_chat
        )
        clear_button.grid(row=0, column=0, padx=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            control_frame,
            text=f"Connected to GitHub Models ({self.model})",
            font=("Arial", 9),
            foreground="#666666"
        )
        self.status_label.grid(row=0, column=1)
        
        # Initial welcome message
        self.add_message("🤖 Assistant", "Hello! I'm your AI assistant. How can I help you today?", "#0066cc")
        
        # Focus on input field
        self.input_field.focus()
        
    def add_message(self, sender, message, color="#333333"):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add sender
        self.chat_display.insert(tk.END, f"{sender}: ", "sender")
        self.chat_display.tag_config("sender", foreground=color, font=("Arial", 10, "bold"))
        
        # Add message
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Scroll to bottom
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def on_send_message(self, event=None):
        """Handle sending a message"""
        message = self.input_field.get().strip()
        if not message:
            return
            
        # Clear input field
        self.input_field.delete(0, tk.END)
        
        # Add user message to display
        self.add_message("👤 You", message, "#008000")
        
        # Disable send button while processing
        self.send_button.config(state='disabled')
        self.status_label.config(text="Thinking...")
        
        # Process in background thread
        threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
        
    def get_ai_response(self, user_message):
        """Get response from AI in background thread"""
        try:
            # Add user message to conversation history
            user_msg = {"role": "user", "content": user_message}
            self.conversation_history.append(user_msg)
            
            # Get AI response
            response = self.client.chat.completions.create(
                messages=self.conversation_history,
                temperature=0.7,
                top_p=0.95,
                max_tokens=500,
                model=self.model
            )
            
            # Extract response
            ai_response = response.choices[0].message.content
            
            # Add to conversation history
            assistant_msg = {"role": "assistant", "content": ai_response}
            self.conversation_history.append(assistant_msg)
            
            # Update GUI in main thread
            self.root.after(0, self.display_ai_response, ai_response)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, self.display_ai_response, error_msg)
    
    def display_ai_response(self, response):
        """Display AI response in main thread"""
        self.add_message("🤖 Assistant", response, "#0066cc")
        
        # Re-enable send button
        self.send_button.config(state='normal')
        self.status_label.config(text=f"Connected to GitHub Models ({self.model})")
        
        # Focus back to input
        self.input_field.focus()
        
    def clear_chat(self):
        """Clear the chat history"""
        # Clear display
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Reset conversation history
        self.conversation_history = [self.system_message]
        
        # Add welcome message
        self.add_message("🤖 Assistant", "Chat cleared! How can I help you?", "#0066cc")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        root.iconbitmap('chatbot.ico')  # Add an icon file if you have one
    except:
        pass  # Ignore if no icon file
    
    # Create and run the app
    app = ChatbotGUI(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the chatbot?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()