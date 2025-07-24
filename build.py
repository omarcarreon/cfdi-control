#!/usr/bin/env python3
"""
Build script for CFDI Control Application
Creates cross-platform executables using PyInstaller
"""

import os
import sys
import platform
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

def check_dependencies():
    """Check if required dependencies are installed."""
    dependencies = [
        ("PyInstaller", "pyinstaller"),
        ("openpyxl", "openpyxl"),
        ("lxml", "lxml"),
        ("pandas", "pandas")
    ]
    
    for name, package in dependencies:
        try:
            __import__(package)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", package])

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            subprocess.run(["rm", "-rf", dir_name])
            print(f"✓ Cleaned {dir_name}")

def build_executable(target_platform=None):
    """Build the executable using PyInstaller."""
    print("Building CFDI Control Application...")
    
    # Get current platform if not specified
    if target_platform is None:
        system = platform.system()
    else:
        system = target_platform
    
    print(f"Target Platform: {system}")
    
    # Base build command - when using .spec file, just pass the spec file
    cmd = ["pyinstaller", "cfdi_control.spec"]
    
    # Platform-specific messages
    if system == "Darwin":  # macOS
        print("Building for macOS...")
    elif system == "Windows":
        print("Building for Windows...")
    else:
        print("Building for Linux...")
    
    # Run the build
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Build completed successfully!")
        
        # Get executable path
        if system == "Windows":
            exe_path = "dist/CFDI_Control.exe"
        elif system == "Darwin":
            # On macOS, PyInstaller creates a binary, not .app by default
            exe_path = "dist/CFDI_Control"
        else:
            exe_path = "dist/CFDI_Control"
        
        print(f"Executable location: {exe_path}")
        
        # Check file size
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"Executable size: {size:.1f} MB")
        
        return True
    else:
        print("✗ Build failed!")
        print("Error output:")
        print(result.stderr)
        return False

def test_executable():
    """Test the built executable."""
    print("Testing executable...")
    
    system = platform.system()
    if system == "Windows":
        exe_path = "dist/CFDI_Control.exe"
    elif system == "Darwin":
        exe_path = "dist/CFDI_Control"
    else:
        exe_path = "dist/CFDI_Control"
    
    if not os.path.exists(exe_path):
        print(f"✗ Executable not found: {exe_path}")
        return False
    
    print(f"✓ Executable found: {exe_path}")
    print("Note: Manual testing required for GUI applications")
    return True

def create_distribution_package():
    """Create distribution package with documentation."""
    print("Creating distribution package...")
    
    # Create distribution directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    system = platform.system()
    if system == "Windows":
        platform_name = "windows"
    elif system == "Darwin":
        platform_name = "macOS"
    else:
        platform_name = "ubuntu"
    
    dist_dir = f"CFDI_Control_{platform_name}_{timestamp}"
    
    if os.path.exists(dist_dir):
        subprocess.run(["rm", "-rf", dist_dir])
    
    os.makedirs(dist_dir)
    
    # Copy executable
    if system == "Windows":
        exe_name = "CFDI_Control.exe"
    else:
        exe_name = "CFDI_Control"
    
    if os.path.exists(f"dist/{exe_name}"):
        subprocess.run(["cp", f"dist/{exe_name}", dist_dir])
    
    # Copy documentation
    if os.path.exists("docs/USER_MANUAL.md"):
        subprocess.run(["cp", "docs/USER_MANUAL.md", dist_dir])
    
    # Copy README
    if os.path.exists("README.md"):
        subprocess.run(["cp", "README.md", dist_dir])
    
    # Create zip file
    zip_name = f"{dist_dir}.zip"
    if os.path.exists(zip_name):
        os.remove(zip_name)
    
    if system == "Windows":
        subprocess.run(["powershell", "Compress-Archive", "-Path", dist_dir, "-DestinationPath", zip_name])
    else:
        subprocess.run(["zip", "-r", zip_name, dist_dir])
    
    # Clean up temp directory
    subprocess.run(["rm", "-rf", dist_dir])
    
    print(f"✓ Distribution package created: {zip_name}")
    return zip_name

def create_install_script(dist_dir, system):
    """Create platform-specific installation script."""
    if system == "Windows":
        script_content = """@echo off
echo Installing CFDI Control Application...
echo.
echo This will install CFDI Control to your system.
echo.
pause
echo Installation complete!
pause
"""
        script_path = os.path.join(dist_dir, "install.bat")
    else:
        script_content = """#!/bin/bash
echo "Installing CFDI Control Application..."
echo ""
echo "This will install CFDI Control to your system."
echo ""
read -p "Press Enter to continue..."
echo "Installation complete!"
"""
        script_path = os.path.join(dist_dir, "install.sh")
        subprocess.run(["chmod", "+x", script_path])
    
    with open(script_path, "w") as f:
        f.write(script_content)

def main():
    """Main build function."""
    parser = argparse.ArgumentParser(description="Build CFDI Control Application")
    parser.add_argument("--platform", choices=["windows", "macos", "linux"], 
                       help="Target platform for build")
    parser.add_argument("--clean", action="store_true", 
                       help="Clean previous build artifacts")
    parser.add_argument("--test", action="store_true", 
                       help="Test the built executable")
    parser.add_argument("--package", action="store_true", 
                       help="Create distribution package")
    
    args = parser.parse_args()
    
    print("CFDI Control Application - Build Script")
    print("=" * 50)
    
    # Clean if requested
    if args.clean:
        clean_build()
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    check_dependencies()
    
    # Build executable
    print("\n2. Building executable...")
    target_platform = args.platform.upper() if args.platform else None
    if build_executable(target_platform):
        print("\n✓ Build process completed successfully!")
        
        # Test if requested
        if args.test:
            print("\n3. Testing executable...")
            test_executable()
        
        # Create package if requested
        if args.package:
            print("\n4. Creating distribution package...")
            dist_dir = create_distribution_package()
            print(f"\n✓ Distribution package ready: {dist_dir}")
        
        print("\nNext steps:")
        print("1. Test the executable manually")
        print("2. Distribute the executable to users")
        print("3. Create release on GitHub")
    else:
        print("\n✗ Build process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 