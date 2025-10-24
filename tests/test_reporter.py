"""
Tests for test reporter.
"""

import unittest
import json
from grumpi_miner.reporter import TestReporter
from grumpi_miner.test_executor import TestSuite, TestResult, TestStatus
from grumpi_miner.combination_generator import DimensionCombination
from grumpi_miner.dimensions import FormatVariation, StructuralArchitecture


class TestTestReporter(unittest.TestCase):
    """Test TestReporter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.reporter = TestReporter()
        
        # Create a test suite with some results
        self.suite = TestSuite(name="Test Report Suite")
        
        combos_and_statuses = [
            ({
                "FormatVariation": FormatVariation.JSON,
                "StructuralArchitecture": StructuralArchitecture.HIERARCHICAL,
            }, TestStatus.PASSED),
            ({
                "FormatVariation": FormatVariation.XML,
                "StructuralArchitecture": StructuralArchitecture.FLAT,
            }, TestStatus.PASSED),
            ({
                "FormatVariation": FormatVariation.YAML,
                "StructuralArchitecture": StructuralArchitecture.TREE,
            }, TestStatus.FAILED, "Test failed due to invalid structure"),
        ]
        
        for dims, status, *error in combos_and_statuses:
            combo = DimensionCombination(dimensions=dims)
            error_msg = error[0] if error else None
            result = TestResult(
                combination=combo,
                status=status,
                error_message=error_msg,
            )
            self.suite.add_result(result)
        
        self.suite.mark_complete()
    
    def test_format_summary(self):
        """Test formatting test suite summary."""
        summary = self.reporter.format_summary(self.suite)
        
        self.assertIn("Test Report Suite", summary)
        self.assertIn("Total Tests: 3", summary)
        self.assertIn("PASSED", summary)
        self.assertIn("FAILED", summary)
    
    def test_format_detailed_results(self):
        """Test formatting detailed results."""
        detailed = self.reporter.format_detailed_results(self.suite)
        
        self.assertIn("Detailed Results", detailed)
        # Should contain information about all tests
        for i in range(1, 4):
            self.assertIn(f"{i}.", detailed)
    
    def test_format_failures(self):
        """Test formatting failures."""
        failures = self.reporter.format_failures(self.suite)
        
        self.assertIn("Failures and Errors", failures)
        self.assertIn("Test failed due to invalid structure", failures)
    
    def test_format_dimension_analysis(self):
        """Test dimension analysis formatting."""
        analysis = self.reporter.format_dimension_analysis(self.suite)
        
        self.assertIn("Dimension Analysis", analysis)
        self.assertIn("FormatVariation", analysis)
        self.assertIn("StructuralArchitecture", analysis)
    
    def test_generate_report(self):
        """Test generating full report."""
        report = self.reporter.generate_report(
            self.suite,
            include_details=True,
            include_dimension_analysis=True
        )
        
        # Should include all sections
        self.assertIn("Test Report Suite", report)
        self.assertIn("Dimension Analysis", report)
        self.assertIn("Failures and Errors", report)
        self.assertIn("Detailed Results", report)
    
    def test_export_json(self):
        """Test exporting results to JSON."""
        json_data = self.reporter.export_json(self.suite)
        
        # Should be JSON-serializable
        json_str = json.dumps(json_data)
        self.assertIsNotNone(json_str)
        
        # Check structure
        self.assertEqual(json_data['name'], "Test Report Suite")
        self.assertEqual(len(json_data['results']), 3)
        self.assertIn('summary', json_data)


if __name__ == '__main__':
    unittest.main()
