"""
Settings and configuration for CFDI Control Application
"""

# CFDI XML to Excel Column Mapping
# Maps XML paths to Excel column letters (row 3 headers)
CFDI_MAPPING = {
    "cfdi:Comprobante/@Fecha": "B",           # Date
    "cfdi:Comprobante/@FormaPago": "C",       # Payment Method
    "cfdi:Comprobante/@SubTotal": "D",        # Subtotal
    "cfdi:Comprobante/@Descuento": "E",       # Discount
    "cfdi:Comprobante/@Moneda": "F",          # Currency
    "cfdi:Comprobante/@Total": "G",           # Total
    "cfdi:Comprobante/@TipoDeComprobante": "H", # Document Type
    "cfdi:Comprobante/@MetodoPago": "I",      # Payment Method
    "cfdi:Emisor/@Rfc": "J",                  # Sender RFC
    "cfdi:Emisor/@Nombre": "K",               # Sender Name
    "cfdi:Emisor/@RegimenFiscal": "L",       # Sender Tax Regime
    "cfdi:Receptor/@Rfc": "M",                # Receiver RFC
    "cfdi:Receptor/@RegimenFiscalReceptor": "N",             # Receiver Tax Regime
    "cfdi:Receptor/@UsoCFDI": "O",     # Receiver Uso CFDI
    "cfdi:Impuestos/@TotalImpuestosTrasladados": "P" # Total Taxes
}

# Excel Template Configuration
EXCEL_CONFIG = {
    "header_row": 3,              # Row where column headers are located
    "data_start_row": 4,          # Row where data starts (after headers)
    "month_tabs": [               # Expected month tab names
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
}

# Application Settings
APP_CONFIG = {
    "app_name": "CFDI Control Application",
    "version": "1.0.0",
    "window_size": "800x600",
    "supported_file_types": {
        "excel": [".xlsx", ".xls"],
        "xml": [".xml"]
    }
}

# Processing Settings
PROCESSING_CONFIG = {
    "max_files_per_batch": 1000,  # Maximum XML files to process at once
    "progress_update_interval": 0.1,  # Progress bar update interval (seconds)
    "output_filename_template": "CFDI_Control_{year}_{month:02d}_{timestamp}.xlsx"
} 