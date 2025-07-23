#!/usr/bin/env python3
"""
CFDI Control Application - Main Entry Point
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point for the CFDI Control Application."""
    try:
        # Import and run the main application
        from gui.main_window import CFDIApplication
        
        app = CFDIApplication()
        app.run()
        
    except ImportError as e:
        print(f"Error al importar módulos requeridos: {e}")
        print("Por favor asegúrese de que todas las dependencias estén instaladas: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error de la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 