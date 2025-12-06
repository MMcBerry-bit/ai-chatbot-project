"""
Microsoft Store In-App Purchase Handler
Handles purchases for unlimited unlock and premium subscription
"""

import sys
import json
from pathlib import Path

# Note: For actual Microsoft Store IAP, you need the Windows Store Services SDK
# This is a simplified version for development/testing
# In production, you'll need to use Windows.Services.Store namespace

class StoreIAP:
    def __init__(self, app_data_dir):
        self.app_data_dir = Path(app_data_dir)
        self.purchase_file = self.app_data_dir / "purchases.json"
        self.load_purchases()
        
        # Product IDs (must match Partner Center configuration)
        self.UNLIMITED_PRODUCT_ID = "unlimited_unlock"
        self.PREMIUM_PRODUCT_ID = "premium_subscription"
        
    def load_purchases(self):
        """Load purchase history"""
        default_data = {
            "purchases": [],
            "unlimited_unlocked": False,
            "premium_active": False
        }
        
        try:
            if self.purchase_file.exists():
                with open(self.purchase_file, 'r') as f:
                    self.data = {**default_data, **json.load(f)}
            else:
                self.data = default_data
                self.save_purchases()
        except Exception as e:
            print(f"Error loading purchases: {e}")
            self.data = default_data
            
    def save_purchases(self):
        """Save purchase history"""
        try:
            with open(self.purchase_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving purchases: {e}")
            
    def purchase_unlimited(self, callback=None):
        """
        Purchase unlimited unlock ($0.99)
        In production, this will call Windows Store Services
        """
        try:
            # TODO: Replace with actual Microsoft Store IAP call
            # from Windows.Services.Store import StoreContext
            # context = StoreContext.GetDefault()
            # result = await context.RequestPurchaseAsync(self.UNLIMITED_PRODUCT_ID)
            
            # For development: simulate successful purchase
            self.data["unlimited_unlocked"] = True
            self.data["purchases"].append({
                "product_id": self.UNLIMITED_PRODUCT_ID,
                "timestamp": str(datetime.now().isoformat()),
                "price": "$0.99",
                "status": "completed"
            })
            self.save_purchases()
            
            if callback:
                callback(True, "Purchase successful!")
                
            return True
            
        except Exception as e:
            if callback:
                callback(False, f"Purchase failed: {str(e)}")
            return False
            
    def purchase_premium(self, callback=None):
        """
        Purchase premium subscription ($9.99/month)
        In production, this will call Windows Store Services
        """
        try:
            # TODO: Replace with actual Microsoft Store IAP call
            # This should handle subscription purchase
            
            # For development: simulate successful purchase
            from datetime import datetime, timedelta
            expiry = datetime.now() + timedelta(days=30)
            
            self.data["premium_active"] = True
            self.data["premium_expiry"] = expiry.isoformat()
            self.data["purchases"].append({
                "product_id": self.PREMIUM_PRODUCT_ID,
                "timestamp": str(datetime.now().isoformat()),
                "price": "$9.99/month",
                "status": "active",
                "expiry": expiry.isoformat()
            })
            self.save_purchases()
            
            if callback:
                callback(True, "Premium subscription activated!")
                
            return True
            
        except Exception as e:
            if callback:
                callback(False, f"Purchase failed: {str(e)}")
            return False
            
    def restore_purchases(self):
        """
        Restore previous purchases
        In production, this queries the Microsoft Store
        """
        # TODO: Implement actual restore from Microsoft Store
        # For now, just load from local file
        self.load_purchases()
        return self.data.get("purchases", [])
        
    def is_unlimited_purchased(self):
        """Check if unlimited unlock was purchased"""
        return self.data.get("unlimited_unlocked", False)
        
    def is_premium_active(self):
        """Check if premium subscription is active"""
        if not self.data.get("premium_active", False):
            return False
            
        # Check expiry
        from datetime import datetime
        expiry_str = self.data.get("premium_expiry")
        if not expiry_str:
            return False
            
        try:
            expiry = datetime.fromisoformat(expiry_str)
            if datetime.now() > expiry:
                self.data["premium_active"] = False
                self.save_purchases()
                return False
            return True
        except:
            return False


# Import datetime at module level
from datetime import datetime
