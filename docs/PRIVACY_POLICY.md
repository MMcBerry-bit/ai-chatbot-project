# Privacy Policy for AI Chatbot
**Dorcas Innovations LLC**

*Last Updated: November 10, 2026*

## Introduction

Dorcas Innovations LLC ("we," "our," or "us") operates the AI Chatbot application (the "Service"). This page informs you of our policies regarding the collection, use, and disclosure of personal data when you use our Service.

## Information We Collect

### User Account Information
- **Username**: Required for account creation and login
- **Email Address**: Collected during registration for account recovery and support
- **Password**: Stored as encrypted hash (SHA-256) for security
- **Account Metadata**: Creation date, last login time
- **User Preferences**: App settings and configuration data

### Chat and Usage Data
- **Conversation Data**: Saved conversations are stored locally in user-specific directories. Messages you send are transmitted to our backend service to generate a reply (see Third-Party Services)
- **Usage Statistics**: Daily chat count, subscription tier, purchase history
- **Configuration Settings**: AI model preferences, app customization

### Automatically Collected Information
- **Usage Data**: Information about how you use the app (anonymized)
- **Error Reports**: Technical information when the app encounters issues
- **Device Information**: Operating system version, app version for support purposes
- **Install Identifier**: A random ID generated on your device, sent with each request to apply daily usage limits
- **IP Address**: Received by our backend when the app connects, and used in hashed form to apply usage limits and prevent abuse
- **Purchase Verification**: If you buy an add-on, a Microsoft Store ID key is sent to our backend so we can confirm the purchase with Microsoft

## How We Use Your Information

- **Account Management**: To create, maintain, and authenticate your user account
- **Service Provision**: To enable AI chat functionality through our backend service and Microsoft Azure OpenAI Service
- **Subscription Management**: To track free tier limits and premium subscriptions
- **Data Segregation**: To keep your conversations and settings separate from other users
- **App Improvement**: To enhance features and fix bugs
- **Customer Support**: To provide technical assistance when requested
- **Legal Compliance**: To comply with applicable laws and regulations

## Data Storage and Security

### Local Storage (Primary)
- Account data and saved conversations are stored locally on your device
- User accounts stored in: `AppData/Local/AI_Chatbot/users.json`
- User-specific data in: `AppData/Local/AI_Chatbot/users/[username]/`
- Passwords are never stored in plain text (SHA-256 hashing)
- Chat messages are sent to our backend service only to generate a reply. Our backend does not keep the content of your conversations
- Each user's data is isolated in separate directories

### Third-Party Services
- **Dorcas Innovations backend (hosted on Microsoft Azure)**: Receives your messages, applies usage limits, and forwards them for AI processing
- **Microsoft Azure OpenAI Service**: Processes your messages to generate replies, under Microsoft's terms
- **Microsoft Privacy Statement**: https://privacy.microsoft.com/privacystatement
- **Microsoft Store**: Processes purchases and confirms add-on ownership
- **Pollinations.ai**: Receives your image prompts when you use image generation
- Our backend stores usage counters and purchase status, not the content of your conversations

### Security Measures
- All API communications use HTTPS encryption
- Passwords are hashed using SHA-256 encryption
- User data is isolated per account for privacy
- The app contains no API keys; the AI service key is held only on our backend
- Our backend receives your messages, install identifier and IP address as described above; your username, email and password are not sent to it

## Data Sharing

We do not sell, trade, or rent your personal information to third parties. Data is only shared:
- With Microsoft Azure OpenAI Service (for AI functionality)
- With Microsoft (to verify Store purchases)
- When required by law
- With your explicit consent

## Your Rights

You have the right to:
- **Access**: Request information about data we have about you
- **Correction**: Correct inaccurate personal information
- **Deletion**: Request deletion of your personal data
- **Portability**: Receive your data in a portable format
- **Objection**: Object to processing of your personal data

## Data Retention

- **User Accounts**: Stored locally until you delete your account or uninstall the app
- **Conversation Data**: Stored locally in your user directory until you delete them
- **Configuration Data**: Stored until you uninstall the app
- **Purchase History**: Maintained for subscription management and support
- **Login Sessions**: Active until you logout or close the app

## User Account Management

### Account Creation
- You create a local account with username, email, and password
- Account data is stored only on your local device
- No cloud synchronization (data does not sync across devices)

### Account Deletion
- You can delete your account by contacting support
- All associated data will be removed from your device
- This action cannot be undone

### Data Portability
- Your conversation history can be exported via the "Save Conversation" feature
- Account data is stored in standard JSON format for portability

## Children's Privacy

Our Service is not intended for children under 13. We do not knowingly collect personal information from children under 13. If you are a parent and believe your child has provided us with personal information, please contact us.

## International Data Transfers

Your data may be processed in countries other than your own when using our backend and Microsoft Azure services. We ensure appropriate safeguards are in place for such transfers.

## Changes to This Privacy Policy

We may update our Privacy Policy from time to time. We will notify you of any changes by:
- Posting the new Privacy Policy on this page
- Updating the "Last Updated" date
- Providing in-app notifications for significant changes

## Contact Information

**Dorcas Innovations LLC**

For questions about this Privacy Policy or our data practices:

- **Email**: matthewmcberry@dorcasinnovationsllc.onmicrosoft.com
- **Website**: https://mmcberry-bit.github.io/ai-chatbot-project/
- **GitHub**: https://github.com/MMcBerry-bit/ai-chatbot-project

## Legal Basis for Processing (GDPR)

If you are in the European Economic Area (EEA), our legal basis for collecting and using personal information includes:
- **Consent**: When you provide explicit consent
- **Contract**: When processing is necessary for service provision
- **Legitimate Interests**: For app improvement and customer support
- **Legal Obligation**: When required by law

## California Privacy Rights (CCPA)

California residents have additional rights including:
- Right to know what personal information is collected
- Right to delete personal information
- Right to opt-out of sale (we do not sell personal information)
- Right to non-discrimination for exercising privacy rights

---

**Effective Date**: November 24, 2025
**Company**: Dorcas Innovations LLC
**Contact**: matthewmcberry@dorcasinnovationsllc.onmicrosoft.com