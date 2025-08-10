#!/usr/bin/env python3
"""
Setup script for CrisisSim MCP Server
This script helps users set up the environment and install dependencies.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def check_openai_key():
    """Check if OpenAI API key is set."""
    print("🔑 Checking OpenAI API key...")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API key found in environment variables!")
        return True
    else:
        print("⚠️  OpenAI API key not found in environment variables.")
        print("The server will use the hardcoded fallback key.")
        return True

def test_imports():
    """Test if all required modules can be imported."""
    print("🧪 Testing imports...")
    try:
        import openai
        import mcp
        print("✅ All required modules can be imported!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function."""
    print("🚨 CrisisSim MCP Server Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Check OpenAI key
    check_openai_key()
    
    print("\n" + "=" * 40)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the demo: python demo.py")
    print("2. Or run the server directly: python server.py")
    print("3. Check README.md for detailed usage instructions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
