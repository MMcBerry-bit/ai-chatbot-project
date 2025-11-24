# Create EXE for Microsoft Store
# This script builds a standalone executable ready for Store packaging

import subprocess
import sys
import os
from pathlib import Path

def build_executable():
    """Build standalone executable using PyInstaller"""
    
    print("🚀 Building Store-Ready AI Chatbot EXE...")
    
    # PyInstaller command with all necessary options
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # Windows app (no console)
        "--name", "AI_Chatbot_Store",   # Output name
        "--clean",                      # Clean build
        "--noconfirm",                  # Overwrite without asking
        
        # Icon (if you have one)
        # "--icon=ai_chatbot.ico",
        
        # Add data files
        "--add-data", "docs/STORE_PUBLISHING_GUIDE.md;.",
        "--add-data", "docs/APP_README.md;.",
        
        # Hidden imports (in case of issues)
        "--hidden-import", "tkinter",
        "--hidden-import", "openai",
        
        # Exclude unnecessary packages
        "--exclude-module", "IPython",
        "--exclude-module", "jupyter",
        "--exclude-module", "notebook",
        
        # Optimize
        "--strip",                      # Remove debug symbols
        "--optimize", "2",              # Optimize bytecode
        
        # Main file
        "src/chatbot_store_ready.py"
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Build successful!")
        print(f"📁 EXE location: {Path.cwd() / 'dist' / 'AI_Chatbot_Store.exe'}")
        print("\n🎯 Next steps for Microsoft Store:")
        print("1. Test the EXE on a clean Windows system")
        print("2. Create MSIX package using Visual Studio")
        print("3. Submit to Microsoft Store")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_msix_config():
    """Create configuration for MSIX packaging"""
    
    msix_config = '''<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:mp="http://schemas.microsoft.com/appx/2014/phone/manifest"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10">
  
  <Identity Name="DorcasInnovations.AIChatbot"
            Publisher="CN=Dorcas Innovations LLC"
            Version="1.0.0.0" />
  
  <mp:PhoneIdentity PhoneProductId="your-guid-here" PhonePublisherId="00000000-0000-0000-0000-000000000000"/>
  
  <Properties>
    <DisplayName>AI Chatbot</DisplayName>
    <PublisherDisplayName>Dorcas Innovations LLC</PublisherDisplayName>
    <Logo>Assets\\StoreLogo.png</Logo>
    <Description>Intelligent AI chatbot powered by GitHub Models - by Dorcas Innovations LLC</Description>
  </Properties>
  
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Universal" MinVersion="10.0.17763.0" MaxVersionTested="10.0.19041.0" />
  </Dependencies>
  
  <Resources>
    <Resource Language="x-generate"/>
  </Resources>
  
  <Applications>
    <Application Id="App" Executable="AI_Chatbot_Store.exe" EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements
        DisplayName="AI Chatbot"
        Square150x150Logo="Assets\\Square150x150Logo.png"
        Square44x44Logo="Assets\\Square44x44Logo.png"
        Description="Intelligent AI chatbot for Windows"
        BackgroundColor="transparent">
        <uap:DefaultTile Wide310x150Logo="Assets\\Wide310x150Logo.png"/>
      </uap:VisualElements>
    </Application>
  </Applications>
  
  <Capabilities>
    <Capability Name="internetClient" />
  </Capabilities>
</Package>'''
    
    # Save MSIX config
    Path("Package.appxmanifest").write_text(msix_config)
    print("📄 Created Package.appxmanifest for MSIX packaging")

def main():
    """Main build process"""
    print("🏪 AI Chatbot - Microsoft Store Build Process")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    # Build executable
    if build_executable():
        # Create MSIX configuration
        create_msix_config()
        
        print("\n🎉 Build Complete!")
        print("\n📋 File Checklist:")
        print("✅ AI_Chatbot_Store.exe (in dist/ folder)")
        print("✅ Package.appxmanifest (for MSIX)")
        print("✅ Store publishing guides")
        
        print("\n🔧 Manual Steps Needed:")
        print("1. Create app icons (see icon requirements below)")
        print("2. Test EXE on clean Windows system") 
        print("3. Package as MSIX using Visual Studio")
        print("4. Create Microsoft Store listing")
        print("5. Submit for review")
        
        print("\n🖼️ Required Icon Sizes:")
        print("• Square44x44Logo.png (44x44)")
        print("• Square150x150Logo.png (150x150)")
        print("• Wide310x150Logo.png (310x150)")
        print("• StoreLogo.png (50x50)")
        
        return True
    else:
        print("❌ Build failed. Check errors above.")
        return False

if __name__ == "__main__":
    main()