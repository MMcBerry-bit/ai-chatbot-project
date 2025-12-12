"""
Premium Features Window
Allows users to purchase unlimited or premium subscription
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

class PremiumWindow:
    def __init__(self, parent, app):
        self.app = app
        
        # Create dialog window
        self.window = tk.Toplevel(parent)
        self.window.title("Unlock Premium Features")
        self.window.geometry("650x800")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.window.geometry("+{}+{}".format(
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the premium window UI"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = ttk.Label(
            main_frame, 
            text="🚀 Unlock Premium Features",
            font=("Segoe UI", 18, "bold")
        )
        header_label.pack(pady=(0, 10))
        
        # Current status
        status_frame = ttk.LabelFrame(main_frame, text="Current Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        current_tier = self.app.usage_tracker.get_tier_name()
        status_text = self.app.usage_tracker.get_status_text()
        
        ttk.Label(
            status_frame,
            text=f"Tier: {current_tier}",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            status_frame,
            text=status_text,
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, pady=(5, 0))
        
        # Free tier info
        free_frame = ttk.LabelFrame(main_frame, text="FREE", padding="15")
        free_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(free_frame, text="✓ 15 chats per day", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(free_frame, text="✓ GPT-4o-mini AI model", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(free_frame, text="✓ Basic chat features", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
        
        # Unlimited tier
        unlimited_frame = ttk.LabelFrame(main_frame, text="UNLIMITED - $0.99 (One-time)", padding="15")
        unlimited_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(unlimited_frame, text="✓ UNLIMITED chats daily", font=("Segoe UI", 10, "bold"), foreground="#0066cc").pack(anchor=tk.W, pady=2)
        ttk.Label(unlimited_frame, text="✓ GPT-4o-mini AI model", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(unlimited_frame, text="✓ No daily limits forever", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
        
        unlock_btn = ttk.Button(
            unlimited_frame,
            text="🔓 Unlock Unlimited - $0.99",
            command=self.purchase_unlimited,
            width=30
        )
        unlock_btn.pack(pady=(10, 0))
        
        # Premium tier
        premium_frame = ttk.LabelFrame(main_frame, text="PREMIUM - $9.99/month", padding="15")
        premium_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(premium_frame, text="✓ EVERYTHING in Unlimited, PLUS:", font=("Segoe UI", 10, "bold"), foreground="#009900").pack(anchor=tk.W, pady=2)
        ttk.Label(premium_frame, text="✓ Multiple AI models (GPT-4o, o1-preview, o1-mini)", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=2)
        ttk.Label(premium_frame, text="✓ AI Image generation (Pollinations.ai)", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=2)
        ttk.Label(premium_frame, text="✓ Priority support", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(premium_frame, text="✓ Early access to new features", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
        
        premium_btn = ttk.Button(
            premium_frame,
            text="⭐ Subscribe to Premium - $9.99/month",
            command=self.purchase_premium,
            width=40
        )
        premium_btn.pack(pady=(10, 0))
        
        # Restore purchases
        restore_frame = ttk.Frame(main_frame)
        restore_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Label(
            restore_frame,
            text="Already purchased?",
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT)
        
        restore_btn = ttk.Button(
            restore_frame,
            text="Restore Purchases",
            command=self.restore_purchases,
            width=20
        )
        restore_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Close button
        close_btn = ttk.Button(
            main_frame,
            text="Close",
            command=self.window.destroy,
            width=15
        )
        close_btn.pack(pady=(20, 0))
        
    def purchase_unlimited(self):
        """Handle unlimited unlock purchase"""
        if self.app.usage_tracker.data.get("is_unlimited", False):
            messagebox.showinfo("Already Unlocked", "You already have unlimited chats!")
            return
            
        response = messagebox.askyesno(
            "Confirm Purchase",
            "Purchase unlimited chats for $0.99?\n\n"
            "This is a one-time purchase that never expires."
        )
        
        if response:
            def on_purchase_complete(success, message):
                if success:
                    self.app.usage_tracker.unlock_unlimited()
                    self.app.update_status_display()
                    messagebox.showinfo("Success!", "🎉 Unlimited chats unlocked!\n\nYou can now chat without limits!")
                    self.window.destroy()
                else:
                    messagebox.showerror("Purchase Failed", message)
                    
            self.app.store_iap.purchase_unlimited(on_purchase_complete)
            
    def purchase_premium(self):
        """Handle premium subscription purchase"""
        if self.app.usage_tracker.is_premium_active():
            messagebox.showinfo("Already Subscribed", "You already have an active Premium subscription!")
            return
            
        response = messagebox.askyesno(
            "Confirm Subscription",
            "Subscribe to Premium for $9.99/month?\n\n"
            "Includes:\n"
            "• Multiple AI models (GPT-4o, o1, etc.)\n"
            "• Image generation\n"
            "• Unlimited chats\n\n"
            "Subscription renews monthly."
        )
        
        if response:
            def on_purchase_complete(success, message):
                if success:
                    self.app.usage_tracker.activate_premium(30)
                    self.app.update_status_display()
                    messagebox.showinfo("Success!", "🌟 Premium activated!\n\nEnjoy all premium features!")
                    self.window.destroy()
                else:
                    messagebox.showerror("Purchase Failed", message)
                    
            self.app.store_iap.purchase_premium(on_purchase_complete)
            
    def restore_purchases(self):
        """Restore previous purchases"""
        purchases = self.app.store_iap.restore_purchases()
        
        if self.app.store_iap.is_unlimited_purchased():
            self.app.usage_tracker.unlock_unlimited()
            
        if self.app.store_iap.is_premium_active():
            # Get expiry from IAP
            expiry_str = self.app.store_iap.data.get("premium_expiry")
            if expiry_str:
                from datetime import datetime
                expiry = datetime.fromisoformat(expiry_str)
                days = (expiry - datetime.now()).days
                self.app.usage_tracker.activate_premium(days)
                
        self.app.update_status_display()
        messagebox.showinfo("Restore Complete", "Purchases restored successfully!")
        self.window.destroy()
