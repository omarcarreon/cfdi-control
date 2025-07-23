"""
XML Parser for CFDI (Mexican electronic invoices)
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Import configuration
from config.settings import CFDI_MAPPING

class CFDIXMLParser:
    """Parser for CFDI XML files with predefined mapping."""
    
    def __init__(self):
        """Initialize the CFDI XML parser."""
        self.logger = logging.getLogger(__name__)
        
    def parse_cfdi_file(self, xml_file_path: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single CFDI XML file and extract data according to predefined mapping.
        
        Args:
            xml_file_path: Path to the XML file
            
        Returns:
            Dictionary with extracted data or None if parsing fails
        """
        try:
            # Parse XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            
            # Extract data using predefined mapping
            extracted_data = {}
            
            for xml_path, excel_column in CFDI_MAPPING.items():
                value = self._extract_xml_value(root, xml_path)
                extracted_data[excel_column] = value
                
            # Add file information
            extracted_data['file_path'] = xml_file_path
            extracted_data['file_name'] = Path(xml_file_path).name
            
            self.logger.info(f"Successfully parsed CFDI file: {xml_file_path}")
            return extracted_data
            
        except ET.ParseError as e:
            self.logger.error(f"XML parsing error in {xml_file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error parsing {xml_file_path}: {e}")
            return None
    
    def _extract_xml_value(self, root: ET.Element, xml_path: str) -> str:
        """
        Extract value from XML using XPath-like path.
        
        Args:
            root: Root element of XML tree
            xml_path: Path to extract (e.g., "cfdi:Comprobante/@Fecha")
            
        Returns:
            Extracted value or empty string if not found
        """
        try:
            # Define namespace mapping
            namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/4'}
            
            # Split path into element and attribute
            if '/@' in xml_path:
                element_path, attr_name = xml_path.split('/@')
                
                # Handle root element attributes (cfdi:Comprobante)
                if element_path == 'cfdi:Comprobante':
                    return root.get(attr_name, '')
                
                # Handle child element attributes
                element = root.find(element_path, namespaces)
                if element is not None:
                    return element.get(attr_name, '')
            else:
                # Just element path (no attribute)
                element = root.find(xml_path, namespaces)
                if element is not None:
                    return element.text or ''
                        
        except Exception as e:
            self.logger.warning(f"Error extracting {xml_path}: {e}")
            
        return ''
    
    def parse_multiple_files(self, xml_file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Parse multiple CFDI XML files.
        
        Args:
            xml_file_paths: List of XML file paths
            
        Returns:
            List of dictionaries with extracted data
        """
        results = []
        
        for file_path in xml_file_paths:
            data = self.parse_cfdi_file(file_path)
            if data:
                results.append(data)
            else:
                self.logger.warning(f"Failed to parse file: {file_path}")
                
        return results
    
    def validate_cfdi_structure(self, xml_file_path: str) -> bool:
        """
        Basic validation of CFDI XML structure.
        
        Args:
            xml_file_path: Path to the XML file
            
        Returns:
            True if valid CFDI structure, False otherwise
        """
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            
            # Check if root element is Comprobante
            if 'Comprobante' in root.tag:
                return True
            else:
                self.logger.warning(f"Root element is not Comprobante: {root.tag}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error validating CFDI structure: {e}")
            return False
    
    def get_processing_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a summary of processing results.
        
        Args:
            results: List of parsed CFDI data
            
        Returns:
            Summary dictionary with statistics
        """
        if not results:
            return {
                'total_files': 0,
                'successful_files': 0,
                'failed_files': 0,
                'total_amount': 0.0,
                'currency': '',
                'date_range': {'start': '', 'end': ''}
            }
        
        # Calculate statistics
        total_amount = 0.0
        currencies = set()
        dates = []
        
        for result in results:
            # Sum total amounts
            total_str = result.get('G', '0')
            try:
                total_amount += float(total_str)
            except ValueError:
                pass
            
            # Collect currencies
            currency = result.get('F', '')
            if currency:
                currencies.add(currency)
            
            # Collect dates
            date = result.get('B', '')
            if date:
                dates.append(date)
        
        return {
            'total_files': len(results),
            'successful_files': len(results),
            'failed_files': 0,  # Will be calculated from total input
            'total_amount': total_amount,
            'currency': list(currencies)[0] if currencies else '',
            'date_range': {
                'start': min(dates) if dates else '',
                'end': max(dates) if dates else ''
            }
        } 