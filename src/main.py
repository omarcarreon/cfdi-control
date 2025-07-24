#!/usr/bin/env python3
"""
CFDI Control Application - Main Entry Point

This module serves as the main entry point for the CFDI Control Application.
It initializes the GUI application and handles any startup errors.

Author: CFDI Control Team
Version: 1.0.0
"""

import sys
import os
import logging
from pathlib import Path

# Configure logging for the application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cfdi_control.log'),
        logging.StreamHandler()
    ]
)

# Add src to Python path to ensure imports work correctly
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """
    Main entry point for the CFDI Control Application.
    
    This function:
    1. Initializes the GUI application
    2. Handles import errors gracefully
    3. Provides user-friendly error messages
    4. Sets up logging for debugging
    
    Raises:
        SystemExit: If the application fails to start or encounters critical errors
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting CFDI Control Application...")
        
        # Import and run the main application
        # Use absolute import to ensure it works in both development and executable
        import sys
        import os
        
        # Add the src directory to the path if it's not already there
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Try different import strategies
        try:
            from gui.main_window import CFDIApplication
        except ImportError:
            # If relative import fails, try absolute import
            try:
                from src.gui.main_window import CFDIApplication
            except ImportError:
                # Last resort: find the file in the PyInstaller bundle
                import importlib.util
                import sys
                
                # Look for the file in various possible locations
                possible_paths = [
                    os.path.join(current_dir, "gui", "main_window.py"),
                    os.path.join(current_dir, "src", "gui", "main_window.py"),
                    os.path.join(os.path.dirname(current_dir), "src", "gui", "main_window.py"),
                ]
                
                # Also check if we're in a PyInstaller bundle
                if getattr(sys, 'frozen', False):
                    # Running in a PyInstaller bundle
                    bundle_dir = sys._MEIPASS
                    possible_paths.append(os.path.join(bundle_dir, "src", "gui", "main_window.py"))
                    possible_paths.append(os.path.join(bundle_dir, "gui", "main_window.py"))
                
                main_window_path = None
                for path in possible_paths:
                    if os.path.exists(path):
                        main_window_path = path
                        break
                
                if main_window_path:
                    spec = importlib.util.spec_from_file_location("main_window", main_window_path)
                    main_window_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(main_window_module)
                    CFDIApplication = main_window_module.CFDIApplication
                else:
                    raise ImportError(f"Could not find main_window.py in any of these paths: {possible_paths}")
        
        # Initialize the application
        app = CFDIApplication()
        
        # Start the GUI event loop
        app.run()
        
        logger.info("Application started successfully")
        
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        print(f"Error al importar módulos requeridos: {e}")
        print("Por favor asegúrese de que todas las dependencias estén instaladas:")
        print("pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error de la aplicación: {e}")
        print("Consulte el archivo de log 'cfdi_control.log' para más detalles")
        sys.exit(1)

if __name__ == "__main__":
    main() 