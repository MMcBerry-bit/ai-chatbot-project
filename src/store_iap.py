"""
Microsoft Store In-App Purchase Handler
Handles purchases for unlimited unlock and premium subscription

Requirements for production:
    pip install winrt-Windows.Services.Store
    
Note: This implementation uses real Windows Store Services APIs.
The app must be packaged as MSIX and submitted to Microsoft Store for IAP to work.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Try to import Windows Store Services
try:
    # For Windows 10/11 Store integration
    import asyncio
    from winrt.windows.services.store import (
        StoreContext,
        StorePurchaseStatus,
        StoreProductKind
    )
    STORE_API_AVAILABLE = True
except ImportError:
    STORE_API_AVAILABLE = False
    print("⚠️  Windows Store Services not available - running in mock mode")
    print("   Install with: pip install winrt-Windows.Services.Store")

class StoreIAP:
    def __init__(self, app_data_dir):
        self.app_data_dir = Path(app_data_dir)
        self.purchase_file = self.app_data_dir / "purchases.json"
        self.load_purchases()
        
        # Product IDs (must match Partner Center configuration)
        # TODO: Update these with your actual Store IDs after Partner Center setup
        self.UNLIMITED_PRODUCT_ID = "unlimited_unlock"
        self.PREMIUM_PRODUCT_ID = "premium_subscription"
        
        # Initialize Store context if available
        if STORE_API_AVAILABLE:
            try:
                self.store_context = StoreContext.get_default()
            except:
                self.store_context = None
                print("⚠️  Could not initialize Store Context - using mock mode")
        else:
            self.store_context = None
        
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
        Uses real Microsoft Store IAP if available
        """
        if STORE_API_AVAILABLE and self.store_context:
            # Real Store purchase
            asyncio.run(self._purchase_unlimited_async(callback))
        else:
            # Mock purchase for development
            self._mock_purchase_unlimited(callback)
    
    async def _purchase_unlimited_async(self, callback):
        """Async method for real Store purchase"""
        try:
            # Request purchase from Microsoft Store
            result = await self.store_context.request_purchase_async(self.UNLIMITED_PRODUCT_ID)
            
            if result.status == StorePurchaseStatus.SUCCEEDED:
                # Save purchase locally
                self.data["unlimited_unlocked"] = True
                self.data["purchases"].append({
                    "product_id": self.UNLIMITED_PRODUCT_ID,
                    "timestamp": datetime.now().isoformat(),
                    "price": "$0.99",
                    "status": "completed",
                    "store_id": result.store_id if hasattr(result, 'store_id') else None
                })
                self.save_purchases()
                
                if callback:
                    callback(True, "Purchase successful!")
                return True
                
            elif result.status == StorePurchaseStatus.ALREADY_PURCHASED:
                self.data["unlimited_unlocked"] = True
                self.save_purchases()
                if callback:
                    callback(True, "Already purchased!")
                return True
                
            elif result.status == StorePurchaseStatus.NOT_PURCHASED:
                if callback:
                    callback(False, "Purchase was cancelled")
                return False
                
            else:
                if callback:
                    callback(False, f"Purchase failed: {result.status}")
                return False
                
        except Exception as e:
            if callback:
                callback(False, f"Purchase error: {str(e)}")
            return False
    
    def _mock_purchase_unlimited(self, callback):
        """Mock purchase for development/testing"""
        try:
            self.data["unlimited_unlocked"] = True
            self.data["purchases"].append({
                "product_id": self.UNLIMITED_PRODUCT_ID,
                "timestamp": datetime.now().isoformat(),
                "price": "$0.99",
                "status": "completed (mock)",
                "note": "This is a mock purchase - no real payment"
            })
            self.save_purchases()
            
            if callback:
                callback(True, "Mock purchase successful! (Development mode)")
            return True
        except Exception as e:
            if callback:
                callback(False, f"Mock purchase failed: {str(e)}")
            return False
            
    def purchase_premium(self, callback=None):
        """
        Purchase premium subscription ($9.99/month)
        Uses real Microsoft Store IAP if available
        """
        if STORE_API_AVAILABLE and self.store_context:
            # Real Store purchase
            asyncio.run(self._purchase_premium_async(callback))
        else:
            # Mock purchase for development
            self._mock_purchase_premium(callback)
    
    async def _purchase_premium_async(self, callback):
        """Async method for real Store subscription purchase"""
        try:
            # Request subscription purchase from Microsoft Store
            result = await self.store_context.request_purchase_async(self.PREMIUM_PRODUCT_ID)
            
            if result.status == StorePurchaseStatus.SUCCEEDED:
                expiry = datetime.now() + timedelta(days=30)
                
                self.data["premium_active"] = True
                self.data["premium_expiry"] = expiry.isoformat()
                self.data["purchases"].append({
                    "product_id": self.PREMIUM_PRODUCT_ID,
                    "timestamp": datetime.now().isoformat(),
                    "price": "$9.99/month",
                    "status": "active",
                    "expiry": expiry.isoformat(),
                    "store_id": result.store_id if hasattr(result, 'store_id') else None
                })
                self.save_purchases()
                
                if callback:
                    callback(True, "Premium subscription activated!")
                return True
                
            elif result.status == StorePurchaseStatus.ALREADY_PURCHASED:
                # Check subscription status
                await self._refresh_subscription_status()
                if callback:
                    callback(True, "Subscription already active!")
                return True
                
            elif result.status == StorePurchaseStatus.NOT_PURCHASED:
                if callback:
                    callback(False, "Subscription was cancelled")
                return False
                
            else:
                if callback:
                    callback(False, f"Purchase failed: {result.status}")
                return False
                
        except Exception as e:
            if callback:
                callback(False, f"Purchase error: {str(e)}")
            return False
    
    def _mock_purchase_premium(self, callback):
        """Mock subscription purchase for development/testing"""
        try:
            expiry = datetime.now() + timedelta(days=30)
            
            self.data["premium_active"] = True
            self.data["premium_expiry"] = expiry.isoformat()
            self.data["purchases"].append({
                "product_id": self.PREMIUM_PRODUCT_ID,
                "timestamp": datetime.now().isoformat(),
                "price": "$9.99/month",
                "status": "active (mock)",
                "expiry": expiry.isoformat(),
                "note": "This is a mock subscription - no real payment"
            })
            self.save_purchases()
            
            if callback:
                callback(True, "Mock subscription activated! (Development mode)")
            return True
        except Exception as e:
            if callback:
                callback(False, f"Mock purchase failed: {str(e)}")
            return False
    
    async def _refresh_subscription_status(self):
        """Refresh subscription status from Store"""
        if not (STORE_API_AVAILABLE and self.store_context):
            return
        
        try:
            # Get app license from Store
            app_license = await self.store_context.get_app_license_async()
            
            # Check if premium subscription is in license
            if app_license and hasattr(app_license, 'add_on_licenses'):
                for addon_id, addon_license in app_license.add_on_licenses.items():
                    if addon_id == self.PREMIUM_PRODUCT_ID and addon_license.is_active:
                        # Update local data with Store info
                        expiry_date = addon_license.expiration_date
                        self.data["premium_active"] = True
                        self.data["premium_expiry"] = expiry_date.isoformat() if expiry_date else None
                        self.save_purchases()
                        return
            
            # Not found or expired
            self.data["premium_active"] = False
            self.save_purchases()
            
        except Exception as e:
            print(f"Error refreshing subscription: {e}")
            
    def restore_purchases(self):
        """
        Restore previous purchases from Microsoft Store
        Uses real Store license check if available
        """
        if STORE_API_AVAILABLE and self.store_context:
            asyncio.run(self._restore_purchases_async())
        else:
            # Load from local file only
            self.load_purchases()
        
        return self.data.get("purchases", [])
    
    async def _restore_purchases_async(self):
        """Async method to restore purchases from Store"""
        try:
            # Get app license from Microsoft Store
            app_license = await self.store_context.get_app_license_async()
            
            if not app_license:
                return
            
            # Check for unlimited unlock
            if hasattr(app_license, 'add_on_licenses'):
                for addon_id, addon_license in app_license.add_on_licenses.items():
                    if addon_id == self.UNLIMITED_PRODUCT_ID and addon_license.is_active:
                        self.data["unlimited_unlocked"] = True
                    
                    if addon_id == self.PREMIUM_PRODUCT_ID and addon_license.is_active:
                        expiry_date = addon_license.expiration_date
                        self.data["premium_active"] = True
                        self.data["premium_expiry"] = expiry_date.isoformat() if expiry_date else None
            
            self.save_purchases()
            
        except Exception as e:
            print(f"Error restoring purchases: {e}")
        
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
