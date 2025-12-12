"""
Authentication Window - Login and Registration
Handles user authentication for AI Chatbot
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import hashlib
from pathlib import Path

class AuthWindow:
    def __init__(self, app_data_dir, on_success_callback):
        self.app_data_dir = app_data_dir
        self.users_file = app_data_dir / "users.json"
        self.on_success = on_success_callback
        self.current_user = None
        
        # Create window
        self.window = tk.Tk()
        self.window.title("🤖 AI Chatbot - Login")
        self.window.geometry("450x550")
        self.window.configure(bg="#f0f0f0")
        self.window.resizable(False, False)
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.window.winfo_screenheight() // 2) - (550 // 2)
        self.window.geometry(f"450x550+{x}+{y}")
        
        # Load users database
        self.load_users()
        
        # Setup UI
        self.setup_ui()
        
    def load_users(self):
        """Load users from JSON file"""
        try:
            if self.users_file.exists():
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
                self.save_users()
        except Exception as e:
            print(f"Error loading users: {e}")
            self.users = {}
            
    def save_users(self):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
            
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def setup_ui(self):
        """Setup the authentication UI"""
        main_frame = ttk.Frame(self.window, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Title
        title_label = tk.Label(
            main_frame,
            text="🤖 AI Chatbot",
            font=("Segoe UI", 24, "bold"),
            bg="#f0f0f0",
            fg="#0066cc"
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Welcome! Please login or create an account",
            font=("Segoe UI", 10),
            bg="#f0f0f0",
            fg="#666666"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login/Register tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Login tab
        login_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(login_frame, text="Login")
        self.setup_login_tab(login_frame)
        
        # Register tab
        register_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(register_frame, text="Create Account")
        self.setup_register_tab(register_frame)
        
        # Footer
        footer_label = tk.Label(
            main_frame,
            text="© 2025 Dorcas Innovations LLC",
            font=("Segoe UI", 8),
            bg="#f0f0f0",
            fg="#999999"
        )
        footer_label.pack(side=tk.BOTTOM)
        
    def setup_login_tab(self, parent):
        """Setup login tab"""
        # Username
        ttk.Label(parent, text="Username:", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(10, 5))
        self.login_username = ttk.Entry(parent, font=("Segoe UI", 11), width=30)
        self.login_username.pack(fill=tk.X, pady=(0, 15))
        self.login_username.focus()
        
        # Password
        ttk.Label(parent, text="Password:", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.login_password = ttk.Entry(parent, font=("Segoe UI", 11), width=30, show="●")
        self.login_password.pack(fill=tk.X, pady=(0, 20))
        
        # Bind Enter key
        self.login_username.bind('<Return>', lambda e: self.login_password.focus())
        self.login_password.bind('<Return>', lambda e: self.do_login())
        
        # Login button
        login_btn = tk.Button(
            parent,
            text="Login",
            command=self.do_login,
            font=("Segoe UI", 12, "bold"),
            bg="#0066cc",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            pady=10
        )
        login_btn.pack(fill=tk.X, pady=(10, 10))
        
        # Info
        info_label = tk.Label(
            parent,
            text="Don't have an account? Switch to 'Create Account' tab",
            font=("Segoe UI", 9),
            fg="#666666"
        )
        info_label.pack(pady=(20, 0))
        
    def setup_register_tab(self, parent):
        """Setup registration tab"""
        # Username
        ttk.Label(parent, text="Username:", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(10, 5))
        self.reg_username = ttk.Entry(parent, font=("Segoe UI", 11), width=30)
        self.reg_username.pack(fill=tk.X, pady=(0, 15))
        
        # Email
        ttk.Label(parent, text="Email:", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.reg_email = ttk.Entry(parent, font=("Segoe UI", 11), width=30)
        self.reg_email.pack(fill=tk.X, pady=(0, 15))
        
        # Password
        ttk.Label(parent, text="Password:", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.reg_password = ttk.Entry(parent, font=("Segoe UI", 11), width=30, show="●")
        self.reg_password.pack(fill=tk.X, pady=(0, 15))
        
        # Confirm Password
        ttk.Label(parent, text="Confirm Password:", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.reg_confirm = ttk.Entry(parent, font=("Segoe UI", 11), width=30, show="●")
        self.reg_confirm.pack(fill=tk.X, pady=(0, 20))
        
        # Bind Enter key
        self.reg_username.bind('<Return>', lambda e: self.reg_email.focus())
        self.reg_email.bind('<Return>', lambda e: self.reg_password.focus())
        self.reg_password.bind('<Return>', lambda e: self.reg_confirm.focus())
        self.reg_confirm.bind('<Return>', lambda e: self.do_register())
        
        # Register button
        register_btn = tk.Button(
            parent,
            text="Create Account",
            command=self.do_register,
            font=("Segoe UI", 12, "bold"),
            bg="#009900",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            pady=10
        )
        register_btn.pack(fill=tk.X, pady=(10, 10))
        
    def do_login(self):
        """Handle login"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        # Check credentials
        if username not in self.users:
            messagebox.showerror("Error", "Username not found")
            return
            
        if self.users[username]['password'] != self.hash_password(password):
            messagebox.showerror("Error", "Incorrect password")
            return
            
        # Login successful - update last login
        import datetime
        self.users[username]['last_login'] = datetime.datetime.now().isoformat()
        self.save_users()
        
        self.current_user = username
        messagebox.showinfo("Success", f"Welcome back, {username}!")
        self.window.destroy()
        self.on_success(username)
        
    def do_register(self):
        """Handle registration"""
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        # Validation
        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return
            
        # Create account with metadata
        import datetime
        self.users[username] = {
            'password': self.hash_password(password),
            'email': email,
            'created_at': datetime.datetime.now().isoformat(),
            'last_login': None
        }
        self.save_users()
        
        messagebox.showinfo("Success", f"Account created successfully!\nWelcome, {username}!")
        self.current_user = username
        self.window.destroy()
        self.on_success(username)
        
    def run(self):
        """Run the authentication window"""
        self.window.mainloop()
        return self.current_user
