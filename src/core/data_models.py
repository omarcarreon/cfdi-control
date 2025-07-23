"""
Data models for CFDI information
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

@dataclass
class CFDIData:
    """Data model for a single CFDI record."""
    
    # Basic invoice information
    fecha: str = ''                    # Date (Column B)
    forma_pago: str = ''               # Payment method (Column C)
    subtotal: str = ''                 # Subtotal (Column D)
    descuento: str = ''                # Discount (Column E)
    moneda: str = ''                   # Currency (Column F)
    total: str = ''                    # Total (Column G)
    tipo_comprobante: str = ''         # Document type (Column H)
    metodo_pago: str = ''              # Payment method (Column I)
    
    # Sender information
    emisor_rfc: str = ''               # Sender RFC (Column J)
    emisor_nombre: str = ''            # Sender name (Column K)
    emisor_regimen: str = ''           # Sender tax regime (Column L)
    
    # Receiver information
    receptor_rfc: str = ''             # Receiver RFC (Column M)
    receptor_nombre: str = ''          # Receiver name (Column N)
    receptor_regimen: str = ''         # Receiver tax regime (Column O)
    
    # Tax information
    total_impuestos: str = ''          # Total taxes (Column P)
    
    # File information
    file_path: str = ''                # Original file path
    file_name: str = ''                # Original file name
    
    def to_excel_row(self) -> Dict[str, str]:
        """Convert to Excel row format."""
        return {
            'B': self.fecha,
            'C': self.forma_pago,
            'D': self.subtotal,
            'E': self.descuento,
            'F': self.moneda,
            'G': self.total,
            'H': self.tipo_comprobante,
            'I': self.metodo_pago,
            'J': self.emisor_rfc,
            'K': self.emisor_nombre,
            'L': self.emisor_regimen,
            'M': self.receptor_rfc,
            'N': self.receptor_nombre,
            'O': self.receptor_regimen,
            'P': self.total_impuestos
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CFDIData':
        """Create CFDIData from dictionary."""
        return cls(
            fecha=data.get('B', ''),
            forma_pago=data.get('C', ''),
            subtotal=data.get('D', ''),
            descuento=data.get('E', ''),
            moneda=data.get('F', ''),
            total=data.get('G', ''),
            tipo_comprobante=data.get('H', ''),
            metodo_pago=data.get('I', ''),
            emisor_rfc=data.get('J', ''),
            emisor_nombre=data.get('K', ''),
            emisor_regimen=data.get('L', ''),
            receptor_rfc=data.get('M', ''),
            receptor_nombre=data.get('N', ''),
            receptor_regimen=data.get('O', ''),
            total_impuestos=data.get('P', ''),
            file_path=data.get('file_path', ''),
            file_name=data.get('file_name', '')
        )
    
    def validate(self) -> List[str]:
        """Validate the CFDI data and return list of errors."""
        errors = []
        
        # Required fields validation
        if not self.fecha:
            errors.append("Fecha es requerida")
        if not self.total:
            errors.append("Total es requerido")
        if not self.emisor_rfc:
            errors.append("RFC del emisor es requerido")
        if not self.receptor_rfc:
            errors.append("RFC del receptor es requerido")
        
        # Format validation
        try:
            if self.total and float(self.total) < 0:
                errors.append("Total no puede ser negativo")
        except ValueError:
            errors.append("Total debe ser un número válido")
        
        try:
            if self.subtotal and float(self.subtotal) < 0:
                errors.append("Subtotal no puede ser negativo")
        except ValueError:
            errors.append("Subtotal debe ser un número válido")
        
        return errors

@dataclass
class ProcessingResult:
    """Result of CFDI processing operation."""
    
    successful_files: int = 0
    failed_files: int = 0
    total_amount: float = 0.0
    currency: str = ''
    date_range: Dict[str, str] = None
    errors: List[str] = None
    processed_data: List[CFDIData] = None
    
    def __post_init__(self):
        if self.date_range is None:
            self.date_range = {'start': '', 'end': ''}
        if self.errors is None:
            self.errors = []
        if self.processed_data is None:
            self.processed_data = []
    
    def add_error(self, error: str):
        """Add an error to the result."""
        self.errors.append(error)
    
    def get_summary_text(self) -> str:
        """Get a human-readable summary of the processing result."""
        summary = f"Procesamiento completado:\n"
        summary += f"• Archivos procesados exitosamente: {self.successful_files}\n"
        summary += f"• Archivos con errores: {self.failed_files}\n"
        
        if self.total_amount > 0:
            summary += f"• Monto total: {self.total_amount:.2f} {self.currency}\n"
        
        if self.date_range['start'] and self.date_range['end']:
            summary += f"• Rango de fechas: {self.date_range['start']} - {self.date_range['end']}\n"
        
        if self.errors:
            summary += f"\nErrores encontrados:\n"
            for error in self.errors:
                summary += f"• {error}\n"
        
        return summary

class CFDIDataProcessor:
    """Processor for CFDI data with validation and transformation."""
    
    def __init__(self):
        """Initialize the CFDI data processor."""
        self.logger = logging.getLogger(__name__)
    
    def process_raw_data(self, raw_data_list: List[Dict[str, Any]]) -> ProcessingResult:
        """
        Process raw CFDI data into structured format.
        
        Args:
            raw_data_list: List of raw data dictionaries from XML parser
            
        Returns:
            ProcessingResult with processed data and statistics
        """
        result = ProcessingResult()
        processed_data = []
        
        for raw_data in raw_data_list:
            try:
                # Convert to CFDIData object
                cfdi_data = CFDIData.from_dict(raw_data)
                
                # Validate the data
                validation_errors = cfdi_data.validate()
                if validation_errors:
                    result.failed_files += 1
                    for error in validation_errors:
                        result.add_error(f"{cfdi_data.file_name}: {error}")
                    continue
                
                # Add to processed data
                processed_data.append(cfdi_data)
                result.successful_files += 1
                
                # Update statistics
                try:
                    if cfdi_data.total:
                        result.total_amount += float(cfdi_data.total)
                except ValueError:
                    pass
                
                if cfdi_data.moneda:
                    result.currency = cfdi_data.moneda
                
            except Exception as e:
                result.failed_files += 1
                error_msg = f"Error procesando {raw_data.get('file_name', 'archivo')}: {str(e)}"
                result.add_error(error_msg)
                self.logger.error(error_msg)
        
        result.processed_data = processed_data
        
        # Calculate date range
        if processed_data:
            dates = [data.fecha for data in processed_data if data.fecha]
            if dates:
                result.date_range = {
                    'start': min(dates),
                    'end': max(dates)
                }
        
        return result 