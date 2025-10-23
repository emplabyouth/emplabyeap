#!/usr/bin/env python3
"""
YEAP Dashboard - Quick Start Script (Python Version)
Usage: Run this script directly in your IDE, or execute 'python start_dashboard.py' in command line
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("=" * 50)
    print("YEAP Dashboard - Quick Start Script")
    print("=" * 50)
    print()

def check_environment():
    """Check runtime environment"""
    # Check if we're in the correct directory
    if not Path("orignaldata").exists():
        print("❌ Error: Please run this script from the project root directory")
        print(f"Current directory: {os.getcwd()}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check if streamlit_app.py exists in streamlit directory
    streamlit_app = Path("streamlit/streamlit_app.py")
    if not streamlit_app.exists():
        print("❌ Error: streamlit/streamlit_app.py not found")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("✅ Environment check passed")

def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import streamlit
        print("✅ Streamlit is installed")
        return True
    except ImportError:
        print("❌ Streamlit is not installed")
        print("Please install it using: pip install streamlit")
        return False

def start_streamlit():
    """Start the Streamlit application"""
    try:
        print("🚀 Starting Streamlit application...")
        print("📊 YEAP Dashboard will open in your browser shortly...")
        print("🔗 Local URL: http://localhost:8501")
        print("🌐 Network URL will be shown after startup")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Change to streamlit directory and run the app
        os.chdir("streamlit")
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Streamlit server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def main():
    """Main function"""
    print_banner()
    check_environment()
    
    if not check_dependencies():
        input("Press Enter to exit...")
        sys.exit(1)
    
    start_streamlit()

if __name__ == "__main__":
    main()