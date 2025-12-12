# Microsoft Store In-App Purchase Setup Guide

## Overview

Your app now has **real Microsoft Store IAP integration** with automatic fallback to mock mode for development.

---

## ✅ What's Been Implemented

### 1. Real Windows Store Services Integration
- ✅ Uses `winrt.windows.services.store` APIs
- ✅ Async purchase requests
- ✅ License validation
- ✅ Subscription management
- ✅ Purchase restoration
- ✅ Automatic fallback to mock mode

### 2. Dual Mode Operation
- **Production Mode**: Real Store IAP when available
- **Development Mode**: Mock purchases for testing
- Seamless switching based on environment

### 3. Smart Detection
- Automatically detects if Windows Store Services are available
- Falls back gracefully if not in Store environment
- Clear console warnings about current mode

---

## 📦 Installation Steps

### Step 1: Install Windows Runtime Package

**Option A - Using pip (Recommended):**
```powershell
pip install winrt-Windows.Services.Store
```

**Option B - If that fails:**
```powershell
pip install winrt
```

### Step 2: Update Requirements File

Add to `requirements_app.txt`:
```
winrt-Windows.Services.Store>=1.0.0
```

### Step 3: Test the Installation

```powershell
python -c "from winrt.windows.services.store import StoreContext; print('Store API available!')"
```

If successful, you'll see: `Store API available!`

---

## 🏪 Microsoft Partner Center Configuration

### Step 1: Create IAP Products

1. Go to Partner Center: https://partner.microsoft.com/dashboard
2. Navigate to your app → **Add-ons**
3. Click **Create a new add-on**

### Step 2: Configure Unlimited Unlock

**Product details:**
- **Product ID**: `unlimited_unlock`
- **Product type**: Durable
- **Content type**: Digital content
- **Pricing**: $0.99 (Tier 2)
- **Markets**: Select all desired markets
- **Properties**:
  - Title: "Unlimited Chats"
  - Description: "Remove daily chat limits forever with one-time purchase"

### Step 3: Configure Premium Subscription

**Product details:**
- **Product ID**: `premium_subscription`
- **Product type**: Subscription
- **Subscription period**: Monthly (30 days)
- **Free trial**: Optional (7 days recommended)
- **Pricing**: $9.99/month
- **Markets**: Select all desired markets
- **Properties**:
  - Title: "Premium Subscription"
  - Description: "Unlimited chats + advanced AI models + image generation"
  - Recurrence: Every month
  - Auto-renew: Enabled

### Step 4: Update Product IDs in Code

If you chose different Product IDs, update `store_iap.py`:
```python
self.UNLIMITED_PRODUCT_ID = "your_unlimited_id"
self.PREMIUM_PRODUCT_ID = "your_premium_id"
```

---

## 🧪 Testing Your IAP

### Development Testing (Mock Mode)

While developing, the app runs in **mock mode**:
- No real payments
- Purchases are simulated
- Data saved locally
- Console shows: `"⚠️ Windows Store Services not available - running in mock mode"`

**To test:**
```powershell
python src/chatbot_store_ready.py
```
Click purchase buttons - they'll work without real payments.

### Sandbox Testing (Real Store API)

After packaging as MSIX and installing locally:

1. **Install your MSIX package**:
   ```powershell
   Add-AppxPackage -Path "msix\AI_Chatbot.msix"
   ```

2. **Run the installed app**

3. **Test purchases** (sandbox mode):
   - Uses real Store APIs
   - No real charges
   - Microsoft Account required
   - Purchases tracked by Store

### Production Testing

After Store submission and approval:
1. Download from Microsoft Store
2. Test with real Microsoft Account
3. Verify real payment processing
4. Check subscription renewal
5. Test purchase restoration

---

## 🔍 Verification Checklist

### Before MSIX Packaging:
- [ ] `winrt-Windows.Services.Store` installed
- [ ] Product IDs match Partner Center
- [ ] Code runs without errors
- [ ] Mock purchases work in development

### After MSIX Packaging:
- [ ] App installs successfully
- [ ] Store Context initializes
- [ ] Purchase dialogs appear
- [ ] License validation works

### In Partner Center:
- [ ] Add-on products created
- [ ] Pricing configured
- [ ] Markets selected
- [ ] Product descriptions complete
- [ ] Add-ons submitted for review

### After Store Approval:
- [ ] Real purchases work
- [ ] Payment processing succeeds
- [ ] Receipts are generated
- [ ] Subscriptions auto-renew
- [ ] Purchase restoration works

---

## 🐛 Troubleshooting

### "Store API not available" Error

**Cause**: App not running in Store context  
**Solutions**:
1. Install `winrt-Windows.Services.Store` package
2. Package as MSIX
3. Install MSIX locally for testing
4. Check Windows 10/11 version (needs 1809+)

### "StoreContext is None" Error

**Cause**: Store initialization failed  
**Solutions**:
1. Ensure app is packaged as MSIX
2. Check Package.appxmanifest has correct identity
3. Verify app is signed properly
4. Run from installed location, not IDE

### Purchase Dialog Doesn't Appear

**Causes**:
- Not signed into Microsoft Account
- No internet connection
- Product ID mismatch
- App not from Store

**Solutions**:
1. Sign into Windows with Microsoft Account
2. Check internet connection
3. Verify Product IDs match Partner Center
4. Install from Store or sideload signed MSIX

### Subscription Not Renewing

**Check**:
1. Partner Center subscription settings
2. Payment method on Microsoft Account
3. Subscription status in Store
4. License expiration dates

---

## 📱 How It Works

### Purchase Flow (Production)

```
User clicks purchase
    ↓
App calls purchase_unlimited() or purchase_premium()
    ↓
Checks if Store API available
    ↓
If YES: Calls Windows Store Services
    ↓
Microsoft Store shows payment dialog
    ↓
User completes payment
    ↓
Store returns purchase result
    ↓
App validates and saves locally
    ↓
Features unlocked
```

### Purchase Flow (Development)

```
User clicks purchase
    ↓
App calls purchase_unlimited() or purchase_premium()
    ↓
Checks if Store API available
    ↓
If NO: Uses mock purchase
    ↓
Simulates successful purchase
    ↓
Saves to local JSON
    ↓
Features unlocked (no payment)
```

---

## 🔐 Security Features

### Implemented:
- ✅ License validation from Microsoft Store
- ✅ Expiration checking for subscriptions
- ✅ Purchase restoration from Store
- ✅ Local data encryption (user directories)
- ✅ Secure async operations

### Microsoft Store Provides:
- ✅ Payment processing security
- ✅ Receipt generation
- ✅ Fraud prevention
- ✅ Refund handling
- ✅ Subscription management

---

## 💡 Best Practices

### 1. Always Validate Licenses
```python
# Refresh subscription status periodically
asyncio.run(store_iap._refresh_subscription_status())
```

### 2. Handle Network Errors
The code already includes try/catch blocks for all Store operations.

### 3. Test All Scenarios
- First purchase
- Already purchased
- Cancelled purchase
- Network failure
- Expired subscription
- Purchase restoration

### 4. Provide Clear Feedback
All callbacks return success/failure messages to show users.

### 5. Support Offline Mode
App gracefully handles when Store is unreachable.

---

## 📊 Pricing Strategy

### Current Configuration:
- **Free**: 15 chats/day
- **Unlimited**: $0.99 one-time
- **Premium**: $9.99/month

### Recommended Testing:
1. Start with conservative pricing
2. Monitor conversion rates
3. Adjust based on user feedback
4. Consider regional pricing
5. Run promotional pricing events

---

## 🚀 Launch Checklist

- [ ] Install `winrt-Windows.Services.Store`
- [ ] Test mock purchases work
- [ ] Create Partner Center add-ons
- [ ] Match Product IDs in code
- [ ] Build MSIX package
- [ ] Test MSIX installation
- [ ] Verify Store API initializes
- [ ] Test sandbox purchases
- [ ] Submit add-ons for review
- [ ] Submit app for review
- [ ] Test production purchases
- [ ] Monitor purchase metrics

---

## 📞 Support

**Questions?** Contact:
- **Email**: matthewmcberry@dorcasinnovationsllc.onmicrosoft.com
- **Partner Center Help**: https://partner.microsoft.com/support

**Resources**:
- Store Services API: https://docs.microsoft.com/windows/uwp/monetize/in-app-purchases-and-trials
- IAP Best Practices: https://docs.microsoft.com/windows/uwp/monetize/in-app-purchases-and-trials-using-the-windows-applicationmodel-store-namespace

---

**Status**: ✅ Real Microsoft Store IAP Ready!  
**Mode**: Dual (Production + Development)  
**Next Step**: Install WinRT package and test
