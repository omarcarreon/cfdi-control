"""
Main window for CFDI Control Application
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import sys
import os
import threading
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our core modules
from core.xml_parser import CFDIXMLParser
from core.data_models import CFDIDataProcessor
from core.excel_processor import ExcelProcessor

class CFDIApplication:
    """Main application class for CFDI Control."""
    
    def __init__(self):
        """Initialize the main application window."""
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
        # Initialize processors
        self.xml_parser = CFDIXMLParser()
        self.data_processor = CFDIDataProcessor()
        self.excel_processor = ExcelProcessor()
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def setup_window(self):
        """Configure the main window properties."""
        self.root.title("Aplicación de Control CFDI")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Aplicación de Control CFDI", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Year and Month Selection
        ttk.Label(main_frame, text="Seleccionar Año y Mes:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Year selection
        year_frame = ttk.Frame(main_frame)
        year_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(year_frame, text="Año:").grid(row=0, column=0, padx=(0, 5))
        self.year_var = tk.StringVar(value="2025")
        year_combo = ttk.Combobox(year_frame, textvariable=self.year_var, 
                                  values=[str(year) for year in range(2020, 2031)], 
                                  width=10, state="readonly")
        year_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Month selection
        ttk.Label(year_frame, text="Mes:").grid(row=0, column=2, padx=(0, 5))
        self.month_var = tk.StringVar(value="")  # No default selection
        month_names = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        month_combo = ttk.Combobox(year_frame, textvariable=self.month_var,
                                   values=month_names, width=10, state="readonly")
        month_combo.grid(row=0, column=3)
        
        # File Selection Section
        ttk.Label(main_frame, text="Selección de Archivos:", font=("Arial", 12, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=(20, 5))
        
        # Excel Template Selection
        ttk.Label(main_frame, text="Plantilla Excel:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.excel_path_var = tk.StringVar()
        excel_frame = ttk.Frame(main_frame)
        excel_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(excel_frame, textvariable=self.excel_path_var, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(excel_frame, text="Examinar", command=self.select_excel_file).grid(row=0, column=1, padx=(5, 0))
        excel_frame.columnconfigure(0, weight=1)
        
        # XML Files Selection
        ttk.Label(main_frame, text="Archivos XML:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.xml_files_var = tk.StringVar(value="No se han seleccionado archivos")
        xml_frame = ttk.Frame(main_frame)
        xml_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(xml_frame, textvariable=self.xml_files_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(xml_frame, text="Seleccionar Archivos", command=self.select_xml_files).grid(row=0, column=1, padx=(5, 0))
        xml_frame.columnconfigure(0, weight=1)
        
        # Processing Section
        ttk.Label(main_frame, text="Procesamiento:", font=("Arial", 12, "bold")).grid(
            row=8, column=0, sticky=tk.W, pady=(20, 5))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Listo para procesar")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=10, column=0, columnspan=2, pady=5)
        
        # Process button (initially disabled)
        self.process_button = ttk.Button(main_frame, text="Procesar Archivos CFDI", 
                                        command=self.process_files, state="disabled")
        self.process_button.grid(row=11, column=0, columnspan=2, pady=10)
        
        # Open file location button (initially disabled)
        self.download_button = ttk.Button(main_frame, text="Abrir Ubicación del Archivo", 
                                         command=self.open_file_location, state="disabled")
        self.download_button.grid(row=12, column=0, columnspan=2, pady=5)
        
        # Store output file path
        self.output_file_path = None
        
        # Bind validation to year and month changes
        self.year_var.trace_add('write', self._validate_inputs)
        self.month_var.trace_add('write', self._validate_inputs)
        self.excel_path_var.trace_add('write', self._validate_inputs)
        
    def _process_files_worker(self, year: int, month: int):
        """
        Worker method to process files in background thread.
        
        Args:
            year: Selected year
            month: Selected month
        """
        try:
            excel_template = self.excel_path_var.get()
            xml_files = self.selected_xml_files
            
            # Update progress
            self.root.after(0, lambda: self.status_var.set("Validando plantilla Excel..."))
            self.root.after(0, lambda: self.progress_var.set(10))
            
            # Validate Excel template
            validation_result = self.excel_processor.validate_template_structure(excel_template)
            if not validation_result['valid']:
                error_msg = "Error en la plantilla Excel:\n" + "\n".join(validation_result['errors'])
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                self.root.after(0, self._reset_ui)
                return
            
            # Update progress
            self.root.after(0, lambda: self.status_var.set("Procesando archivos XML..."))
            self.root.after(0, lambda: self.progress_var.set(30))
            
            # Parse XML files
            raw_data_list = self.xml_parser.parse_multiple_files(xml_files)
            if not raw_data_list:
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudieron procesar los archivos XML."))
                self.root.after(0, self._reset_ui)
                return
            
            # Update progress
            self.root.after(0, lambda: self.status_var.set("Validando datos CFDI..."))
            self.root.after(0, lambda: self.progress_var.set(60))
            
            # Process and validate CFDI data
            processing_result = self.data_processor.process_raw_data(raw_data_list)
            
            # Update progress
            self.root.after(0, lambda: self.status_var.set("Llenando plantilla Excel..."))
            self.root.after(0, lambda: self.progress_var.set(80))
            
            # Fill Excel template
            excel_result = self.excel_processor.process_cfdi_to_excel(
                template_path=excel_template,
                cfdi_data_list=processing_result.processed_data,
                year=year,
                month=month
            )
            
            if not excel_result['success']:
                self.root.after(0, lambda: messagebox.showerror("Error", excel_result['error_message']))
                self.root.after(0, self._reset_ui)
                return
            
            # Update progress
            self.root.after(0, lambda: self.status_var.set("Completado"))
            self.root.after(0, lambda: self.progress_var.set(100))
            
            # Store output file path and enable download button
            self.output_file_path = excel_result['output_path']
            
            # Show success message
            success_msg = f"Procesamiento completado exitosamente!\n\n"
            success_msg += f"Archivos procesados: {processing_result.successful_files}\n"
            success_msg += f"Archivos con errores: {processing_result.failed_files}\n"
            success_msg += f"Registros llenados: {excel_result['records_processed']}\n"
            success_msg += f"Archivo de salida: {Path(excel_result['output_path']).name}\n\n"
            success_msg += f"Use el botón 'Abrir Ubicación del Archivo' para encontrar el archivo procesado."
            
            self.root.after(0, lambda: messagebox.showinfo("Éxito", success_msg))
            self.root.after(0, self._enable_download)
            self.root.after(0, self._reset_ui)
            
        except Exception as e:
            error_msg = f"Error inesperado durante el procesamiento: {str(e)}"
            self.logger.error(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            self.root.after(0, self._reset_ui)
    
    def _reset_ui(self):
        """Reset the UI to ready state."""
        self.process_button.config(state="normal")
        self.status_var.set("Listo para procesar")
        self.progress_var.set(0)
    
    def _enable_download(self):
        """Enable the download button."""
        self.download_button.config(state="normal")
    
    def _validate_inputs(self, *args):
        """Validate all inputs and enable/disable process button accordingly."""
        # Check if all required fields are filled
        year_selected = self.year_var.get().strip() != ""
        month_selected = self.month_var.get().strip() != ""
        excel_selected = self.excel_path_var.get().strip() != ""
        xml_selected = hasattr(self, 'selected_xml_files') and len(self.selected_xml_files) > 0
        
        # Enable process button only if all conditions are met
        if year_selected and month_selected and excel_selected and xml_selected:
            self.process_button.config(state="normal")
        else:
            self.process_button.config(state="disabled")
    
    def _validate_month_tab_exists(self, year: int, month: int) -> bool:
        """
        Validate that the selected month tab exists in the Excel template.
        
        Args:
            year: Selected year
            month: Selected month (1-12)
            
        Returns:
            True if month tab exists, False otherwise
        """
        try:
            excel_template = self.excel_path_var.get()
            
            # Load the Excel workbook
            workbook = self.excel_processor.load_template(excel_template)
            if not workbook:
                messagebox.showerror("Error", "No se pudo cargar la plantilla Excel.")
                return False
            
            # Try to find the month tab
            month_worksheet = self.excel_processor.find_month_tab(workbook, month, year)
            if not month_worksheet:
                # Get the expected tab name format
                expected_tab_name = self.excel_processor.get_month_tab_name(month, year)
                month_names = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                              "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                selected_month_name = month_names[month]
                
                error_msg = f"La pestaña '{selected_month_name}' no existe en la plantilla Excel.\n\n"
                error_msg += f"Se esperaba encontrar: '{expected_tab_name}'\n"
                error_msg += f"Pestañas disponibles: {', '.join(workbook.sheetnames)}\n\n"
                error_msg += f"Por favor seleccione un mes que exista en la plantilla."
                
                messagebox.showerror("Error", error_msg)
                return False
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar la plantilla Excel: {str(e)}")
            return False
    
    def open_file_location(self):
        """Open the file location in the system's file explorer."""
        if self.output_file_path and os.path.exists(self.output_file_path):
            try:
                import subprocess
                import platform
                
                system = platform.system()
                file_path = Path(self.output_file_path)
                
                if system == "Darwin":  # macOS
                    # Open folder and select the file in Finder
                    subprocess.run(["open", "-R", str(file_path)])
                elif system == "Windows":
                    # Open folder and select the file in Windows Explorer
                    subprocess.run(["explorer", "/select,", str(file_path)], shell=True)
                else:  # Linux
                    # Open folder in default file manager
                    subprocess.run(["xdg-open", str(file_path.parent)])
                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la ubicación del archivo: {str(e)}")
        else:
            messagebox.showerror("Error", "No hay archivo procesado disponible para descargar.")
        
    def select_excel_file(self):
        """Open file dialog to select Excel template."""
        filename = filedialog.askopenfilename(
            title="Seleccionar Plantilla Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.excel_path_var.set(filename)
            self._validate_inputs()  # Trigger validation
            
    def select_xml_files(self):
        """Open file dialog to select multiple XML files."""
        filenames = filedialog.askopenfilenames(
            title="Seleccionar Archivos XML",
            filetypes=[("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")]
        )
        if filenames:
            count = len(filenames)
            self.xml_files_var.set(f"{count} archivo(s) seleccionado(s)")
            self.selected_xml_files = filenames
        else:
            self.xml_files_var.set("No se han seleccionado archivos")
            self.selected_xml_files = []
        self._validate_inputs()  # Trigger validation
            
    def process_files(self):
        """Process the selected files."""
        # Validate inputs
        if not self.excel_path_var.get():
            messagebox.showerror("Error", "Por favor seleccione un archivo de plantilla Excel.")
            return
            
        if not hasattr(self, 'selected_xml_files') or not self.selected_xml_files:
            messagebox.showerror("Error", "Por favor seleccione archivos XML para procesar.")
            return
        
        # Get year and month
        if not self.year_var.get().strip() or not self.month_var.get().strip():
            messagebox.showerror("Error", "Por favor seleccione un año y mes válidos.")
            return
            
        try:
            year = int(self.year_var.get())
            # Convert month name to number
            month_name = self.month_var.get().strip()
            month_names = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                          "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            if month_name not in month_names:
                messagebox.showerror("Error", "Por favor seleccione un mes válido.")
                return
            month = month_names.index(month_name)
        except ValueError:
            messagebox.showerror("Error", "Por favor seleccione un año y mes válidos.")
            return
        
        # Validate that the selected month tab exists in the Excel file
        if not self._validate_month_tab_exists(year, month):
            return
        
        # Update UI
        self.process_button.config(state="disabled")
        self.download_button.config(state="disabled")
        self.status_var.set("Procesando archivos...")
        self.progress_var.set(0)
        
        # Start processing in a separate thread to avoid blocking the GUI
        processing_thread = threading.Thread(
            target=self._process_files_worker,
            args=(year, month)
        )
        processing_thread.daemon = True
        processing_thread.start()
        
    def run(self):
        """Start the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = CFDIApplication()
    app.run() 