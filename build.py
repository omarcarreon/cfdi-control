#!/usr/bin/env python3
"""
Build script for CFDI Control Application
Creates cross-platform executables using PyInstaller
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyInstaller"])
    
    try:
        import openpyxl
        print("✓ openpyxl is installed")
    except ImportError:
        print("✗ openpyxl not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openpyxl"])
    
    try:
        import lxml
        print("✓ lxml is installed")
    except ImportError:
        print("✗ lxml not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "lxml"])

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building CFDI Control Application...")
    
    # Get current platform
    system = platform.system()
    print(f"Platform: {system}")
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=CFDI_Control",
        "src/main.py"
    ]
    
    # Add platform-specific options
    if system == "Darwin":  # macOS
        cmd.extend(["--target-arch=universal2"])
        print("Building for macOS...")
    elif system == "Windows":
        print("Building for Windows...")
    else:
        print("Building for Linux...")
    
    # Run the build
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Build completed successfully!")
        print(f"Executable location: dist/CFDI_Control")
    else:
        print("✗ Build failed!")
        print("Error output:")
        print(result.stderr)
        return False
    
    return True

def main():
    """Main build function."""
    print("CFDI Control Application - Build Script")
    print("=" * 50)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    check_dependencies()
    
    # Build executable
    print("\n2. Building executable...")
    if build_executable():
        print("\n✓ Build process completed successfully!")
        print("\nNext steps:")
        print("1. Test the executable: ./dist/CFDI_Control")
        print("2. Distribute the executable to users")
    else:
        print("\n✗ Build process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 