"""
Unit tests for data models functionality
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.data_models import CFDIDataProcessor, ProcessingResult, CFDIData


class TestCFDIDataProcessor(unittest.TestCase):
    """Test cases for CFDIDataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = CFDIDataProcessor()
        
        # Sample raw CFDI data for testing (matches XML parser output format)
        self.sample_raw_data = {
            'B': '2024-01-15T10:30:00',  # Date
            'C': '01',  # FormaPago
            'D': '1000.00',  # SubTotal
            'E': '0.00',  # Descuento
            'F': 'MXN',  # Moneda
            'G': '1160.00',  # Total
            'H': 'I',  # TipoDeComprobante
            'I': 'PUE',  # MetodoPago
            'J': 'AAA010101AAA',  # Emisor RFC
            'K': 'EMPRESA EJEMPLO S.A. DE C.V.',  # Emisor Nombre
            'L': '601',  # Emisor RegimenFiscal
            'M': 'XEXX010101000',  # Receptor RFC
            'N': '',  # Receptor Nombre
            'O': '601',  # Receptor RegimenFiscalReceptor
            'P': '160.00',  # TotalImpuestosTrasladados
            'file_path': '/test/path.xml',
            'file_name': 'test.xml'
        }
    
    def test_process_raw_data_success(self):
        """Test successful processing of raw CFDI data."""
        raw_data_list = [self.sample_raw_data]
        
        result = self.processor.process_raw_data(raw_data_list)
        
        self.assertIsInstance(result, ProcessingResult)
        self.assertEqual(result.successful_files, 1)
        self.assertEqual(result.failed_files, 0)
        self.assertEqual(len(result.processed_data), 1)
        self.assertEqual(len(result.errors), 0)
    
    def test_process_raw_data_multiple_records(self):
        """Test processing multiple CFDI records."""
        raw_data_list = []
        for i in range(3):
            data = self.sample_raw_data.copy()
            data['B'] = f'2024-01-{15+i:02d}T10:30:00'
            data['G'] = f'{1160.00 + i * 100:.2f}'
            raw_data_list.append(data)
        
        result = self.processor.process_raw_data(raw_data_list)
        
        self.assertEqual(result.successful_files, 3)
        self.assertEqual(result.failed_files, 0)
        self.assertEqual(len(result.processed_data), 3)
    
    def test_process_raw_data_with_invalid_records(self):
        """Test processing with some invalid records."""
        raw_data_list = [
            self.sample_raw_data,  # Valid
            {},  # Invalid - empty data
            {'B': '2024-01-15T10:30:00'}  # Partial data
        ]
        
        result = self.processor.process_raw_data(raw_data_list)
        
        self.assertEqual(result.successful_files, 1)
        self.assertEqual(result.failed_files, 2)
        self.assertEqual(len(result.processed_data), 1)
        self.assertGreater(len(result.errors), 0)
    
    def test_process_raw_data_empty_list(self):
        """Test processing empty data list."""
        result = self.processor.process_raw_data([])
        
        self.assertEqual(result.successful_files, 0)
        self.assertEqual(result.failed_files, 0)
        self.assertEqual(len(result.processed_data), 0)
    
    def test_process_raw_data_with_missing_required_fields(self):
        """Test processing with missing required fields."""
        incomplete_data = {
            'B': '2024-01-15T10:30:00',  # Date
            'G': '1160.00',  # Total
            # Missing RFC fields
            'file_path': '/test/path.xml',
            'file_name': 'test.xml'
        }
        
        result = self.processor.process_raw_data([incomplete_data])
        
        self.assertEqual(result.successful_files, 0)
        self.assertEqual(result.failed_files, 1)
        self.assertGreater(len(result.errors), 0)


class TestCFDIData(unittest.TestCase):
    """Test cases for CFDIData class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = {
            'B': '2024-01-15T10:30:00',
            'C': '01',
            'D': '1000.00',
            'E': '0.00',
            'F': 'MXN',
            'G': '1160.00',
            'H': 'I',
            'I': 'PUE',
            'J': 'AAA010101AAA',
            'K': 'EMPRESA EJEMPLO S.A. DE C.V.',
            'L': '601',
            'M': 'XEXX010101000',
            'N': '',
            'O': '601',
            'P': '160.00',
            'file_path': '/test/path.xml',
            'file_name': 'test.xml'
        }
    
    def test_from_dict_creation(self):
        """Test creating CFDIData from dictionary."""
        cfdi_data = CFDIData.from_dict(self.sample_data)
        
        self.assertEqual(cfdi_data.fecha, '2024-01-15T10:30:00')
        self.assertEqual(cfdi_data.total, '1160.00')
        self.assertEqual(cfdi_data.emisor_rfc, 'AAA010101AAA')
        self.assertEqual(cfdi_data.receptor_rfc, 'XEXX010101000')
        self.assertEqual(cfdi_data.file_name, 'test.xml')
    
    def test_to_excel_row(self):
        """Test conversion to Excel row format."""
        cfdi_data = CFDIData.from_dict(self.sample_data)
        excel_row = cfdi_data.to_excel_row()
        
        self.assertEqual(excel_row['B'], '2024-01-15T10:30:00')
        self.assertEqual(excel_row['G'], '1160.00')
        self.assertEqual(excel_row['J'], 'AAA010101AAA')
        self.assertEqual(excel_row['M'], 'XEXX010101000')
    
    def test_validate_valid_data(self):
        """Test validation of valid CFDI data."""
        cfdi_data = CFDIData.from_dict(self.sample_data)
        errors = cfdi_data.validate()
        
        self.assertEqual(len(errors), 0)
    
    def test_validate_missing_required_fields(self):
        """Test validation with missing required fields."""
        incomplete_data = self.sample_data.copy()
        incomplete_data['B'] = ''  # Missing date
        incomplete_data['G'] = ''  # Missing total
        incomplete_data['J'] = ''  # Missing emisor RFC
        incomplete_data['M'] = ''  # Missing receptor RFC
        
        cfdi_data = CFDIData.from_dict(incomplete_data)
        errors = cfdi_data.validate()
        
        self.assertGreater(len(errors), 0)
        self.assertIn("Fecha es requerida", errors)
        self.assertIn("Total es requerido", errors)
        self.assertIn("RFC del emisor es requerido", errors)
        self.assertIn("RFC del receptor es requerido", errors)
    
    def test_validate_invalid_numeric_values(self):
        """Test validation with invalid numeric values."""
        invalid_data = self.sample_data.copy()
        invalid_data['G'] = 'not-a-number'  # Invalid total
        
        cfdi_data = CFDIData.from_dict(invalid_data)
        errors = cfdi_data.validate()
        
        self.assertGreater(len(errors), 0)
        self.assertIn("Total debe ser un número válido", errors)
    
    def test_validate_negative_values(self):
        """Test validation with negative values."""
        negative_data = self.sample_data.copy()
        negative_data['G'] = '-100.00'  # Negative total
        
        cfdi_data = CFDIData.from_dict(negative_data)
        errors = cfdi_data.validate()
        
        self.assertGreater(len(errors), 0)
        self.assertIn("Total no puede ser negativo", errors)


class TestProcessingResult(unittest.TestCase):
    """Test cases for ProcessingResult class."""
    
    def test_processing_result_creation(self):
        """Test creating a ProcessingResult instance."""
        result = ProcessingResult(
            successful_files=5,
            failed_files=2,
            total_amount=1000.0,
            currency='MXN',
            date_range={'start': '2024-01-01', 'end': '2024-01-31'},
            errors=['Error 1', 'Error 2'],
            processed_data=[]
        )
        
        self.assertEqual(result.successful_files, 5)
        self.assertEqual(result.failed_files, 2)
        self.assertEqual(result.total_amount, 1000.0)
        self.assertEqual(result.currency, 'MXN')
        self.assertEqual(len(result.errors), 2)
    
    def test_processing_result_default_values(self):
        """Test ProcessingResult with default values."""
        result = ProcessingResult()
        
        self.assertEqual(result.successful_files, 0)
        self.assertEqual(result.failed_files, 0)
        self.assertEqual(result.total_amount, 0.0)
        self.assertEqual(result.currency, '')
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.processed_data), 0)
        self.assertIsNotNone(result.date_range)
    
    def test_add_error(self):
        """Test adding errors to ProcessingResult."""
        result = ProcessingResult()
        result.add_error("Test error")
        
        self.assertEqual(len(result.errors), 1)
        self.assertIn("Test error", result.errors)
    
    def test_get_summary_text(self):
        """Test summary text generation."""
        result = ProcessingResult(
            successful_files=3,
            failed_files=1,
            total_amount=1500.0,
            currency='MXN',
            date_range={'start': '2024-01-01', 'end': '2024-01-31'},
            errors=['Error 1']
        )
        
        summary = result.get_summary_text()
        
        self.assertIn("3", summary)  # Successful files
        self.assertIn("1", summary)  # Failed files
        self.assertIn("1500.00", summary)  # Total amount
        self.assertIn("MXN", summary)  # Currency
        self.assertIn("Error 1", summary)  # Error message


if __name__ == '__main__':
    unittest.main() 