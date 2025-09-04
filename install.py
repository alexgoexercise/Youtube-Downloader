#!/usr/bin/env python3
"""
Installation script for YouTube Video & Audio Downloader
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    
    try:
        # Install yt-dlp
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp>=2023.12.30"])
        print("✅ yt-dlp installed successfully")
        
        # Verify installation
        import yt_dlp
        print(f"✅ yt-dlp version: {yt_dlp.version.__version__}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except ImportError as e:
        print(f"❌ Failed to import yt-dlp: {e}")
        return False

def test_application():
    """Test if the application can be imported"""
    try:
        from youtube_video_downloader import YouTubeDownloaderApp
        print("✅ Application can be imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import application: {e}")
        return False

def main():
    """Main installation process"""
    print("YouTube Video & Audio Downloader - Installation")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed. Please check your Python environment.")
        return False
    
    # Test application
    if not test_application():
        print("\n❌ Application test failed.")
        return False
    
    print("\n🎉 Installation completed successfully!")
    print("\nTo run the application:")
    print("python youtube_video_downloader.py")
    print("\nTo build an executable:")
    print("pip install pyinstaller")
    print("pyinstaller youtube_video_downloader.spec")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
