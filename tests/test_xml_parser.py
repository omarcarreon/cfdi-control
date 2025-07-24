"""
Unit tests for XML parser functionality
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.xml_parser import CFDIXMLParser


class TestCFDIXMLParser(unittest.TestCase):
    """Test cases for CFDIXMLParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = CFDIXMLParser()
        
        # Sample CFDI XML content for testing
        self.sample_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/3" 
                   Fecha="2024-01-15T10:30:00" 
                   FormaPago="01" 
                   SubTotal="1000.00" 
                   Descuento="0.00" 
                   Moneda="MXN" 
                   Total="1160.00" 
                   TipoDeComprobante="I" 
                   MetodoPago="PUE">
    <cfdi:Emisor Rfc="AAA010101AAA" Nombre="EMPRESA EJEMPLO S.A. DE C.V." RegimenFiscal="601"/>
    <cfdi:Receptor Rfc="XEXX010101000" RegimenFiscalReceptor="601" UsoCFDI="G01"/>
    <cfdi:Impuestos TotalImpuestosTrasladados="160.00"/>
</cfdi:Comprobante>'''
    
    def test_parse_cfdi_file_valid(self):
        """Test parsing a valid CFDI XML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(self.sample_xml)
            temp_file = f.name
        
        try:
            result = self.parser.parse_cfdi_file(temp_file)
            
            self.assertIsNotNone(result)
            self.assertIn('B', result)  # Date column
            self.assertEqual(result['B'], '2024-01-15T10:30:00')
            self.assertEqual(result['G'], '1160.00')  # Total
            self.assertEqual(result['J'], 'AAA010101AAA')  # Emisor RFC
            self.assertEqual(result['M'], 'XEXX010101000')  # Receptor RFC
            self.assertIn('file_path', result)
            self.assertIn('file_name', result)
            
        finally:
            os.unlink(temp_file)
    
    def test_parse_cfdi_file_invalid_xml(self):
        """Test parsing an invalid XML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write("This is not valid XML")
            temp_file = f.name
        
        try:
            result = self.parser.parse_cfdi_file(temp_file)
            self.assertIsNone(result)
        finally:
            os.unlink(temp_file)
    
    def test_parse_cfdi_file_nonexistent(self):
        """Test parsing a non-existent file."""
        result = self.parser.parse_cfdi_file("nonexistent_file.xml")
        self.assertIsNone(result)
    
    def test_parse_multiple_files(self):
        """Test parsing multiple XML files."""
        files = []
        try:
            # Create multiple test files
            for i in range(3):
                with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
                    # Modify the XML slightly for each file
                    modified_xml = self.sample_xml.replace('2024-01-15T10:30:00', f'2024-01-{15+i:02d}T10:30:00')
                    f.write(modified_xml)
                    files.append(f.name)
            
            results = self.parser.parse_multiple_files(files)
            
            self.assertEqual(len(results), 3)
            for result in results:
                self.assertIsNotNone(result)
                self.assertIn('B', result)  # Date column
                
        finally:
            for file in files:
                if os.path.exists(file):
                    os.unlink(file)
    
    def test_parse_multiple_files_with_invalid(self):
        """Test parsing multiple files where some are invalid."""
        files = []
        try:
            # Create valid files
            for i in range(2):
                with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
                    modified_xml = self.sample_xml.replace('2024-01-15T10:30:00', f'2024-01-{15+i:02d}T10:30:00')
                    f.write(modified_xml)
                    files.append(f.name)
            
            # Create invalid file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
                f.write("Invalid XML content")
                files.append(f.name)
            
            results = self.parser.parse_multiple_files(files)
            
            # Should have 2 valid results (invalid file should be skipped)
            self.assertEqual(len(results), 2)
            
        finally:
            for file in files:
                if os.path.exists(file):
                    os.unlink(file)
    
    def test_extract_data_from_element(self):
        """Test data extraction from XML element."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(self.sample_xml)
            temp_file = f.name
        
        try:
            result = self.parser.parse_cfdi_file(temp_file)
            
            # Test specific data extraction
            self.assertEqual(result.get('C'), '01')  # FormaPago
            self.assertEqual(result.get('D'), '1000.00')  # SubTotal
            self.assertEqual(result.get('F'), 'MXN')  # Moneda
            self.assertEqual(result.get('K'), 'EMPRESA EJEMPLO S.A. DE C.V.')  # Emisor Nombre
            self.assertEqual(result.get('P'), '160.00')  # TotalImpuestosTrasladados
            
        finally:
            os.unlink(temp_file)
    
    def test_validate_cfdi_structure_valid(self):
        """Test CFDI structure validation with valid file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(self.sample_xml)
            temp_file = f.name
        
        try:
            is_valid = self.parser.validate_cfdi_structure(temp_file)
            self.assertTrue(is_valid)
        finally:
            os.unlink(temp_file)
    
    def test_validate_cfdi_structure_invalid(self):
        """Test CFDI structure validation with invalid file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
<invalid:Root>
    <invalid:Element>Test</invalid:Element>
</invalid:Root>''')
            temp_file = f.name
        
        try:
            is_valid = self.parser.validate_cfdi_structure(temp_file)
            self.assertFalse(is_valid)
        finally:
            os.unlink(temp_file)
    
    def test_get_processing_summary(self):
        """Test processing summary generation."""
        # Create test data
        test_results = [
            {'B': '2024-01-15T10:30:00', 'G': '1000.00', 'F': 'MXN'},
            {'B': '2024-01-16T10:30:00', 'G': '2000.00', 'F': 'MXN'},
        ]
        
        summary = self.parser.get_processing_summary(test_results)
        
        self.assertEqual(summary['total_files'], 2)
        self.assertEqual(summary['successful_files'], 2)
        self.assertEqual(summary['total_amount'], 3000.0)
        self.assertEqual(summary['currency'], 'MXN')
        self.assertIn('date_range', summary)


if __name__ == '__main__':
    unittest.main() 