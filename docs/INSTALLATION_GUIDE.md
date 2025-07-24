# Installation Guide - CFDI Control Application

## 📋 Overview

This guide provides step-by-step instructions for installing the CFDI Control Application on different platforms and environments.

## 🎯 Installation Options

### Option 1: Executable Installation (Recommended for End Users)
- **Windows**: Download and run `CFDI_Control.exe`
- **macOS**: Download and install `CFDI_Control.app`
- **Linux**: Download and run `CFDI_Control` binary

### Option 2: Source Code Installation (Recommended for Developers)
- Clone the repository
- Set up Python environment
- Install dependencies
- Run from source

## 🚀 Option 1: Executable Installation

### Windows Installation

#### Prerequisites
- Windows 10 or higher
- 4GB RAM minimum
- 100MB free disk space

#### Installation Steps
1. **Download the executable**
   - Go to the releases page
   - Download `CFDI_Control.exe` for Windows

2. **Run the installer**
   ```cmd
   # Double-click the downloaded file
   CFDI_Control.exe
   ```

3. **Follow installation wizard**
   - Accept the license agreement
   - Choose installation directory
   - Complete the installation

4. **Launch the application**
   - Find CFDI Control in Start Menu
   - Or run from desktop shortcut

#### Troubleshooting Windows
```cmd
# If the application doesn't start
# Check Windows Defender settings
# Add exception for CFDI_Control.exe

# If you get "Windows protected your PC" message
# Click "More info" → "Run anyway"
```

### macOS Installation

#### Prerequisites
- macOS 10.14 (Mojave) or higher
- 4GB RAM minimum
- 100MB free disk space

#### Installation Steps
1. **Download the application**
   - Go to the releases page
   - Download `CFDI_Control.app` for macOS

2. **Install the application**
   ```bash
   # Drag the .app file to Applications folder
   # Or double-click to install
   ```

3. **First run setup**
   ```bash
   # Right-click the app in Applications
   # Select "Open" to bypass Gatekeeper
   # Click "Open" in the security dialog
   ```

4. **Launch the application**
   - Find CFDI Control in Applications
   - Or use Spotlight (Cmd + Space)

#### Troubleshooting macOS
```bash
# If you get "unidentified developer" error
# Go to System Preferences → Security & Privacy
# Click "Open Anyway" for CFDI_Control

# If the app doesn't start
# Check Console.app for error messages
# Verify macOS version compatibility
```

### Linux Installation

#### Prerequisites
- Ubuntu 18.04+ or equivalent
- 4GB RAM minimum
- 100MB free disk space

#### Installation Steps
1. **Download the binary**
   ```bash
   # Download CFDI_Control binary
   wget https://github.com/user/cfdi_control/releases/latest/download/CFDI_Control
   ```

2. **Make executable**
   ```bash
   chmod +x CFDI_Control
   ```

3. **Run the application**
   ```bash
   ./CFDI_Control
   ```

4. **Create desktop shortcut (optional)**
   ```bash
   # Create desktop entry
   cat > ~/.local/share/applications/cfdi-control.desktop << EOF
   [Desktop Entry]
   Name=CFDI Control
   Exec=/path/to/CFDI_Control
   Icon=/path/to/icon.png
   Type=Application
   Categories=Office;
   EOF
   ```

## 🔧 Option 2: Source Code Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/user/cfdi_control.git
   cd cfdi_control
   ```

2. **Create virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python src/main.py
   ```

### Development Dependencies (Optional)
```bash
# Install development tools
pip install black flake8 pytest pytest-cov

# Install additional tools
pip install mypy pylint
```

## 🧪 Testing the Installation

### Test Basic Functionality
1. **Launch the application**
   - The main window should appear
   - Year/month dropdowns should be populated
   - File selection buttons should be functional

2. **Test file selection**
   - Click "Seleccionar Plantilla Excel"
   - Navigate to a test Excel file
   - Verify file selection works

3. **Test XML processing**
   - Click "Seleccionar Archivos XML"
   - Select test CFDI XML files
   - Verify file validation works

### Test with Sample Data
```bash
# Create test directory
mkdir test_data
cd test_data

# Create sample Excel template
# Create sample XML files
# Test the complete workflow
```

## 🔧 Configuration

### Application Settings
The application uses default settings that can be customized:

```python
# src/config/settings.py
class Settings:
    # Excel template settings
    HEADER_ROW = 3
    DATA_START_ROW = 4
    
    # CFDI mapping
    CFDI_MAPPING = {
        "cfdi:Comprobante/@Fecha": "B",
        # ... other mappings
    }
```

### Environment Variables (Optional)
```bash
# Set debug mode
export CFDI_DEBUG=1

# Set log level
export CFDI_LOG_LEVEL=INFO

# Set custom config path
export CFDI_CONFIG_PATH=/path/to/config.json
```

## 🚨 Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip list | grep -E "(openpyxl|lxml|tkinter)"

# Check system requirements
# Windows: Check Windows version
# macOS: Check macOS version
# Linux: Check distribution and dependencies
```

#### File Permission Issues
```bash
# Windows
# Run as Administrator

# macOS
# Check Gatekeeper settings
# System Preferences → Security & Privacy

# Linux
# Check file permissions
chmod +x CFDI_Control
```

#### Missing Dependencies
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check for missing system libraries
# Windows: Install Visual C++ Redistributable
# macOS: Install Xcode Command Line Tools
# Linux: Install python3-tk
```

#### GUI Issues
```python
# Test Tkinter installation
import tkinter as tk
root = tk.Tk()
root.destroy()
print("Tkinter is working")
```

### Platform-Specific Issues

#### Windows Issues
```cmd
# If you get "api-ms-win-core" errors
# Install Visual C++ Redistributable 2015-2022

# If PyInstaller executable doesn't work
# Try running with --debug flag
pyinstaller --debug=all cfdi_control.spec
```

#### macOS Issues
```bash
# If you get "notarization" warnings
# This is normal for non-Apple signed apps
# Click "Open Anyway" in Security & Privacy

# If the app crashes on startup
# Check Console.app for crash logs
# Verify macOS version compatibility
```

#### Linux Issues
```bash
# If you get "tkinter" errors
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo yum install tkinter         # CentOS/RHEL

# If you get "lib" errors
# Install required system libraries
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

## 📊 Performance Optimization

### System Requirements
- **Minimum**: 4GB RAM, 100MB disk space
- **Recommended**: 8GB RAM, 500MB disk space
- **Optimal**: 16GB RAM, 1GB disk space

### Performance Tips
```bash
# Close other applications during processing
# Use SSD storage for better I/O performance
# Ensure adequate free disk space
# Monitor system resources during processing
```

## 🔒 Security Considerations

### File Permissions
```bash
# Ensure proper file permissions
# Windows: Run as user (not Administrator for normal use)
# macOS: Grant necessary permissions when prompted
# Linux: Use appropriate user permissions
```

### Network Security
```bash
# The application doesn't require internet access
# Block network access if needed
# Use firewall rules for additional security
```

## 📞 Support

### Getting Help
1. **Check documentation**: Review this guide and other docs
2. **Check logs**: Look for error messages in application logs
3. **Test with sample data**: Verify with known good files
4. **Contact support**: Provide detailed error information

### Reporting Issues
When reporting issues, include:
- Operating system and version
- Application version
- Steps to reproduce the issue
- Error messages or logs
- Sample files (if possible)

---

*Last updated: [Current Date]*
*Installation Guide Version: 1.0* 