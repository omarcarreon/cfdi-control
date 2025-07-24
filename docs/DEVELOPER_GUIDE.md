# Developer Guide - CFDI Control Application

## 📋 Project Overview

The CFDI Control Application is a desktop application built with Python 3.11+ that processes CFDI (Mexican electronic invoices) XML files and fills Excel control templates with extracted data.

### 🎯 Architecture
- **GUI Layer**: Tkinter-based desktop interface
- **Core Processing**: XML parsing and Excel manipulation
- **Data Layer**: CFDI data models and validation
- **Utilities**: Helper functions and configuration management

## 🏗️ Project Structure

```
cfdi_control/
├── src/                          # Main source code
│   ├── main.py                   # Application entry point
│   ├── gui/                      # GUI components
│   │   ├── main_window.py        # Main application window
│   │   └── components/           # Reusable GUI components
│   ├── core/                     # Core business logic
│   │   ├── xml_parser.py         # XML processing
│   │   ├── excel_processor.py    # Excel file handling
│   │   └── data_models.py        # Data structures
│   ├── utils/                    # Utility functions
│   │   ├── validators.py         # Data validation
│   │   └── helpers.py            # Helper functions
│   └── config/                   # Configuration
│       └── settings.py           # Application settings
├── tests/                        # Test suite
├── docs/                         # Documentation
├── resources/                     # Static resources
├── build.py                      # Build script
├── cfdi_control.spec            # PyInstaller spec
└── requirements.txt              # Dependencies
```

## 🚀 Development Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)
- Git

### Local Development Environment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cfdi_control
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python src/main.py
   ```

### Development Tools

#### Code Quality
- **Black**: Code formatting
- **flake8**: Linting
- **pytest**: Testing framework

#### IDE Configuration
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black"
}
```

## 📚 Core Components

### 1. Main Application (`src/main.py`)
Entry point that initializes the GUI application.

```python
def main():
    """Main entry point for the CFDI Control Application."""
    try:
        from gui.main_window import CFDIApplication
        app = CFDIApplication()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)
```

### 2. GUI Layer (`src/gui/`)
Tkinter-based user interface components.

#### Main Window (`src/gui/main_window.py`)
- Main application window
- Year/month selection
- File upload interfaces
- Progress indicators
- Results display

#### Components (`src/gui/components/`)
- Reusable GUI components
- Custom widgets
- Dialog boxes

### 3. Core Processing (`src/core/`)

#### XML Parser (`src/core/xml_parser.py`)
Handles CFDI XML file processing:

```python
class CFDIXMLParser:
    """Parser for CFDI XML files."""
    
    def __init__(self):
        self.mapping = CFDI_MAPPING
    
    def parse_file(self, file_path: str) -> Dict[str, str]:
        """Parse a single CFDI XML file."""
        
    def parse_files(self, file_paths: List[str]) -> List[Dict[str, str]]:
        """Parse multiple CFDI XML files."""
```

#### Excel Processor (`src/core/excel_processor.py`)
Handles Excel template manipulation:

```python
class ExcelProcessor:
    """Process Excel templates and fill with CFDI data."""
    
    def load_template(self, file_path: str) -> None:
        """Load Excel template file."""
        
    def fill_month_data(self, month: str, data: List[Dict[str, str]]) -> None:
        """Fill month tab with CFDI data."""
        
    def save_output(self, output_path: str) -> None:
        """Save filled template to output file."""
```

#### Data Models (`src/core/data_models.py`)
Defines data structures and validation:

```python
@dataclass
class CFDIData:
    """CFDI data structure."""
    fecha: str
    forma_pago: str
    subtotal: str
    # ... other fields
    
class CFDIValidator:
    """Validate CFDI data integrity."""
    
    def validate_xml_structure(self, xml_content: str) -> bool:
        """Validate XML structure."""
        
    def validate_data_completeness(self, data: CFDIData) -> bool:
        """Validate data completeness."""
```

### 4. Utilities (`src/utils/`)

#### Validators (`src/utils/validators.py`)
Data validation functions:

```python
def validate_excel_template(file_path: str) -> bool:
    """Validate Excel template structure."""
    
def validate_xml_files(file_paths: List[str]) -> List[str]:
    """Validate XML files and return valid ones."""
```

#### Helpers (`src/utils/helpers.py`)
Utility functions:

```python
def get_month_name(month_number: int) -> str:
    """Convert month number to Spanish name."""
    
def format_currency(amount: str) -> str:
    """Format currency values."""
```

### 5. Configuration (`src/config/`)

#### Settings (`src/config/settings.py`)
Application configuration:

```python
class Settings:
    """Application settings and configuration."""
    
    # CFDI to Excel column mapping
    CFDI_MAPPING = {
        "cfdi:Comprobante/@Fecha": "B",
        "cfdi:Comprobante/@FormaPago": "C",
        # ... other mappings
    }
    
    # Excel template settings
    HEADER_ROW = 3
    DATA_START_ROW = 4
    MONTH_NAMES = ["Enero", "Febrero", "Marzo", ...]
```

## 🔧 Data Flow

### 1. User Input Flow
```
User Selection → GUI Validation → File Processing → Data Extraction → Excel Filling → Output Generation
```

### 2. XML Processing Flow
```
XML File → Parse Structure → Extract Data → Validate → Map to Excel Columns
```

### 3. Excel Processing Flow
```
Template Load → Validate Structure → Clear Month Data → Fill New Data → Save Output
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_xml_parser.py

# Run with coverage
pytest --cov=src tests/
```

### Test Structure
```
tests/
├── test_xml_parser.py      # XML parsing tests
├── test_excel_processor.py # Excel processing tests
├── test_data_models.py     # Data model tests
├── test_integration.py     # Integration tests
└── test_data/              # Test data files
```

### Writing Tests
```python
import pytest
from src.core.xml_parser import CFDIXMLParser

class TestCFDIXMLParser:
    """Test XML parser functionality."""
    
    def test_parse_valid_xml(self):
        """Test parsing valid CFDI XML."""
        parser = CFDIXMLParser()
        data = parser.parse_file("tests/test_data/valid_cfdi.xml")
        assert data["fecha"] is not None
        
    def test_parse_invalid_xml(self):
        """Test parsing invalid XML."""
        parser = CFDIXMLParser()
        with pytest.raises(ValueError):
            parser.parse_file("tests/test_data/invalid.xml")
```

## 🚀 Building and Deployment

### Development Build
```bash
# Run build script
python build.py

# Or use PyInstaller directly
pyinstaller --onefile --windowed src/main.py --name CFDI_Control
```

### Production Build
```bash
# Build for specific platform
python build.py --platform windows
python build.py --platform macos
```

### Build Configuration
The `cfdi_control.spec` file contains PyInstaller configuration:

```python
# Hidden imports for PyInstaller
hiddenimports=[
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'openpyxl',
    'lxml',
    'pandas'
]
```

## 📊 Performance Considerations

### Memory Management
- Process XML files in batches
- Clear Excel data before filling
- Use generators for large file processing

### Error Handling
- Validate input files before processing
- Provide meaningful error messages
- Implement graceful degradation

### Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🔒 Security Considerations

### File Validation
- Validate XML structure before processing
- Check file extensions and content
- Implement file size limits

### Data Sanitization
- Sanitize extracted data before Excel insertion
- Validate currency and numeric values
- Handle special characters properly

## 📝 Code Style Guidelines

### Python Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all functions

### Naming Conventions
- Classes: PascalCase (`CFDIXMLParser`)
- Functions: snake_case (`parse_xml_file`)
- Constants: UPPER_CASE (`CFDI_MAPPING`)

### Documentation
- Inline comments for complex logic
- Docstrings for all public methods
- README files for each module

## 🐛 Debugging

### Common Issues

#### PyInstaller Issues
```bash
# Debug PyInstaller build
pyinstaller --debug=all cfdi_control.spec
```

#### GUI Issues
```python
# Enable Tkinter debugging
import tkinter as tk
tk._test()  # Test Tkinter installation
```

#### XML Parsing Issues
```python
# Debug XML parsing
import xml.etree.ElementTree as ET
tree = ET.parse('file.xml')
root = tree.getroot()
print(ET.tostring(root, encoding='unicode'))
```

## 📈 Future Enhancements

### Planned Features
- Multi-language support
- Advanced Excel templates
- Cloud storage integration
- Batch processing improvements
- Real-time validation

### Architecture Improvements
- Plugin system for custom processors
- Database integration for data persistence
- API integration for external services
- Advanced error reporting

---

*Last updated: [Current Date]*
*Developer Guide Version: 1.0* 