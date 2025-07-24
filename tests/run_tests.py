#!/usr/bin/env python3
"""
Test runner for CFDI Control Application
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def run_all_tests():
    """Run all test suites."""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

def run_specific_test(test_name):
    """Run a specific test module or class."""
    loader = unittest.TestLoader()
    
    if test_name.endswith('.py'):
        # Load specific test file
        test_file = Path(__file__).parent / test_name
        if test_file.exists():
            suite = loader.loadTestsFromName(test_name[:-3], str(test_file))
        else:
            print(f"Test file {test_name} not found.")
            return 1
    else:
        # Load specific test class or method
        suite = loader.loadTestsFromName(test_name)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        exit_code = run_specific_test(test_name)
    else:
        # Run all tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code) 