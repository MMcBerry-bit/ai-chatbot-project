# GitHub Pages Deployment Guide

This guide explains how to deploy and use the AI Chatbot on GitHub Pages.

## Overview

The AI Chatbot includes a static web version that runs entirely in the browser using HTML, CSS, and JavaScript. This version can be hosted on GitHub Pages for free, providing instant access to the chatbot without any installation.

## Features of the GitHub Pages Version

- ✅ **No Server Required**: Runs completely in the browser
- ✅ **No Installation**: Access from any device with a web browser
- ✅ **Free Hosting**: GitHub Pages provides free hosting for static sites
- ✅ **Automatic Deployment**: Updates automatically via GitHub Actions
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile
- ✅ **Privacy Focused**: All data stored locally in browser
- ✅ **Persistent Storage**: Conversations and settings saved to localStorage
- ✅ **Export Functionality**: Download chat history as text file

## Architecture

The GitHub Pages version consists of three main files:

1. **`index.html`** - The HTML structure and UI components
2. **`styles.css`** - Modern, responsive styling
3. **`app.js`** - JavaScript logic for API calls and UI interactions

## How It Works

1. **User Configuration**: User provides their GitHub Personal Access Token via the settings panel
2. **Token Storage**: Token is stored securely in browser's localStorage
3. **API Communication**: When sending a message, the app makes a direct API call to GitHub Models
4. **Response Handling**: AI response is displayed and conversation history is maintained
5. **Persistence**: All conversations and settings are saved locally in the browser

## Deployment Steps

### Option 1: Automatic Deployment (Recommended)

The repository is already configured for automatic deployment:

1. **Push to Main Branch**:
   ```bash
   git push origin main
   ```

2. **GitHub Actions Workflow**: The `.github/workflows/deploy-pages.yml` workflow automatically:
   - Checks out the code
   - Configures GitHub Pages
   - Uploads the site files
   - Deploys to GitHub Pages

3. **Access Your Site**: 
   - Visit `https://YOUR_USERNAME.github.io/ai-chatbot-project/`
   - First deployment may take 2-3 minutes

### Option 2: Manual Deployment

If automatic deployment isn't working:

1. **Go to Repository Settings** > **Pages**
2. **Source**: Select "Deploy from a branch"
3. **Branch**: Select `main` branch and `/ (root)` folder
4. **Save**
5. **Wait for Deployment**: Check the Actions tab for deployment status

### Option 3: Deploy Your Own Fork

1. **Fork the Repository**:
   - Click "Fork" button on GitHub
   - This creates your own copy

2. **Enable GitHub Pages**:
   - Go to Settings > Pages in your fork
   - Source: Deploy from a branch
   - Branch: `main` / (root)
   - Click Save

3. **Access Your Deployment**:
   - `https://YOUR_USERNAME.github.io/ai-chatbot-project/`

## Using the Deployed App

### First-Time Setup

1. **Visit the Site**: Navigate to your GitHub Pages URL

2. **Open Settings**: Click the "⚙️ Settings" button

3. **Add GitHub Token**:
   - Go to [github.com/settings/tokens](https://github.com/settings/tokens)
   - Click "Generate new token (classic)"
   - No special scopes are needed for public models
   - Copy the token
   - Paste it in the settings panel
   - Click "Save Settings"

4. **Start Chatting**: Type a message and press Send!

### Features

- **Multiple AI Models**: Choose from GPT-4.1-mini, GPT-4o, Mistral, Llama, and more
- **Temperature Control**: Adjust response creativity (0-1)
- **Token Limits**: Control response length
- **Clear Chat**: Start fresh conversations
- **Export Chat**: Download conversation history

### Privacy & Security

- ✅ **Local Storage Only**: Your token and conversations stay in your browser
- ✅ **No Server**: No backend server that could log or store data
- ✅ **Direct API Calls**: Communication goes directly to GitHub's API
- ✅ **HTTPS**: All communication is encrypted
- ⚠️ **Token Security**: Keep your GitHub token private
- ⚠️ **Browser Storage**: Clearing browser data will erase conversations

## Customization

### Changing Colors

Edit `styles.css` and modify the CSS variables in the `:root` selector:

```css
:root {
    --primary-color: #2196f3;  /* Change primary color */
    --secondary-color: #4caf50; /* Change secondary color */
    /* ... more variables ... */
}
```

### Adding More Models

Edit `app.js` and add options to the model select dropdown:

```javascript
// In index.html, find the modelSelect options and add:
<option value="model-name">Model Display Name</option>
```

### Modifying System Prompt

Edit `app.js` and find the `getAIResponse` function:

```javascript
const messages = [
    {
        role: 'system',
        content: 'Your custom system prompt here...'
    }
];
```

## Troubleshooting

### Site Not Deploying

1. **Check Actions Tab**: Look for failed workflows
2. **Verify Permissions**: Settings > Actions > General > Workflow permissions should be "Read and write"
3. **Check Branch**: Ensure you're deploying from the correct branch

### API Errors

1. **Invalid Token**: Regenerate your GitHub token
2. **Rate Limits**: GitHub Models has usage limits
3. **Model Unavailable**: Try a different model from the dropdown

### Chat Not Saving

1. **Browser Storage**: Check if your browser allows localStorage
2. **Private Browsing**: localStorage may not persist in incognito/private mode
3. **Clear Cache**: Try clearing browser cache and reconfiguring

### Styling Issues

1. **Cache**: Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)
2. **Browser Compatibility**: Use a modern browser (Chrome, Firefox, Safari, Edge)

## GitHub Actions Workflow

The workflow file `.github/workflows/deploy-pages.yml` contains:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
  
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/deploy-pages@v4
```

## Performance Optimization

### Caching

The browser automatically caches static files (HTML, CSS, JS). To force updates:

1. Version your files: `styles.css?v=2`
2. Use cache busting: Add timestamps to file references
3. Configure cache headers in GitHub Pages settings

### Loading Speed

- All files are minified and optimized
- No external dependencies beyond GitHub Models API
- Responsive images and assets

## Limitations

- **No Backend**: Cannot store data server-side
- **GitHub Token Required**: Users must provide their own token
- **Rate Limits**: Subject to GitHub Models API rate limits
- **Browser-Only**: Cannot run server-side tasks
- **Public Repository**: GitHub Pages free tier requires public repos

## Advanced Configuration

### Custom Domain

1. **Add CNAME File**: Create a `CNAME` file with your domain
2. **Configure DNS**: Point your domain to GitHub Pages
3. **Settings**: Add custom domain in repository settings

### Analytics

Add analytics by including tracking code in `index.html`:

```html
<!-- Google Analytics example -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-ID"></script>
```

## Best Practices

1. **Regular Updates**: Keep dependencies and workflows updated
2. **Security**: Never commit tokens or secrets to the repository
3. **Testing**: Test changes locally before pushing to main
4. **Documentation**: Keep this guide updated with changes
5. **User Privacy**: Be transparent about data usage

## Support

For issues or questions:

- **GitHub Issues**: [Create an issue](https://github.com/MMcBerry-bit/ai-chatbot-project/issues)
- **Documentation**: Check `docs/` folder
- **Community**: Discussions tab on GitHub

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Made with ❤️ by Dorcas Innovations LLC**
