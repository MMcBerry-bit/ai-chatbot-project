"""
Usage Tracker for AI Chatbot
Tracks daily chat usage and premium status
"""

import json
from pathlib import Path
from datetime import datetime, date

class UsageTracker:
    def __init__(self, app_data_dir):
        self.app_data_dir = Path(app_data_dir)
        self.usage_file = self.app_data_dir / "usage.json"
        self.load_usage()
        
    def load_usage(self):
        """Load usage data from file"""
        default_data = {
            "last_reset": str(date.today()),
            "daily_count": 0,
            "total_chats": 0,
            "is_unlimited": False,
            "is_premium": False,
            "premium_expiry": None,
            "first_used": str(datetime.now().isoformat())
        }
        
        try:
            if self.usage_file.exists():
                with open(self.usage_file, 'r') as f:
                    self.data = {**default_data, **json.load(f)}
                    
                # Check if we need to reset daily count
                self._check_daily_reset()
            else:
                self.data = default_data
                self.save_usage()
        except Exception as e:
            print(f"Error loading usage: {e}")
            self.data = default_data
            
    def save_usage(self):
        """Save usage data to file"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving usage: {e}")
            
    def _check_daily_reset(self):
        """Reset daily count if it's a new day"""
        last_reset = self.data.get("last_reset", str(date.today()))
        if last_reset != str(date.today()):
            self.data["daily_count"] = 0
            self.data["last_reset"] = str(date.today())
            self.save_usage()
            
    def can_chat(self):
        """Check if user can send a chat message"""
        # Premium users have unlimited
        if self.is_premium_active():
            return True
            
        # Unlimited tier users have unlimited
        if self.data.get("is_unlimited", False):
            return True
            
        # Free users limited to 15 per day
        return self.data.get("daily_count", 0) < 15
        
    def get_remaining_chats(self):
        """Get number of remaining chats for free users"""
        if self.is_premium_active() or self.data.get("is_unlimited", False):
            return -1  # Unlimited
            
        return max(0, 15 - self.data.get("daily_count", 0))
        
    def increment_chat_count(self):
        """Increment chat counter"""
        self.data["daily_count"] = self.data.get("daily_count", 0) + 1
        self.data["total_chats"] = self.data.get("total_chats", 0) + 1
        self.save_usage()
        
    def unlock_unlimited(self):
        """Unlock unlimited chats (one-time purchase)"""
        self.data["is_unlimited"] = True
        self.save_usage()
        
    def activate_premium(self, days=30):
        """Activate premium subscription"""
        from datetime import timedelta
        expiry = datetime.now() + timedelta(days=days)
        self.data["is_premium"] = True
        self.data["premium_expiry"] = expiry.isoformat()
        self.save_usage()
        
    def is_premium_active(self):
        """Check if premium subscription is active"""
        if not self.data.get("is_premium", False):
            return False
            
        expiry_str = self.data.get("premium_expiry")
        if not expiry_str:
            return False
            
        try:
            expiry = datetime.fromisoformat(expiry_str)
            if datetime.now() > expiry:
                # Expired
                self.data["is_premium"] = False
                self.save_usage()
                return False
            return True
        except:
            return False
            
    def get_tier_name(self):
        """Get the user's current tier"""
        if self.is_premium_active():
            return "Premium Subscription"
        elif self.data.get("is_unlimited", False):
            return "Unlimited"
        else:
            return "Free"
            
    def get_status_text(self):
        """Get status text for display"""
        tier = self.get_tier_name()
        
        if self.is_premium_active():
            expiry = datetime.fromisoformat(self.data.get("premium_expiry"))
            days_left = (expiry - datetime.now()).days
            return f"{tier} ({days_left} days left)"
        elif self.data.get("is_unlimited", False):
            return f"{tier} - Unlimited Chats"
        else:
            remaining = self.get_remaining_chats()
            return f"{tier} - {remaining}/15 chats today"
