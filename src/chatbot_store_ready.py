#!/usr/bin/env python3
"""
Store-Ready AI Chatbot
Version prepared for Microsoft Store submission
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import os
import sys
import json
import webbrowser
from pathlib import Path
from openai import OpenAI

class StoreReadyChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Chatbot - Store Edition")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # App data directory
        self.app_data_dir = Path.home() / "AppData" / "Local" / "AI_Chatbot"
        self.app_data_dir.mkdir(exist_ok=True)
        
        self.config_file = self.app_data_dir / "config.json"
        self.conversations_file = self.app_data_dir / "conversations.json"
        
        # Load configuration
        self.load_config()
        
        # Initialize chatbot backend
        self.setup_chatbot()
        self.setup_gui()
        
        # Load conversation history
        self.load_conversations()
        
    def load_config(self):
        """Load app configuration"""
        default_config = {
            "api_provider": "github",
            "github_token": "",
            "model": "openai/gpt-4.1-mini",
            "first_run": True,
            "theme": "default"
        }
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = {**default_config, **json.load(f)}
            else:
                self.config = default_config
                self.save_config()
        except:
            self.config = default_config
            
    def save_config(self):
        """Save app configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Failed to save config: {e}")
            
    def setup_chatbot(self):
        """Initialize the chatbot backend with better error handling"""
        self.endpoint = "https://models.github.ai/inference"
        self.model = self.config.get("model", "openai/gpt-4.1-mini")
        self.client = None
        
        # Try to get token from config or environment
        self.token = self.config.get("github_token") or os.environ.get("GITHUB_TOKEN")
        
        if self.token:
            try:
                self.client = OpenAI(
                    base_url=self.endpoint,
                    api_key=self.token,
                )
                self.connection_status = "Connected"
            except Exception as e:
                self.connection_status = f"Connection Error: {e}"
                self.client = None
        else:
            self.connection_status = "No API Token"
            
        # System message
        self.system_message = {
            "role": "system",
            "content": """You are a helpful, friendly AI assistant built for Windows. 
            Provide clear, concise responses. Keep conversations engaging and helpful."""
        }
        
        # Conversation history
        self.conversation_history = [self.system_message]
        
    def setup_gui(self):
        """Setup the enhanced GUI"""
        # Create menu bar
        self.create_menu()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Title and status
        title_label = ttk.Label(header_frame, text="🤖 AI Chatbot", font=("Segoe UI", 18, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        self.status_label = ttk.Label(
            header_frame,
            text=self.connection_status,
            font=("Segoe UI", 9),
            foreground="#666666"
        )
        self.status_label.grid(row=0, column=1, sticky=tk.E)
        
        # Chat display area with better styling
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#333333",
            state=tk.DISABLED,
            relief=tk.FLAT,
            borderwidth=1
        )
        self.chat_display.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="#0066cc", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("assistant", foreground="#009900", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("system", foreground="#666666", font=("Segoe UI", 10, "italic"))
        
        # Input frame with better layout
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Input field
        self.input_field = ttk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            width=70
        )
        self.input_field.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.input_field.bind('<Return>', self.on_send_message)
        self.input_field.bind('<Control-Return>', lambda e: self.input_field.insert(tk.INSERT, '\n'))
        
        # Button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=1)
        
        # Send button
        self.send_button = ttk.Button(
            button_frame,
            text="Send",
            command=self.on_send_message,
            width=8
        )
        self.send_button.grid(row=0, column=0, padx=(0, 5))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, pady=(0, 10))
        
        # Buttons
        ttk.Button(control_frame, text="🧹 Clear", command=self.clear_chat).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(control_frame, text="💾 Save", command=self.save_conversation).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(control_frame, text="⚙️ Settings", command=self.show_settings).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(control_frame, text="ℹ️ About", command=self.show_about).grid(row=0, column=3)
        
        # Show welcome message
        self.show_welcome_message()
        
        # Focus on input
        self.input_field.focus()
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Conversation", command=self.clear_chat, accelerator="Ctrl+N")
        file_menu.add_command(label="Save Conversation", command=self.save_conversation, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="API Configuration", command=self.show_settings)
        settings_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.clear_chat())
        self.root.bind('<Control-s>', lambda e: self.save_conversation())
        
    def show_welcome_message(self):
        """Show welcome message based on connection status"""
        if not self.client:
            if self.config.get("first_run", True):
                self.add_message("🔧 Setup Required", 
                               "Welcome to AI Chatbot! To get started, you'll need to configure your API settings.\n\n"
                               "Go to Settings → API Configuration to set up your GitHub token.\n\n"
                               "Need help? Check the About section for setup instructions.", 
                               "system")
                self.config["first_run"] = False
                self.save_config()
            else:
                self.add_message("⚠️ Not Connected", 
                               "API configuration required. Go to Settings → API Configuration to connect.", 
                               "system")
        else:
            self.add_message("🤖 AI Assistant", 
                           f"Hello! I'm ready to help. Connected to {self.model}.\n\n"
                           "Type your message below and press Enter to chat!", 
                           "assistant")
            
    def add_message(self, sender, message, tag="normal"):
        """Add a message to the chat display with styling"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Add message with styling
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}:\n", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Scroll to bottom
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def on_send_message(self, event=None):
        """Handle sending a message with better error handling"""
        message = self.input_field.get().strip()
        if not message:
            return
            
        # Check if connected
        if not self.client:
            messagebox.showwarning("Not Connected", 
                                 "Please configure your API settings first.\n\n"
                                 "Go to Settings → API Configuration.")
            return
            
        # Clear input field
        self.input_field.delete(0, tk.END)
        
        # Add user message to display
        self.add_message("👤 You", message, "user")
        
        # Disable send button while processing
        self.send_button.config(state='disabled')
        self.status_label.config(text="Thinking...")
        
        # Process in background thread
        threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
        
    def get_ai_response(self, user_message):
        """Get response from AI with enhanced error handling"""
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
            error_msg = f"Sorry, I encountered an error: {str(e)}\n\nPlease check your internet connection and API configuration."
            self.root.after(0, self.display_ai_response, error_msg)
    
    def display_ai_response(self, response):
        """Display AI response in main thread"""
        self.add_message("🤖 AI Assistant", response, "assistant")
        
        # Re-enable send button
        self.send_button.config(state='normal')
        self.status_label.config(text=self.connection_status)
        
        # Focus back to input
        self.input_field.focus()
        
    def clear_chat(self):
        """Clear the chat history"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Reset conversation history
        self.conversation_history = [self.system_message]
        
        # Show welcome message
        self.show_welcome_message()
        
    def save_conversation(self):
        """Save current conversation"""
        try:
            conversations = []
            if self.conversations_file.exists():
                with open(self.conversations_file, 'r') as f:
                    conversations = json.load(f)
            
            # Add current conversation
            import datetime
            conversation = {
                "timestamp": datetime.datetime.now().isoformat(),
                "messages": self.conversation_history[1:]  # Exclude system message
            }
            conversations.append(conversation)
            
            # Keep only last 50 conversations
            conversations = conversations[-50:]
            
            with open(self.conversations_file, 'w') as f:
                json.dump(conversations, f, indent=2)
                
            messagebox.showinfo("Saved", "Conversation saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save conversation: {e}")
            
    def load_conversations(self):
        """Load conversation history (for future features)"""
        pass  # Placeholder for conversation history feature
        
    def show_settings(self):
        """Show settings dialog"""
        SettingsDialog(self.root, self)
        
    def show_about(self):
        """Show about dialog"""
        about_text = """AI Chatbot - Store Edition
        
Version: 1.0.0
Created with: Python, tkinter, OpenAI API
Developer: Dorcas Innovations LLC

Features:
• Clean Windows-native interface
• GitHub Models integration
• Conversation history
• Keyboard shortcuts
• Persistent settings

Setup Instructions:
1. Get GitHub Personal Access Token:
   - Go to github.com/settings/tokens
   - Generate new token (classic)
   - Select appropriate permissions
   
2. Configure API Settings:
   - Go to Settings → API Configuration
   - Enter your GitHub token
   - Select preferred model

Support: Contact Dorcas Innovations LLC
Privacy Policy: Available upon request

© 2025 Dorcas Innovations LLC. All rights reserved."""
        
        messagebox.showinfo("About AI Chatbot", about_text)

class SettingsDialog:
    def __init__(self, parent, app):
        self.app = app
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("API Configuration")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+{}+{}".format(
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_dialog()
        
    def setup_dialog(self):
        """Setup the settings dialog"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="API Configuration", font=("Segoe UI", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)
        
        # GitHub Token
        ttk.Label(main_frame, text="GitHub Personal Access Token:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.token_var = tk.StringVar(value=self.app.config.get("github_token", ""))
        token_entry = ttk.Entry(main_frame, textvariable=self.token_var, width=60, show="*")
        token_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Help text
        help_text = ("Need a token? Click 'Get Token' to open GitHub's token creation page.\n"
                    "Generate a new token (classic) with appropriate permissions.")
        help_label = ttk.Label(main_frame, text=help_text, font=("Segoe UI", 9), foreground="#666666")
        help_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Get Token button
        ttk.Button(main_frame, text="Get Token", command=self.open_github_tokens).grid(row=4, column=0, sticky=tk.W, pady=(0, 20))
        
        # Model selection
        ttk.Label(main_frame, text="AI Model:").grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        self.model_var = tk.StringVar(value=self.app.config.get("model", "openai/gpt-4.1-mini"))
        model_combo = ttk.Combobox(main_frame, textvariable=self.model_var, width=57)
        model_combo['values'] = [
            "openai/gpt-4.1-mini",
            "openai/gpt-4.1",
            "openai/gpt-5-mini",
            "openai/gpt-5",
            "microsoft/phi-4-mini-instruct"
        ]
        model_combo.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Test Connection", command=self.test_connection).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Save", command=self.save_settings).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=2)
        
    def open_github_tokens(self):
        """Open GitHub tokens page"""
        webbrowser.open("https://github.com/settings/tokens")
        
    def test_connection(self):
        """Test the API connection"""
        token = self.token_var.get().strip()
        if not token:
            messagebox.showerror("Error", "Please enter your GitHub token first.")
            return
            
        try:
            # Test connection
            client = OpenAI(
                base_url="https://models.github.ai/inference",
                api_key=token,
            )
            
            # Simple test request
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model=self.model_var.get(),
                max_tokens=10
            )
            
            messagebox.showinfo("Success", "Connection test successful! ✅")
            
        except Exception as e:
            messagebox.showerror("Connection Failed", f"Failed to connect:\n\n{str(e)}")
            
    def save_settings(self):
        """Save the settings"""
        # Update app config
        self.app.config["github_token"] = self.token_var.get().strip()
        self.app.config["model"] = self.model_var.get()
        
        # Save to file
        self.app.save_config()
        
        # Reinitialize chatbot
        self.app.setup_chatbot()
        self.app.status_label.config(text=self.app.connection_status)
        
        # Show success and close
        messagebox.showinfo("Settings Saved", "Settings saved successfully! ✅")
        self.dialog.destroy()
        
        # Clear and show welcome message
        self.app.clear_chat()

def main():
    """Main function"""
    root = tk.Tk()
    
    # Set app icon (if available)
    try:
        # You can add an .ico file for the app icon
        root.iconbitmap('ai_chatbot.ico')
    except:
        pass
        
    # Create app
    app = StoreReadyChatbot(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit AI Chatbot?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the app
    root.mainloop()

if __name__ == "__main__":
    main()