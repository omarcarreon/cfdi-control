# CFDI Control Application - Testing Documentation

## Overview

This directory contains comprehensive tests for the CFDI Control Application, covering unit tests, integration tests, and data validation tests.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── run_tests.py               # Test runner script
├── test_xml_parser.py         # XML parser unit tests
├── test_excel_processor.py    # Excel processor unit tests
├── test_data_models.py        # Data models unit tests
└── test_integration.py        # Integration tests
```

## Test Categories

### 1. Unit Tests

#### XML Parser Tests (`test_xml_parser.py`)
- **Valid XML parsing**: Tests parsing of valid CFDI XML files
- **Invalid XML handling**: Tests error handling for malformed XML
- **Multiple file processing**: Tests batch processing of XML files
- **Data extraction**: Tests extraction of specific CFDI fields
- **Structure validation**: Tests CFDI structure validation
- **Processing summary**: Tests summary generation

#### Excel Processor Tests (`test_excel_processor.py`)
- **Template loading**: Tests loading of Excel templates
- **Month tab management**: Tests finding and managing month tabs
- **Data filling**: Tests filling CFDI data into Excel sheets
- **Template validation**: Tests validation of Excel template structure
- **File operations**: Tests saving and creating output files
- **Error handling**: Tests handling of invalid templates

#### Data Models Tests (`test_data_models.py`)
- **CFDI data creation**: Tests creating CFDI data objects
- **Data validation**: Tests validation of CFDI data fields
- **Data processing**: Tests processing of raw CFDI data
- **Error handling**: Tests handling of invalid data
- **Processing results**: Tests result object creation and management

### 2. Integration Tests (`test_integration.py`)
- **Complete workflow**: Tests the entire XML → Excel workflow
- **Error scenarios**: Tests handling of invalid files and templates
- **Performance testing**: Tests processing of multiple files
- **Data integrity**: Tests that data is preserved through the workflow
- **Edge cases**: Tests empty data and minimal XML files

## Running Tests

### Run All Tests
```bash
python tests/run_tests.py
```

### Run Specific Test File
```bash
python tests/run_tests.py test_xml_parser.py
```

### Run with pytest
```bash
python -m pytest tests/ -v
```

### Run Specific Test Class
```bash
python -m pytest tests/test_xml_parser.py::TestCFDIXMLParser -v
```

## Test Coverage

### XML Parser Coverage
- ✅ Valid CFDI XML parsing
- ✅ Invalid XML error handling
- ✅ Multiple file processing
- ✅ Data extraction from XML elements
- ✅ CFDI structure validation
- ✅ Processing summary generation
- ✅ Namespace handling (CFDI v3 and v4)

### Excel Processor Coverage
- ✅ Template loading and validation
- ✅ Month tab finding and management
- ✅ Data filling into Excel sheets
- ✅ Output file creation
- ✅ Error handling for invalid templates
- ✅ File operations (save, load)

### Data Models Coverage
- ✅ CFDI data object creation
- ✅ Data validation (required fields, formats)
- ✅ Raw data processing
- ✅ Error collection and reporting
- ✅ Processing result management

### Integration Coverage
- ✅ Complete end-to-end workflow
- ✅ Error scenario handling
- ✅ Performance with multiple files
- ✅ Data integrity verification
- ✅ Edge case handling

## Test Data

### Sample CFDI XML
Tests use a realistic CFDI XML structure with:
- Root `cfdi:Comprobante` element
- Required attributes (Fecha, Total, etc.)
- Child elements (Emisor, Receptor, Impuestos)
- Proper namespace declarations

### Sample Excel Templates
Tests create Excel templates with:
- 12 month tabs (Enero through Diciembre)
- Headers in row 3
- Proper column structure
- CFDI field mappings

## Error Scenarios Tested

1. **Invalid XML files**: Malformed XML, missing elements
2. **Invalid Excel templates**: Missing tabs, wrong structure
3. **Missing required data**: Incomplete CFDI information
4. **Invalid data formats**: Wrong date formats, invalid numbers
5. **File system errors**: Non-existent files, permission issues
6. **Empty data sets**: No valid data to process

## Performance Considerations

- Tests process up to 10 XML files simultaneously
- Excel operations are tested with realistic data volumes
- Memory usage is monitored during batch operations
- Processing time is measured for workflow validation

## Quality Metrics

- **Test Count**: 44 total tests
- **Coverage**: All major components tested
- **Error Scenarios**: Comprehensive error handling tested
- **Integration**: Complete workflow tested
- **Performance**: Batch processing validated

## Maintenance

### Adding New Tests
1. Create test file in `tests/` directory
2. Follow naming convention: `test_<component>.py`
3. Use descriptive test method names
4. Include proper setup and teardown
5. Add to `run_tests.py` if needed

### Updating Tests
- When modifying core functionality, update corresponding tests
- Ensure new features are covered by tests
- Maintain backward compatibility in test data
- Update test documentation when adding new test categories

## Continuous Integration

Tests are designed to run in CI/CD environments:
- No external dependencies beyond the application
- Temporary file cleanup in teardown
- Platform-independent test data
- Clear success/failure reporting

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure `src/` is in Python path
2. **File permission errors**: Check temporary directory access
3. **XML parsing errors**: Verify test XML structure
4. **Excel file errors**: Check openpyxl installation

### Debug Mode
Run tests with verbose output:
```bash
python tests/run_tests.py --verbose
```

### Test Isolation
Each test creates its own temporary files and cleans up after execution to ensure test isolation. 