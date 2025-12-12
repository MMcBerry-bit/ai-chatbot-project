#!/usr/bin/env python3
"""
Store-Ready AI Chatbot - Version 1.2.0
Premium Features with Microsoft Store IAP Integration
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

# Import our custom modules
from usage_tracker import UsageTracker
from store_iap import StoreIAP
from premium_window import PremiumWindow
from image_generator import ImageGenerator
from auth_window import AuthWindow
from watchdog import get_watchdog, OperationMonitor

class StoreReadyChatbot:
    def __init__(self, root, username):
        self.root = root
        self.root.title("🤖 AI Chatbot - Store Edition")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Store current user
        self.current_user = username
        
        # App data directory (shared)
        self.app_data_dir = Path.home() / "AppData" / "Local" / "AI_Chatbot"
        self.app_data_dir.mkdir(exist_ok=True)
        
        # User-specific data directory
        self.user_data_dir = self.app_data_dir / "users" / username
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.user_data_dir / "config.json"
        self.conversations_file = self.user_data_dir / "conversations.json"
        
        # Initialize usage tracking and IAP with user-specific data
        self.usage_tracker = UsageTracker(self.user_data_dir)
        self.store_iap = StoreIAP(self.user_data_dir)
        self.image_generator = ImageGenerator(self.user_data_dir)
        
        # Initialize watchdog
        self.watchdog = get_watchdog()
        self.watchdog.start(on_timeout=self.handle_watchdog_timeout)
        
        # Load configuration
        self.load_config()
        
        # Initialize chatbot backend
        self.setup_chatbot()
        self.setup_gui()
        
        # Start heartbeat mechanism
        self.start_heartbeat()
        
        # Load conversation history
        self.load_conversations()
        
    def load_config(self):
        """Load app configuration"""
        default_config = {
            "api_provider": "github",
            "github_token": "",
            "model": "gpt-4o-mini",
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
        self.endpoint = "https://models.inference.ai.azure.com"
        self.model = self.config.get("model", "gpt-4o-mini")
        self.client = None
        
        # EMBEDDED TOKEN
        embedded_token = "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"
        
        # Use embedded token
        self.token = embedded_token
        
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
        title_label = ttk.Label(header_frame, text=f"🤖 AI Chatbot - {self.current_user}", font=("Segoe UI", 18, "bold"))
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
        
        # Configure text tags for simple styling
        self.chat_display.tag_config("user", foreground="#0066cc", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("assistant", foreground="#009900", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("system", foreground="#666666", font=("Segoe UI", 10, "italic"))
        
        # Premium features frame (Model selector + Image button)
        self.premium_frame = ttk.Frame(main_frame)
        self.premium_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Model selector (for premium users)
        ttk.Label(self.premium_frame, text="AI Model:").pack(side=tk.LEFT, padx=(0, 5))
        self.model_var = tk.StringVar(value="gpt-4o-mini")
        self.model_selector = ttk.Combobox(
            self.premium_frame,
            textvariable=self.model_var,
            width=20,
            state='readonly'
        )
        self.model_selector['values'] = ["gpt-4o-mini"]  # Free users see only this
        self.model_selector.pack(side=tk.LEFT, padx=(0, 15))
        
        # Image generation button (for premium users)
        self.image_button = ttk.Button(
            self.premium_frame,
            text="🎨 Generate Image",
            command=self.generate_image,
            state='disabled'
        )
        self.image_button.pack(side=tk.LEFT)
        
        # Input frame with better layout
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
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
        control_frame.grid(row=4, column=0, pady=(0, 10))
        
        # Buttons
        ttk.Button(control_frame, text="🧹 Clear", command=self.clear_chat).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(control_frame, text="💾 Save", command=self.save_conversation).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(control_frame, text="ℹ️ About", command=self.show_about).grid(row=0, column=2, padx=(0, 10))
        
        # Premium button (highlighted)
        self.premium_button = tk.Button(
            control_frame,
            text="⭐ Unlock Premium",
            command=self.show_premium_window,
            bg="#FFD700",
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.premium_button.grid(row=0, column=3, padx=(10, 0))
        
        # Update status display
        self.update_status_display()
        
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
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")
        
        # Account menu
        account_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Account", menu=account_menu)
        account_menu.add_command(label="Profile", command=self.show_profile)
        account_menu.add_command(label="Logout", command=self.logout)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.clear_chat())
        self.root.bind('<Control-s>', lambda e: self.save_conversation())
        
    def show_welcome_message(self):
        """Show welcome message based on connection status"""
        if not self.client:
            self.add_message("🔧 Setup Required", 
                           "Welcome to AI Chatbot!\n\n"
                           "Unable to connect to AI service. This may be a temporary issue.\n\n"
                           "You can optionally add your own GitHub token in Settings → API Configuration for guaranteed access.", 
                           "system")
        else:
            welcome_msg = f"Hello! I'm ready to help. Connected to {self.model}.\n\n"
            if "Shared Token" in self.connection_status:
                welcome_msg += "You're using the shared AI service. For faster responses and no rate limits, you can add your own token in Settings.\n\n"
            welcome_msg += "Type your message below and press Enter to chat!"
            
            self.add_message("🤖 AI Assistant", welcome_msg, "assistant")
            
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
        
        # Scroll to bottom
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def on_send_message(self, event=None):
        """Handle sending a message with better error handling"""
        message = self.input_field.get().strip()
        if not message:
            return
            
        # Check usage limits
        if not self.usage_tracker.can_chat():
            self.show_limit_reached_popup()
            return
            
        # Check if connected
        if not self.client:
            response = messagebox.askyesno(
                "Not Connected", 
                "No API connection available.\n\n"
                "Would you like to configure your own GitHub token for guaranteed access?"
            )
            if response:
                self.show_settings()
            return
            
        # Clear input field
        self.input_field.delete(0, tk.END)
        
        # Add user message to display
        self.add_message("👤 You", message, "user")
        
        # Increment usage counter
        self.usage_tracker.increment_chat_count()
        self.update_status_display()
        
        # Disable send button while processing
        self.send_button.config(state='disabled')
        self.status_label.config(text="Thinking...")
        
        # Process in background thread
        threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
        
    def get_ai_response(self, user_message):
        """Get response from AI with enhanced error handling"""
        with OperationMonitor("AI Response", timeout_seconds=30):
            try:
                # Disable watchdog temporarily for long AI operation
                self.watchdog.disable_temporarily(duration_seconds=45)
                
                # Add user message to conversation history
                user_msg = {"role": "user", "content": user_message}
                self.conversation_history.append(user_msg)
                
                # Get the selected model (or use default)
                selected_model = self.model_var.get() if hasattr(self, 'model_var') else self.model
                
                # Get AI response
                response = self.client.chat.completions.create(
                    messages=self.conversation_history,
                    temperature=0.7,
                    top_p=0.95,
                    max_tokens=500,
                    model=selected_model
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
        
    def logout(self):
        """Logout current user and return to login screen"""
        response = messagebox.askyesno(
            "Logout",
            f"Are you sure you want to logout, {self.current_user}?"
        )
        if response:
            self.root.destroy()
            # Restart the app
            import subprocess
            subprocess.Popen([sys.executable, __file__])
    
    def show_profile(self):
        """Show user profile information"""
        # Get user info
        users_file = self.app_data_dir / "users.json"
        try:
            with open(users_file, 'r') as f:
                users = json.load(f)
                user_info = users.get(self.current_user, {})
        except:
            user_info = {}
        
        tier = self.usage_tracker.get_tier_name()
        status = self.usage_tracker.get_status_text()
        email = user_info.get('email', 'N/A')
        created = user_info.get('created_at', 'N/A')
        if created != 'N/A':
            from datetime import datetime
            created = datetime.fromisoformat(created).strftime("%B %d, %Y")
        
        profile_text = f"""User Profile

Username: {self.current_user}
Email: {email}
Account Created: {created}

Subscription Status:
Tier: {tier}
{status}

Data Location:
{self.user_data_dir}"""
        
        messagebox.showinfo("Profile", profile_text)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """AI Chatbot - Store Edition
        
Version: 1.2.0
Created with: Python, tkinter, OpenAI API
Developer: Dorcas Innovations LLC

Features:
• Works immediately - no setup required!
• Clean Windows-native interface
• GitHub Models AI integration
• Conversation history
• Keyboard shortcuts
• Premium features available

Using the App:
• Start chatting right away - fully configured!
• Access to GPT-4o-mini model
• Upgrade for advanced models and image generation

Support: Contact Dorcas Innovations LLC
Privacy Policy: Available upon request

© 2025 Dorcas Innovations LLC. All rights reserved."""
        
        messagebox.showinfo("About AI Chatbot", about_text)
    
    def update_status_display(self):
        """Update the status label with current tier and usage info"""
        status_text = self.usage_tracker.get_status_text()
        self.status_label.config(text=status_text)
        
        # Update premium button appearance based on tier
        tier = self.usage_tracker.get_tier_name()
        is_premium = self.usage_tracker.is_premium_active()
        
        if tier == "Premium Subscription":
            self.premium_button.config(
                text="⭐ Premium Active",
                bg="#32CD32"
            )
            # Enable premium features
            self.model_selector['values'] = ["gpt-4o-mini", "gpt-4o", "o1-preview", "o1-mini"]
            self.image_button.config(state='normal')
            
        elif tier == "Unlimited":
            self.premium_button.config(
                text="🔓 Unlimited Active",
                bg="#87CEEB"
            )
            # Unlimited users only get basic model
            self.model_selector['values'] = ["gpt-4o-mini"]
            self.image_button.config(state='disabled')
            
        else:
            self.premium_button.config(
                text="⭐ Unlock Premium",
                bg="#FFD700"
            )
            # Free users only get basic model
            self.model_selector['values'] = ["gpt-4o-mini"]
            self.image_button.config(state='disabled')
    
    def show_premium_window(self):
        """Show the premium features window"""
        PremiumWindow(self.root, self)
    
    def show_limit_reached_popup(self):
        """Show popup when daily limit is reached"""
        remaining = self.usage_tracker.get_remaining_chats()
        
        response = messagebox.askyesno(
            "Daily Limit Reached",
            f"You've used all {remaining} free chats today! 😊\n\n"
            f"Upgrade Options:\n"
            f"• Unlimited: $0.99 one-time - Unlimited chats with gpt-4o-mini\n"
            f"• Premium: $9.99/month - Multiple AI models + Image generation\n\n"
            f"Would you like to see premium options?",
            icon='warning'
        )
        
        if response:
            self.show_premium_window()
    
    def generate_image(self):
        """Generate an image using the input text"""
        prompt = self.input_field.get().strip()
        if not prompt:
            messagebox.showwarning("No Prompt", "Please enter a description for the image you want to generate.")
            return
        
        # Clear input
        self.input_field.delete(0, tk.END)
        
        # Show generating message
        self.add_message("🎨 Image Generator", f"Generating image: \"{prompt}\"...", "system")
        self.send_button.config(state='disabled')
        self.image_button.config(state='disabled')
        
        def on_complete(success, result):
            if success:
                self.add_message("🎨 Image Generator", 
                               f"✅ Image generated successfully!\n\nSaved to: {result}\n\n"
                               f"Opening image...", "system")
                # Open the image
                self.image_generator.open_image(result)
            else:
                self.add_message("🎨 Image Generator", 
                               f"❌ Failed to generate image:\n{result}", "system")
            
            self.send_button.config(state='normal')
            if self.usage_tracker.is_premium_active():
                self.image_button.config(state='normal')
        
        # Generate in background
        self.image_generator.generate_image(prompt, on_complete)

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
        
        self.model_var = tk.StringVar(value=self.app.config.get("model", "gpt-4o-mini"))
        model_combo = ttk.Combobox(main_frame, textvariable=self.model_var, width=57)
        model_combo['values'] = [
            "gpt-4o-mini",
            "gpt-4o",
            "o1-preview",
            "o1-mini"
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
                base_url="https://models.inference.ai.azure.com",
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
    
    def start_heartbeat(self):
        """Start regular heartbeat to watchdog"""
        def heartbeat_loop():
            self.watchdog.heartbeat()
            # Schedule next heartbeat in 2 seconds
            self.root.after(2000, heartbeat_loop)
        
        # Start the loop
        heartbeat_loop()
    
    def handle_watchdog_timeout(self, timeout_count):
        """
        Handle watchdog timeout - app may be hung
        
        Args:
            timeout_count: Number of consecutive timeouts
        """
        if timeout_count == 1:
            # First timeout - try to recover
            self.root.after(0, lambda: messagebox.showwarning(
                "Performance Issue",
                "The app appears to be slow or unresponsive. "
                "Please wait a moment for operations to complete."
            ))
        elif timeout_count == 3:
            # Multiple timeouts - offer restart
            self.root.after(0, lambda: self.offer_restart())
    
    def offer_restart(self):
        """Offer to restart the app if it's hung"""
        response = messagebox.askyesno(
            "App Not Responding",
            "The app appears to be hung. Would you like to restart it?\n\n"
            "Note: Any unsaved messages will be lost."
        )
        if response:
            # Stop watchdog
            self.watchdog.stop()
            # Restart app
            os.execv(sys.executable, ['python'] + sys.argv)


def main():
    """Main function"""
    # Get app data directory
    app_data_dir = Path.home() / "AppData" / "Local" / "AI_Chatbot"
    app_data_dir.mkdir(exist_ok=True)
    
    # Show authentication window first
    authenticated_user = [None]  # Use list to allow modification in nested function
    
    def on_auth_success(username):
        authenticated_user[0] = username
    
    auth_window = AuthWindow(app_data_dir, on_auth_success)
    auth_window.run()
    
    # Check if user authenticated
    if not authenticated_user[0]:
        return  # User closed auth window without logging in
    
    # Create main app window
    root = tk.Tk()
    
    # Set app icon (if available)
    try:
        # You can add an .ico file for the app icon
        root.iconbitmap('ai_chatbot.ico')
    except:
        pass
        
    # Create app with authenticated user
    app = StoreReadyChatbot(root, authenticated_user[0])
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit AI Chatbot?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the app
    root.mainloop()

if __name__ == "__main__":
    main()