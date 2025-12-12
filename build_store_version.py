"""
Build Script for Microsoft Store - With Embedded Token
This script builds the app with your token embedded for immediate use
"""

import subprocess
import os
import sys
from pathlib import Path

def build_for_store():
    """Build the app with embedded token for Microsoft Store"""
    
    print("🏪 Building AI Chatbot for Microsoft Store...")
    print("=" * 60)
    
    print("✅ Token already embedded in source code")
    
    # Use the main source file directly (token already embedded)
    print("\n📝 Using chatbot_store_ready.py (token already embedded)...")
    source_file = Path("src/chatbot_store_ready.py")
    
    print("\n📦 Building executable with PyInstaller...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "AI_Chatbot_Store",
        "--clean",
        "--noconfirm",
        
        # Add data files
        "--add-data", "docs/PRIVACY_POLICY.md;docs",
        
        # Hidden imports
        "--hidden-import", "tkinter",
        "--hidden-import", "openai",
        "--hidden-import", "dotenv",
        "--hidden-import", "winrt",
        "--hidden-import", "winrt.windows.services.store",
        
        # Exclude unnecessary
        "--exclude-module", "IPython",
        "--exclude-module", "jupyter",
        
        # Optimize
        "--strip",
        "--optimize", "2",
        
        # Main file (already has embedded token)
        str(source_file)
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        
        exe_path = Path("dist") / "AI_Chatbot_Store.exe"
        if exe_path.exists():
            print(f"\n📁 EXE created: {exe_path}")
            print(f"📊 Size: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        print("\n" + "=" * 60)
        print("🎉 Build Complete!")
        print("\n📋 Next Steps:")
        print("1. Test the EXE: dist\\AI_Chatbot_Store.exe")
        print("2. Verify the app works without any setup")
        print("3. Create MSIX package using create_msix.ps1")
        print("4. Submit to Microsoft Store")
        
        print("\n⚠️  IMPORTANT:")
        print("• The EXE contains your embedded token")
        print("• DO NOT share the EXE file publicly")
        print("• Only upload to Microsoft Store")
        print("• Monitor your GitHub token usage")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main function"""
    print("🚀 AI Chatbot - Microsoft Store Build Tool")
    print()
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    print()
    
    # Build
    if build_for_store():
        print("\n✅ Ready for Microsoft Store submission!")
    else:
        print("\n❌ Build failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
